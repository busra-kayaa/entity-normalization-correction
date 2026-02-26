import os
import json
import torch
import warnings
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    MT5ForConditionalGeneration,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq
)

# Gereksiz uyarıları kapatma
warnings.filterwarnings("ignore")
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

def train_mt5_colab():
    model_name = "google/mt5-base"

    train_path = "train.json"
    valid_path = "validation.json"
    output_dir = "./final_mt5_base_model"

    print(f"🔄 Model yükleniyor... Eğitim: {train_path} | Doğrulama: {valid_path}")

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = MT5ForConditionalGeneration.from_pretrained(model_name, use_safetensors=False)
    model.config.tie_word_embeddings = False

    # Dosya Kontrolü
    if not os.path.exists(train_path) or not os.path.exists(valid_path):
        print("❌ HATA: 'train.json' veya 'validation.json' bulunamadı!")
        print("Lütfen iki dosyayı da sol taraftaki dosya menüsüne yüklediğinden emin ol.")
        return

    # Verileri Oku
    with open(train_path, "r", encoding="utf-8") as f:
        train_data = json.load(f)
    with open(valid_path, "r", encoding="utf-8") as f:
        valid_data = json.load(f)

    # Ön İşleme (Preprocessing)
    def preprocess_function(examples):
        inputs = ["gec: " + doc for doc in examples["input"]]
        model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

        labels = tokenizer(text_target=examples["target"], max_length=128, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # Train Dataset Hazırlığı
    train_dataset = Dataset.from_list(train_data)
    tokenized_train = train_dataset.map(preprocess_function, batched=True)

    # Validation Dataset Hazırlığı
    valid_dataset = Dataset.from_list(valid_data)
    tokenized_valid = valid_dataset.map(preprocess_function, batched=True)

# Eğitim Argümanları
    # 🛡️ NaN HATASINI VE OOM'U ÇÖZEN NİHAİ EĞİTİM ARGÜMANLARI
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        learning_rate=1e-3,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=16,
        gradient_checkpointing=True,
        optim="adafactor",
        weight_decay=0.01,
        num_train_epochs=5,
        predict_with_generate=True,
        fp16=False,
        logging_steps=50,
        save_total_limit=2
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_valid,
        processing_class=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )

    print("🚀 mT5-Base Eğitimi GPU Üzerinde Başlıyor...")
    trainer.train()

    # En İyi Modeli Kaydet
    trainer.save_model(output_dir)
    print(f"✅ Başarılı! En iyi model şuraya kaydedildi: {output_dir}")
    print("⚠️ ÖNEMLİ: Sol taraftaki klasör simgesinden klasörü indirmeyi unutma!")

if __name__ == "__main__":
    train_mt5_colab()
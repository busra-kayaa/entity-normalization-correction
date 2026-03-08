# !pip install transformers[torch] datasets -q

import torch
import json
import shutil
from datasets import Dataset, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    DataCollatorForSeq2Seq
)


def train_byt5_colab_pro():
    # 1. Veri Yükleme
    def load_data(path):
        with open(path, 'r', encoding='utf-8') as f:
            return Dataset.from_list(json.load(f))

    try:
        raw_datasets = DatasetDict({
            "train": load_data("train.json"),
            "validation": load_data("validation.json")
        })
        print("✅ Veri setleri başarıyla yüklendi.")
    except FileNotFoundError:
        print("❌ HATA: 'train.json' veya 'validation.json' bulunamadı!")
        return

    # 2. Model ve Tokenizer
    model_name = "google/byt5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # 3. Dinamik Padding ile Ön İşleme
    def preprocess_function(examples):
        # ByT5 için prefix kullanmıyoruz, girdi saf haliyle veriliyor
        model_inputs = tokenizer(examples["input"], max_length=256, truncation=True)
        labels = tokenizer(text_target=examples["target"], max_length=256, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = raw_datasets.map(preprocess_function, batched=True)

    # 4. Eğitim Ayarları (A100/L4 Optimize)
    training_args = TrainingArguments(
        output_dir="./byt5_pro_checkpoints",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        gradient_accumulation_steps=4,
        num_train_epochs=20,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        bf16=torch.cuda.is_bf16_supported(),
        fp16=not torch.cuda.is_bf16_supported(),
        logging_steps=10,
        report_to="none"
    )

    # 5. Data Collator (Dinamik Padding ve -100 atamasını otomatik yapar)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, label_pad_token_id=-100)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    # 6. Başlat ve Kaydet
    print(f"🔥 ByT5 Eğitimi Başlıyor... Donanım: {torch.cuda.get_device_name(0)}")
    trainer.train()

    model.save_pretrained("./final_byt5_model")
    tokenizer.save_pretrained("./final_byt5_model")

    print("📦 Model zip formatında sıkıştırılıyor...")
    shutil.make_archive("final_byt5_model", 'zip', "./final_byt5_model")
    print("🏆 Eğitim bitti! 'final_byt5_model.zip' dosyası indirime hazır.")


if __name__ == "__main__":
    train_byt5_colab_pro()
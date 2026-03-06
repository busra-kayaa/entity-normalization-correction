import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback
)


def train_mbart_colab_pro():
    model_name = "facebook/mbart-large-50"
    output_dir = "./final_mbart_model"

    print(f"🔄 mBART Yükleniyor... Donanım: {torch.cuda.get_device_name(0)}")

    # mBART için dil ayarları (İngilizce - İngilizce çalışıp içindeki TR/Bozuklukları düzeltecek)
    tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang="en_XX", tgt_lang="en_XX")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Veri Yükleme
    with open("train.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)
    with open("validation.json", "r", encoding="utf-8") as f:
        valid_data = json.load(f)

    def preprocess_function(examples):
        # mBART prefix gerektirmez, doğrudan gürültülü metni alır
        model_inputs = tokenizer(examples["input"], max_length=128, truncation=True, padding="max_length")
        labels = tokenizer(text_target=examples["target"], max_length=128, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_train = Dataset.from_list(train_data).map(preprocess_function, batched=True)
    tokenized_valid = Dataset.from_list(valid_data).map(preprocess_function, batched=True)

    # 🚀 Colab Pro A100/L4 Ayarları
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        gradient_accumulation_steps=4,
        num_train_epochs=10,
        predict_with_generate=True,
        bf16=torch.cuda.is_bf16_supported(),  # Pro donanım hızlandırıcısı
        fp16=not torch.cuda.is_bf16_supported(),
        logging_steps=20,
        save_total_limit=2,
        report_to="none"
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_valid,
        processing_class=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    print("🚀 mBART Eğitimi Başlıyor...")
    trainer.train()

    # Modeli Kaydet
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"✅ Eğitim tamamlandı! Model şuraya kaydedildi: {output_dir}")

    # 📦 MODELİ PAKETLE VE İNDİR
    print("📦 Model zip formatında sıkıştırılıyor, lütfen bekleyin...")
    #shutil.make_archive("mbart_model_pro", 'zip', output_dir)

    print("⬇️ Model bilgisayarınıza indiriliyor...")
    #files.download("mbart_model_pro.zip")


if __name__ == "__main__":
    train_mbart_colab_pro()
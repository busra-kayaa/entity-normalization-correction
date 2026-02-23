import os
import json
import torch
from pathlib import Path
from datasets import Dataset, DatasetDict
from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)

# 1. Klasör Ayarları
current_file_path = Path(__file__).resolve()
data_dir = current_file_path.parent.parent
output_dir = current_file_path.parent

# 2. Cihaz Ayarı
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Model şu cihazda eğitilecek: {device.upper()}")
print(f"📁 Veri klasörü: {data_dir}")


# 3. Veri Yükleme Fonksiyonu
def load_json_data(file_name):
    path = data_dir / file_name

    if not path.exists():
        raise FileNotFoundError(
            f"❌ Dosya bulunamadı: {path}\nLütfen dosyaların 'step5_models' klasöründe olduğundan emin olun.")

    print(f"📖 Veri yükleniyor: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Dataset.from_list([{"input": item["input"], "target": item["target"]} for item in data])


# 4. Model ve Tokenizer
MODEL_ID = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(MODEL_ID, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(MODEL_ID).to(device)


# 5. Veri Önişleme
def preprocess_function(examples):
    inputs = ["gec: " + text for text in examples["input"]]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(text_target=examples["target"], max_length=128, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


# Verileri Yükle
try:
    print("📦 Veri setleri haritalanıyor...")
    raw_datasets = DatasetDict({
        "train": load_json_data("train.json"),
        "val": load_json_data("validation.json")
    })
    tokenized_datasets = raw_datasets.map(preprocess_function, batched=True)
except Exception as e:
    print(f"❌ Hata: {e}")
    exit()

# 6. Eğitim Parametreleri (v4.46+ Uyumlu)
training_args = TrainingArguments(
    output_dir=str(output_dir / "checkpoints"),
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-4,
    per_device_train_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_steps=10,
    load_best_model_at_end=True,
    fp16=(device == "cuda"),
    report_to="none"
)

# 7. Trainer Kurulumu
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["val"],
    processing_class=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
)

# 8. Eğitimi Başlat
print("🏗️ Eğitim süreci başlıyor... CPU üzerinde biraz zaman alabilir.")
trainer.train()

# 9. Final Modelini Kaydet
final_model_path = output_dir / "final_model"
trainer.save_model(str(final_model_path))
tokenizer.save_pretrained(str(final_model_path))

print(f"✅ Başarılı! Model şuraya kaydedildi: {final_model_path}")
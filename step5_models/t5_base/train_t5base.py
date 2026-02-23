import json
from datasets import Dataset, DatasetDict
from transformers import T5Tokenizer, T5ForConditionalGeneration, TrainingArguments, Trainer

# 1. Model ve Tokenizer Ayarı
model_name = "google-t5/t5-base" # Base model seçimi
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# 2. Veri Yükleme (Dosyaları Colab'a yüklediğini varsayıyorum)
def load_local_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return Dataset.from_list(json.load(f))

raw_datasets = DatasetDict({
    "train": load_local_json("../train.json"),
    "validation": load_local_json("../validation.json")
})

# 3. Ön İşleme Fonksiyonu
def preprocess_function(examples):
    # Giriş metinlerine "gec: " prefix'ini ekle
    inputs = ["gec: " + doc for doc in examples["input"]]

    # Model girişlerini (inputs) tokenize et
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

    # Hedef metinleri (targets/labels) tokenize et
    # Yeni yöntemde 'text_target' parametresini kullanıyoruz
    labels = tokenizer(text_target=examples["target"], max_length=128, truncation=True, padding="max_length")

    # ID'leri model_inputs içine yerleştir
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Veriyi modele hazır hale getiren kritik satır
tokenized_datasets = raw_datasets.map(preprocess_function, batched=True)

# 4. Eğitim Argümanları (En Sade ve Güncel Hal)
training_args = TrainingArguments(
    output_dir="./t5_base_results",
    eval_strategy="epoch",
    learning_rate=3e-4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    save_total_limit=2,
    fp16=True,
    push_to_hub=False,
    report_to="none"
)

# 5. Trainer ve Başlatma (Tokenizer argümanı çıkarıldı)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"]
)

print("🚀 T5-Base Eğitimi Başlıyor...")
trainer.train()
# 6. Modeli Kaydet
model.save_pretrained("./final_t5_base_model")
tokenizer.save_pretrained("./final_t5_base_model")
print("✅ Eğitim bitti, model kaydedildi!")


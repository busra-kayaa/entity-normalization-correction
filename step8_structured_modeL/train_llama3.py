# Unsloth ve eğitim araçlarının kurulumu
#!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
#!pip install --no-deps trl peft accelerate bitsandbytes

from unsloth import FastLanguageModel
import torch

max_seq_length = 2048
dtype = None
load_in_4bit = True

# 1. Ana Modeli Yükle
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/meta-llama-3.1-8b-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# 2. LoRA Katmanlarını Ekle
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)
print("✅ Model ve LoRA adaptörleri hazır!")


import json
from datasets import load_dataset

# 1. Yeni Çoğul Şablon
alpaca_prompt = """Aşağıdaki hatalı metni profesyonelce düzelt ve bulduğun TÜM farklı hata türlerini bir liste (array) olarak belirt.
Yanıtını mutlaka şu JSON formatında ver: {{"corrected": "...", "error_types": ["hata1", "hata2"]}}

### Giriş:
{}

### Yanıt:
{}"""

EOS_TOKEN = tokenizer.eos_token

# 2. Formatlayıcı Fonksiyon
def formatting_prompts_func(examples):
    inputs, targets, error_types = examples["input"], examples["target"], examples["error_type"]
    outputs = []
    for i, t, e in zip(inputs, targets, error_types):
        # Virgüllü stringi listeye çevir
        e_list = [h.strip() for h in str(e).split(",") if h.strip()]
        # JSON objesini oluştur (Türkçe karakterleri koruyarak)
        res_json = json.dumps({"corrected": t, "error_types": e_list}, ensure_ascii=False)
        outputs.append(alpaca_prompt.format(i, res_json) + EOS_TOKEN)
    return {"text": outputs}

# 3. Dosyaları Yükle (train.json ve validation.json Colab'da olmalı!)
dataset = load_dataset("json", data_files="train.json", split="train")
val_dataset = load_dataset("json", data_files="validation.json", split="train")

dataset = dataset.map(formatting_prompts_func, batched = True)
val_dataset = val_dataset.map(formatting_prompts_func, batched = True)

print(f"✅ Veriler hazırlandı. Eğitim: {len(dataset)}, Doğrulama: {len(val_dataset)}")


from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    eval_dataset = val_dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10,
        num_train_epochs = 1,
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 50,
        eval_strategy = "steps",
        eval_steps = 100, # Her 100 adımda bir başarıyı ölç
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

print("🔥 Eğitim Başlıyor...")
trainer.train()


model_adı = "mizan_multi_label_model"
model.save_pretrained(model_adı)
tokenizer.save_pretrained(model_adı)

import os
os.system(f"zip -r {model_adı}.zip {model_adı}")

# files.download(f"{model_adı}.zip")
print("🎉 Model başarıyla indirildi!")
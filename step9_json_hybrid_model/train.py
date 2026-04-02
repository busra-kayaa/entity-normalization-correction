# ==========================================
# 1. KURULUM VE KÜTÜPHANELER
# ==========================================
#!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
#!pip install --no-deps xformers trl peft accelerate bitsandbytes datasets

import torch
import os
import json
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# ==========================================
# 2. MODEL VE LORA YÜKLEME
# ==========================================
max_seq_length = 2048
dtype = None
load_in_4bit = True

print("🧠 1. Ana Model Yükleniyor...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

print("⚙️ 2. LoRA Katmanları Ekleniyor...")
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

# ==========================================
# 3. VERİ SETİ HAZIRLIĞI
# ==========================================
prompt_template = """You are an expert text correction system. Correct the input text and provide a detailed JSON analysis.
Use ONLY these 8 error types: "deascii", "omission", "insertion", "transposition", "substitution", "space", "terminology", "common".

### Input:
{}

### Response:
{}"""

EOS_TOKEN = tokenizer.eos_token

def formatting_prompts_func(examples):
    inputs = examples["input_text"]
    responses = examples["target_json"]
    outputs = []
    for i, r in zip(inputs, responses):
        outputs.append(prompt_template.format(i, r) + EOS_TOKEN)
    return {"text": outputs}

print("📂 Eğitim ve Doğrulama (Validation) setleri yükleniyor...")
train_raw = load_dataset("json", data_files="mizan_v2_train.json", split="train")
val_raw = load_dataset("json", data_files="mizan_v2_validation.json", split="train")

train_dataset = train_raw.map(formatting_prompts_func, batched = True)
val_dataset = val_raw.map(formatting_prompts_func, batched = True)

print(f"✅ Eğitim Seti: {len(train_dataset)} satır, Doğrulama Seti: {len(val_dataset)} satır")

# ==========================================
# 4. EĞİTİMİ BAŞLAT
# ==========================================
trainer = SFTTrainer(
    model = model,
    processing_class = tokenizer,
    train_dataset = train_dataset,
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
        logging_steps = 20,
        eval_strategy = "steps",
        eval_steps = 50,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

print("🔥 Eğitim Başlıyor! Arkanıza yaslanın...")
trainer.train()

# ==========================================
# 5. MODELİ KAYDET VE İNDİR
# ==========================================
model_adı = "mizan_multi_label_v2"
print(f"💾 Model '{model_adı}' klasörüne kaydediliyor...")
model.save_pretrained(model_adı)
tokenizer.save_pretrained(model_adı)

print(f"📦 Model {model_adı}.zip olarak sıkıştırılıyor...")
os.system(f"zip -r {model_adı}.zip {model_adı}")

# from google.colab import files
print("📥 Zip dosyası bilgisayarınıza indiriliyor... (Tarayıcı izin isterse onaylayın)")
# files.download(f"{model_adı}.zip")

print("🎉 Eğitim kusursuz tamamlandı! Mizan v2 artık aramızda!")
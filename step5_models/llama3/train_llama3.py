import torch
import gc
import json
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer


def train_llama3_qlora_colab_optimized():
    torch.cuda.empty_cache()
    gc.collect()

    def format_prompt(example):
        prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Please correct the typographical, de-asciification, and terminology errors in the following text. Do not add any extra comments.
Text: {example['input']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{example['target']}<|eot_id|>"""
        return {"text": prompt}

    def load_and_format_data(path):
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        dataset = Dataset.from_list(raw_data)
        return dataset.map(format_prompt)

    try:
        train_dataset = load_and_format_data("train.json")
        val_dataset = load_and_format_data("validation.json")
    except FileNotFoundError:
        print("❌ HATA: Veri setleri bulunamadı!")
        return

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model_id = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"

    print("🔄 Llama 3.1 (8B) yükleniyor...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    tokenizer.model_max_length = 512

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )

    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    training_args = TrainingArguments(
        output_dir="./llama3_checkpoints",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-4,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=8,
        gradient_checkpointing=True,
        num_train_epochs=5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        bf16=torch.cuda.is_bf16_supported(),
        fp16=not torch.cuda.is_bf16_supported(),
        logging_steps=10,
        report_to="none",
        optim="paged_adamw_8bit"
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        args=training_args
    )

    print(f"🔥 Llama 3.1 QLoRA Eğitimi Başlıyor... Donanım: {torch.cuda.get_device_name(0)}")
    trainer.train()

    final_output_dir = "./final_llama3_lora"
    trainer.model.save_pretrained(final_output_dir)
    tokenizer.save_pretrained(final_output_dir)

    print(f"✅ Eğitim bitti! LoRA adaptörleri '{final_output_dir}' klasörüne kaydedildi.")


if __name__ == "__main__":
    train_llama3_qlora_colab_optimized()
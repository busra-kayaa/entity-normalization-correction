import torch
import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from pathlib import Path
from datetime import datetime


def test_llama3_manual_categorized():
    base_model_id = "unsloth/Meta-Llama-3.1-8B-bnb-4bit"
    lora_path = "./lora_adaptorum"

    reports_dir = Path("./reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_excel = reports_dir / "llama3_manual_test_results.xlsx"
    output_text = reports_dir / "llama3_manual_test_report.txt"

    if not os.path.exists(lora_path):
        print(f"❌ Hata: LoRA ağırlıkları bulunamadı: {lora_path}")
        return

    print("🔄 Llama 3.1 Temel Modeli ve Adaptörler Yükleniyor...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_id, quantization_config=bnb_config, device_map="auto")
    model = PeftModel.from_pretrained(base_model, lora_path)
    model.eval()

    test_cases = [
        ("Turkiye is a bridge between Europe and Asia.", "Türkiye is a bridge between Europe and Asia.", "deascii"),
        ("TURKIYE is now the official name.", "Türkiye is now the official name.", "deascii"),
        ("We are going to Istanbul for the summit.", "We are going to İstanbul for the summit.", "deascii"),
        ("The flight was from London to Turkey.", "The flight was from London to Türkiye.", "terminology"),
        ("The government of Burma is under pressure.", "The government of Myanmar is under pressure.", "terminology"),
        ("Swaziland has changed its name to Eswatini.", "Eswatini has changed its name to Eswatini.", "terminology"),
        ("President Erdğan will speak soon.", "President Erdoğan will speak soon.", "omission"),
        ("The Prsident made a choice.", "The President made a choice.", "omission"),
        ("The poliitcal situation is unstable.", "The political situation is unstable.", "insertion"),
        ("Irsaeli officials reported the news.", "Israeli officials reported the news.", "transposition"),
        ("NewYork is the city that never sleeps.", "New York is the city that never sleeps.", "space"),
        ("The goverment announced a new policy.", "The government announced a new policy.", "common"),
        ("The month of May is beautiful.", "The month of May is beautiful.", "none"),
        ("This is a correctly written English sentence.", "This is a correctly written English sentence.", "none")
    ]

    system_instruction = (
        "You are an expert text normalization and error correction AI. "
        "Correct any spelling, grammar, punctuation, and specific entity terminology errors in the text. "
        "Apply standard entity normalization rules (e.g., 'Turkey' to 'Türkiye'). "
        "If the input is already correct, return it exactly as is."
    )
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:\n"""

    results_list = []
    category_stats = {}

    print(f"\n🧪 {len(test_cases)} manuel senaryo Llama 3.1 ile test ediliyor...\n" + "=" * 80)

    for input_raw, target, category in test_cases:
        if category not in category_stats:
            category_stats[category] = {"total": 0, "correct": 0}

        prompt = alpaca_prompt.format(system_instruction, input_raw.strip())
        inputs = tokenizer([prompt], return_tensors="pt").to("cuda")

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, use_cache=True, temperature=0.1)

        decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        predicted = decoded_output.split("### Response:\n")[-1].strip()

        is_correct = predicted.lower() == target.lower().strip()
        category_stats[category]["total"] += 1
        if is_correct: category_stats[category]["correct"] += 1

        results_list.append({"Kategori": category.upper(), "Girdi": input_raw, "Beklenen": target, "Tahmin": predicted,
                             "Durum": "✅ DOĞRU" if is_correct else "❌ YANLIŞ"})
        print(f"[{category.upper()}] Girdi: {input_raw}\nTahmin: {predicted} {'✅' if is_correct else '❌'}\n{'-' * 80}")

    df_results = pd.DataFrame(results_list)
    df_summary = pd.DataFrame([{"Hata Türü": cat.upper(), "Toplam": st["total"], "Doğru": st["correct"],
                                "Başarı (%)": f"%{(st['correct'] / st['total']) * 100:.2f}"} for cat, st in
                               category_stats.items()])

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name="Test Detayları", index=False)
        df_summary.to_excel(writer, sheet_name="Kategori Özeti", index=False)

    print(f"✅ Test tamamlandı. Rapor kaydedildi: {reports_dir}")


if __name__ == "__main__":
    test_llama3_manual_categorized()
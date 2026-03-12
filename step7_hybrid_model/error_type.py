import json
import torch
import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

def detailed_error_analysis_llama3_local():
    # 1. Klasör ve Yol Ayarları (VS Code ortamı için güncellendi)
    base_model_id = "unsloth/Meta-Llama-3.1-8B-bnb-4bit" # Eğitimde kullandığımız base model
    lora_path = "./lora_adaptorum" # İndirdiğin LoRA klasörünün adı
    data_path = "./test.json"

    reports_dir = Path("./reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_output = reports_dir / "llama3_error_type_performance_detailed.xlsx"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Llama 3.1 Detaylı Analiz Başlatıldı (Cihaz: {device.upper()})")

    if not os.path.exists(lora_path):
        print(f"❌ HATA: LoRA ağırlıkları bulunamadı! Yol: {lora_path}")
        return

    # 2. Model ve Adaptör Yükleme (4-bit QLoRA)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )

    model = PeftModel.from_pretrained(base_model, lora_path)
    model.eval()

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    stats = {}
    all_results = []

    # Alpaca Prompt Şablonu (Eğitimde kullanılanın aynısı)
    system_instruction = (
        "You are an expert text normalization and error correction AI. "
        "Correct any spelling, grammar, punctuation, and specific entity terminology errors in the text. "
        "Apply standard entity normalization rules (e.g., 'Turkey' to 'Türkiye'). "
        "If the input is already correct, return it exactly as is."
    )
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
"""

    # 3. Analiz Döngüsü
    print(f"🔍 {len(test_data)} örnek Llama 3.1 ile kategori bazlı analiz ediliyor...")
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()
        error_category = str(item.get("error_type", "genel")).upper().strip()

        if error_category not in stats:
            stats[error_category] = {"total": 0, "correct": 0}

        prompt = alpaca_prompt.format(system_instruction, original_input)
        inputs = tokenizer([prompt], return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, use_cache=True, temperature=0.1, do_sample=True)

        decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        predicted = decoded_output.split("### Response:\n")[-1].strip()

        is_correct = (predicted.lower() == ground_truth.lower())

        stats[error_category]["total"] += 1
        if is_correct:
            stats[error_category]["correct"] += 1

        all_results.append({
            "Kategori": error_category,
            "Girdi": original_input,
            "Beklenen": ground_truth,
            "Tahmin": predicted,
            "Durum": "✅ DOĞRU" if is_correct else "❌ YANLIŞ"
        })

    # 4. Raporlama
    analysis_results = []
    for cat, data in stats.items():
        acc = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
        analysis_results.append({
            "Hata Türü": cat,
            "Toplam Örnek": data["total"],
            "Doğru Bilinen": data["correct"],
            "Hatalı/Bozulan": data["total"] - data["correct"],
            "Başarı (%)": round(acc, 2)
        })

    df_summary = pd.DataFrame(analysis_results).sort_values(by="Başarı (%)", ascending=False)
    df_details = pd.DataFrame(all_results)

    with pd.ExcelWriter(report_output) as writer:
        df_summary.to_excel(writer, sheet_name="Özet Performans", index=False)
        df_details.to_excel(writer, sheet_name="Tüm Tahminler", index=False)

    print("\n" + "=" * 65)
    print(f"📈 LLAMA 3.1 MODEL PERFORMANS ÖZETİ")
    print("=" * 65)
    print(df_summary.to_string(index=False))
    print("=" * 65)

if __name__ == "__main__":
    detailed_error_analysis_llama3_local()
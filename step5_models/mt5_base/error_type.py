import json
import torch
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, MT5ForConditionalGeneration


def detailed_error_analysis_mt5_fixed():
    # 1. Klasör ve Dosya Yolları
    current_file_path = Path(__file__).resolve()
    mt5_folder = current_file_path.parent
    reports_dir = mt5_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    data_path = mt5_folder.parent.parent / "step5_models" / "test.json"
    model_path = mt5_folder / "final_mt5_base_model"
    report_output = reports_dir / "mt5_error_type_performance_detailed.xlsx"

    # 2. Cihaz ve Model Kurulumu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 mT5 Detaylı Analiz Başlatıldı (Cihaz: {device.upper()})")

    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = MT5ForConditionalGeneration.from_pretrained(model_path).to(device)
    model.eval()

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # İstatistik Tutucu
    stats = {}

    # 3. Tahmin ve Sınıflandırma Döngüsü
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()

        # Kategori ismini standartlaştır (None/none/NONE farkını ortadan kaldırır)
        error_category = str(item.get("error_type", "genel")).lower().strip()

        if error_category not in stats:
            stats[error_category] = {"total": 0, "correct": 0}

        # Model Tahmini Üretme
        input_text = "gec: " + original_input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=128,
                num_beams=5,
                early_stopping=True  # Üretim tutarlılığı için eklendi
            )

        predicted = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Karşılaştırma Mantığı (Küçük harf duyarsız tam eşleşme)
        is_correct = predicted.lower() == ground_truth.lower()

        stats[error_category]["total"] += 1
        if is_correct:
            stats[error_category]["correct"] += 1

    # 4. Analiz Sonuçlarını Hazırlama
    analysis_results = []
    for cat, data in stats.items():
        acc = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
        analysis_results.append({
            "Hata Türü": cat.upper(),
            "Toplam Örnek (Adet)": data["total"],
            "Doğru Bilinen": data["correct"],
            "Hatalı/Bozulan": data["total"] - data["correct"],
            "Başarı (%)": round(acc, 2)
        })

    # 5. Raporlama ve Kaydetme
    df = pd.DataFrame(analysis_results).sort_values(by="Başarı (%)", ascending=False)
    df.to_excel(report_output, index=False)

    print("\n" + "=" * 60)
    print(f"📈 MODEL PERFORMANS ÖZETİ (Toplam Test: {len(test_data)})")
    print("=" * 60)
    print(df.to_string(index=False))
    print("=" * 60)
    print(f"✅ Detaylı kategori raporu kaydedildi: {report_output}")


if __name__ == "__main__":
    detailed_error_analysis_mt5_fixed()
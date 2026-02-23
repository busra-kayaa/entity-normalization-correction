import json
import torch
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration


def detailed_error_type_analysis():
    # 1. Klasör ve Dosya Yolları
    current_file_path = Path(__file__).resolve()
    t5_base_folder = current_file_path.parent

    # Reports klasörünü oluştur
    reports_dir = t5_base_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Veri ve Model Yolları
    step5_models_folder = t5_base_folder.parent
    data_path = step5_models_folder / "test.json"
    model_path = t5_base_folder / "final_t5_base_model"

    # Çıktı Dosyaları
    report_output = reports_dir / "error_type_performance_detailed.xlsx"
    mismatch_log = reports_dir / "failed_examples_by_type.txt"

    # 2. Modeli Yükle
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🔄 Model yükleniyor: {model_path.name}")
    tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)
    model.eval()

    if not data_path.exists():
        print(f"❌ HATA: {data_path} bulunamadı!")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # 3. Analiz Hazırlığı
    stats = {}
    mismatches = []  # Hataları loglamak için

    print("🔍 Hata türü bazlı performans ölçülüyor...")

    for item in tqdm(test_data):
        original_input = item["input"]
        ground_truth = item["target"].strip()
        error_category = item.get("error_type", "Genel/Karma")

        if error_category not in stats:
            stats[error_category] = {"total": 0, "correct": 0}

        # Model Tahmini
        input_text = "gec: " + original_input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=128, num_beams=5)

        predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Başarı Kontrolü
        is_correct = predicted_text.lower() == ground_truth.lower()

        stats[error_category]["total"] += 1
        if is_correct:
            stats[error_category]["correct"] += 1
        else:
            # Hatalı örnekleri daha sonra incelemek için listeye ekle
            mismatches.append({
                "Tür": error_category,
                "Girdi": original_input,
                "Hedef": ground_truth,
                "Tahmin": predicted_text
            })

    # 4. İstatistikleri Tabloya Dönüştür
    analysis_results = []
    for cat, data in stats.items():
        acc = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
        analysis_results.append({
            "Hata Türü": cat,
            "Toplam Örnek": data["total"],
            "Doğru Tahmin": data["correct"],
            "Başarı Oranı (%)": round(acc, 2)
        })

    df_analysis = pd.DataFrame(analysis_results).sort_values(by="Başarı Oranı (%)", ascending=False)

    # 5. Dosyaları Kaydet
    # Excel Raporu
    df_analysis.to_excel(report_output, index=False)

    # Hatalı Örnekler Logu (TXT)
    with open(mismatch_log, "w", encoding="utf-8") as f:
        f.write("=== HATALI TAHMİN ÖRNEKLERİ ===\n\n")
        for m in mismatches:
            f.write(f"Tür: {m['Tür']}\nIn : {m['Girdi']}\nGT : {m['Hedef']}\nPR : {m['Tahmin']}\n{'-' * 30}\n")

    print("\n📊 HATA TÜRÜ BAZLI PERFORMANS TABLOSU")
    print("-" * 50)
    print(df_analysis.to_string(index=False))
    print("-" * 50)
    print(f"💾 Detaylı Excel: {report_output}")
    print(f"💾 Hatalı Örnek Logu: {mismatch_log}")


if __name__ == "__main__":
    detailed_error_type_analysis()
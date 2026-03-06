import json
import torch
import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from google.colab import files


def detailed_error_analysis_mbart_colab():
    # 1. Colab Klasör ve Dosya Yolları
    # Eğitim bittikten sonra modelin kaydedildiği klasör adı:
    model_path = "/content/final_mbart_model"
    data_path = "/content/test.json"

    reports_dir = Path("/content/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_output = reports_dir / "mbart_error_type_performance_detailed.xlsx"

    # 2. Cihaz ve Model Kurulumu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 mBART Detaylı Analiz Başlatıldı (Cihaz: {device.upper()})")

    if not os.path.exists(model_path):
        print(f"❌ HATA: Model bulunamadı! Yol: {model_path}")
        return

    if not os.path.exists(data_path):
        print(f"❌ HATA: test.json bulunamadı! Lütfen dosyayı Colab'a yükle.")
        return

    # mBART için Auto sınıfları kusursuz çalışır
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)
    model.eval()

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # İstatistik Tutucu
    stats = {}
    all_results = []

    # 3. Tahmin ve Sınıflandırma Döngüsü
    print(f"🔍 {len(test_data)} örnek mBART ile kategori bazlı analiz ediliyor...")
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()

        # Kategori ismini standartlaştır
        error_category = str(item.get("error_type", "genel")).upper().strip()

        if error_category not in stats:
            stats[error_category] = {"total": 0, "correct": 0}

        # Girdiyi saf haliyle veriyoruz (Eğitimdeki gibi)
        input_text = original_input

        inputs = tokenizer(input_text, return_tensors="pt", max_length=256, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=256,
                num_beams=5,
                early_stopping=True
            )

        predicted = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Karşılaştırma Mantığı (Küçük harf duyarsız tam eşleşme)
        is_correct = (predicted.lower() == ground_truth.lower())

        stats[error_category]["total"] += 1
        if is_correct:
            stats[error_category]["correct"] += 1

        # Detaylı rapor için tüm tahminleri kaydediyoruz
        all_results.append({
            "Kategori": error_category,
            "Girdi": original_input,
            "Beklenen": ground_truth,
            "Tahmin": predicted,
            "Durum": "✅ DOĞRU" if is_correct else "❌ YANLIŞ"
        })

    # 4. Analiz Sonuçlarını Hazırlama
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

    # 5. Raporlama ve İndirme İşlemi
    df_summary = pd.DataFrame(analysis_results).sort_values(by="Başarı (%)", ascending=False)
    df_details = pd.DataFrame(all_results)

    with pd.ExcelWriter(report_output) as writer:
        df_summary.to_excel(writer, sheet_name="Özet Performans", index=False)
        df_details.to_excel(writer, sheet_name="Tüm Tahminler", index=False)

    print("\n" + "=" * 65)
    print(f"📈 mBART MODEL PERFORMANS ÖZETİ (Toplam Test: {len(test_data)})")
    print("=" * 65)
    print(df_summary.to_string(index=False))
    print("=" * 65)

    print(f"✅ Detaylı kategori raporu oluşturuldu: {report_output}")
    print("⬇️ Excel dosyası bilgisayarınıza indiriliyor...")
    # files.download(str(report_output))


if __name__ == "__main__":
    detailed_error_analysis_mbart_colab()
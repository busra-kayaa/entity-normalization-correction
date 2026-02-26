import json
import torch
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration


def detailed_error_analysis_t5_base_final():
    # 1. Klasör ve Dosya Yolları
    current_file_path = Path(__file__).resolve()
    t5_folder = current_file_path.parent
    reports_dir = t5_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Veri ve Model Yolları
    data_path = t5_folder.parent.parent / "step5_models" / "test.json"
    model_path = (t5_folder / "final_t5_base_model").as_posix()

    report_output = reports_dir / "t5_base_error_type_performance_detailed.xlsx"
    failed_log_output = reports_dir / "t5_base_failed_examples.txt"

    # 2. Cihaz ve Model Kurulumu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 T5-Base Detaylı Analiz Başlatıldı (Cihaz: {device.upper()})")

    # T5 modelleri için özel T5Tokenizer kullanımı daha stabildir
    tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)
    model.eval()

    if not data_path.exists():
        print(f"❌ HATA: {data_path} bulunamadı!")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # İstatistik ve Log Tutucular
    stats = {}
    failed_examples = []

    # 3. Tahmin ve Sınıflandırma Döngüsü
    print(f"🧪 {len(test_data)} örnek kategorilere göre inceleniyor...")
    for item in tqdm(test_data):
        # Tutarlılık için giriş ve hedefi temizle
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()

        # Kategori ismini standartlaştır (None/none karmaşasını bitirir)
        error_category = str(item.get("error_type", "genel")).lower().strip()

        if error_category not in stats:
            stats[error_category] = {"total": 0, "correct": 0}

        # Model Tahmini Üretme (Gelişmiş Parametreler)
        input_text = "gec: " + original_input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=128,
                num_beams=5,
                early_stopping=True  # Üretim tutarlılığı için çok kritik
            )

        predicted = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Karşılaştırma Mantığı (Accuracy standardı: Küçük harf duyarsız)
        is_correct = predicted.lower() == ground_truth.lower()

        stats[error_category]["total"] += 1
        if is_correct:
            stats[error_category]["correct"] += 1
        else:
            # Hatalı/Over-Correction örneklerini kaydet
            failed_examples.append(
                f"Tür: {error_category.upper()}\nIn : {original_input}\nGT : {ground_truth}\nPR : {predicted}\n{'-' * 40}\n"
            )

    # 4. Analiz Sonuçlarını Hazırlama
    analysis_results = []
    for cat, data in stats.items():
        acc = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
        analysis_results.append({
            "Hata Türü": cat.upper(),
            "Toplam Örnek (Adet)": data["total"],
            "Doğru Bilinen": data["correct"],
            "Hatalı/Bozulan (OC)": data["total"] - data["correct"],
            "Başarı (%)": round(acc, 2)
        })

    # 5. Raporlama ve Kaydetme
    df = pd.DataFrame(analysis_results).sort_values(by="Başarı (%)", ascending=False)
    df.to_excel(report_output, index=False)

    # Hatalı Örnekler Logu (TXT)
    with open(failed_log_output, "w", encoding="utf-8") as f:
        f.write(f"=== T5-BASE HATALI TAHMİN VE OC LOGLARI ({len(failed_examples)} Adet) ===\n\n")
        f.writelines(failed_examples)

    print("\n" + "=" * 60)
    print(f"📊 T5-BASE PERFORMANS ÖZETİ")
    print("=" * 60)
    print(df.to_string(index=False))
    print("=" * 60)
    print(f"✅ Detaylı Excel: {report_output}")
    print(f"✅ Hatalı Örnek Logu: {failed_log_output}")


if __name__ == "__main__":
    detailed_error_analysis_t5_base_final()
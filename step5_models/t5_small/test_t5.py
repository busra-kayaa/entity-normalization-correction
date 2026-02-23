import json
import torch
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.metrics import precision_recall_fscore_support
import datetime


def evaluate_model_small():
    # 1. Klasör ve Dosya Yolları
    current_file_path = Path(__file__).resolve()
    t5_small_folder = current_file_path.parent

    # Reports klasörünü oluştur (Yoksa)
    reports_dir = t5_small_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Veri ve Model Yolları
    step5_models_folder = t5_small_folder.parent
    data_path = step5_models_folder / "test.json"
    model_path = t5_small_folder / "final_model"

    # Çıktı Dosyaları (reports klasörü içine)
    excel_output = reports_dir / "small_final_test_results.xlsx"
    text_report = reports_dir / "small_evaluation_report.txt"

    # 2. Cihaz Ayarı
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 T5-Small Genel Testi başlatıldı (Cihaz: {device.upper()})")

    # 3. Model ve Veri Yükleme
    if not data_path.exists():
        print(f"❌ HATA: {data_path} bulunamadı!")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)
    model.eval()

    all_results = []
    y_true = []
    y_pred = []

    print(f"🧪 {len(test_data)} örnek üzerinde model performansı ölçülüyor...")

    # 4. Tahmin Döngüsü
    for item in tqdm(test_data):
        original_input = item["input"]
        ground_truth = item["target"]

        input_text = "gec: " + original_input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=128,
                num_beams=5,
                early_stopping=True
            )

        predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        y_true.append(ground_truth.strip().lower())
        y_pred.append(predicted_text.lower())

        is_match = predicted_text.lower() == ground_truth.lower().strip()

        all_results.append({
            "Bozuk Girdi": original_input,
            "Gerçek Doğru": ground_truth,
            "Model Tahmini": predicted_text,
            "Durum": "BAŞARILI" if is_match else "HATALI"
        })

    # 5. Metrik Hesaplama
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', zero_division=0
    )
    correct_count = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    accuracy = (correct_count / len(y_true)) * 100

    # 6. Metin Raporu Oluşturma
    report_content = f"""
==================================================
      ENTITY NORMALIZATION EVALUATION (T5-SMALL)
==================================================
Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: T5-Small (Fine-tuned)
Test Verisi: {data_path.name}
Toplam Örnek Sayısı: {len(test_data)}

---------------- METRİKLER -----------------------
🎯 Accuracy (Tam Eşleşme): %{accuracy:.2f}
✨ Precision: {precision:.4f}
📈 Recall: {recall:.4f}
🏆 F1-Score: {f1:.4f}

---------------- ÖZET ----------------------------
✅ Başarılı Düzenleme: {correct_count}
❌ Hatalı Düzenleme  : {len(test_data) - correct_count}
==================================================
"""
    with open(text_report, "w", encoding="utf-8") as f:
        f.write(report_content)

    # 7. Excel Raporu Oluşturma
    with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
        df_details = pd.DataFrame(all_results)
        df_details.to_excel(writer, sheet_name="Test Detayları", index=False)

        metrics_summary = {
            "Metrik": ["Accuracy", "Precision", "Recall", "F1-Score", "Başarılı", "Hatalı"],
            "Değer": [f"%{accuracy:.2f}", precision, recall, f1, correct_count, len(test_data) - correct_count]
        }
        pd.DataFrame(metrics_summary).to_excel(writer, sheet_name="Genel Rapor", index=False)

    print(report_content)
    print(f"💾 Excel Raporu kaydedildi: {excel_output}")
    print(f"📄 Metin Raporu kaydedildi: {text_report}")


if __name__ == "__main__":
    evaluate_model_small()
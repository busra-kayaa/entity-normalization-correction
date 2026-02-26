import json
import torch
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.metrics import precision_recall_fscore_support
import datetime
import nltk
from nltk.translate.gleu_score import sentence_gleu
from jiwer import cer

# NLTK bileşenlerini hazırla
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def evaluate_t5_base_advanced():
    # 1. Klasör ve Dosya Yolları
    current_file_path = Path(__file__).resolve()
    t5_folder = current_file_path.parent
    reports_dir = t5_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    project_root = t5_folder.parent.parent
    data_path = project_root / "step5_models" / "test.json"
    model_path = (t5_folder / "final_t5_base_model").as_posix()

    excel_output = reports_dir / "t5_base_advanced_results.xlsx"
    text_report = reports_dir / "t5_base_final_report.txt"

    # 2. Cihaz ve Model Kurulumu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 T5-Base Gelişmiş Test Başlatıldı (Cihaz: {device.upper()})")

    # T5Tokenizer ve Model yükleme
    tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)
    model.eval()

    if not data_path.exists():
        print(f"❌ HATA: Test verisi bulunamadı! {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # Veri Saklama ve Sayaçlar
    all_results = []
    y_true, y_pred = [], []
    cer_scores, gleu_scores = [], []

    # Over-Correction (OC) Analizi için Sayaçlar
    oc_count = 0
    none_total = 0
    none_correct = 0

    # 3. Tahmin ve Analiz Döngüsü
    print(f"🧪 {len(test_data)} örnek üzerinde detaylı metrikler hesaplanıyor...")
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()
        error_type = str(item.get("error_type", "genel")).lower().strip()

        # Model Tahmini
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

        # Standart Metrikler İçin Kayıt (Küçük harf duyarsız)
        y_true.append(ground_truth.lower())
        y_pred.append(predicted_text.lower())

        # Gelişmiş Metrik 1: CER (Karakter Hata Oranı)
        cer_val = cer(ground_truth.lower(), predicted_text.lower())
        cer_scores.append(cer_val)

        # Gelişmiş Metrik 2: GLEU (Gramer/Akış Skoru)
        ref_tokens = nltk.word_tokenize(ground_truth.lower())
        pred_tokens = nltk.word_tokenize(predicted_text.lower())
        gleu_val = sentence_gleu([ref_tokens], pred_tokens)
        gleu_scores.append(gleu_val)

        # Seçici Müdahale (Over-Correction) Analizi
        is_match = predicted_text.lower() == ground_truth.lower()
        if error_type == "none":
            none_total += 1
            if is_match:
                none_correct += 1
            else:
                oc_count += 1

        all_results.append({
            "Hata Türü": error_type.upper(),
            "Girdi": original_input,
            "Hedef": ground_truth,
            "Tahmin": predicted_text,
            "Durum": "BAŞARILI" if is_match else "HATALI",
            "CER": round(cer_val, 4),
            "GLEU": round(gleu_val, 4)
        })

    # 4. Final Hesaplamalar
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    accuracy = (sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)) * 100
    avg_cer = sum(cer_scores) / len(cer_scores)
    avg_gleu = sum(gleu_scores) / len(gleu_scores)
    oc_rate = (oc_count / none_total * 100) if none_total > 0 else 0

    # 5. Raporlama
    report_content = f"""
==================================================
      ADVANCED EVALUATION REPORT (T5-BASE)
==================================================
Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: T5-Base (Normalizer)
Toplam Örnek Sayısı: {len(test_data)}

---------------- TEMEL METRİKLER -----------------
🎯 Accuracy (Tam Eşleşme): %{accuracy:.2f}
✨ Precision: {precision:.4f}
📈 Recall: {recall:.4f}
🏆 F1-Score: {f1:.4f}

---------------- GELİŞMİŞ METRİKLER --------------
📉 Avg CER (Karakter Hata Oranı): {avg_cer:.4f}
🧩 Avg GLEU (Gramer Benzerliği): {avg_gleu:.4f}
⚠️ Over-Correction Rate: %{oc_rate:.2f}

---------------- DETAYLI SEÇİCİ MÜDAHALE ----------
🔍 "None" (Zaten Doğru Olan) Analizi:
- Toplam 'None' Verisi : {none_total}
- Doğru Korunan (TP)   : {none_correct}
- Gereksiz Düzeltilen (OC): {oc_count}

💡 Not: Modelin doğruyu bozmadan geçme başarısı %{(none_correct / none_total * 100) if none_total > 0 else 0:.2f} seviyesindedir.
==================================================
"""
    # Dosyaya Kaydet
    with open(text_report, "w", encoding="utf-8") as f:
        f.write(report_content)
    pd.DataFrame(all_results).to_excel(excel_output, index=False)

    print(report_content)
    print(f"💾 Detaylı Raporlar '{reports_dir}' klasörüne kaydedildi.")


if __name__ == "__main__":
    evaluate_t5_base_advanced()
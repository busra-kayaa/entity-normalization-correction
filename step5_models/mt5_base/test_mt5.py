import json
import torch
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, MT5ForConditionalGeneration
from sklearn.metrics import precision_recall_fscore_support
import datetime
import nltk
from nltk.translate.gleu_score import sentence_gleu
from jiwer import cer

# NLTK gereksinimlerini kontrol et ve indir
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def evaluate_mt5_model():
    # 1. Klasör ve Dosya Yolları
    current_file_path = Path(__file__).resolve()
    model_folder = current_file_path.parent
    reports_dir = model_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Proje yapına göre veri ve model yolları
    project_root = model_folder.parent.parent
    data_path = project_root / "step5_models" / "test.json"
    model_path = model_folder / "final_mt5_base_model"

    excel_output = reports_dir / "mt5_test_results_detailed.xlsx"
    text_report = reports_dir / "mt5_final_evaluation_report.txt"

    # 2. Cihaz Ayarı
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 mT5-Base Testi başlatıldı (Cihaz: {device.upper()})")

    # 3. Model ve Tokenizer Yükleme
    # Proje Analizi: Çok dilli karakter yapısı için AutoTokenizer kullanıyoruz [cite: 60]
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = MT5ForConditionalGeneration.from_pretrained(model_path).to(device)
    model.eval()

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    all_results = []
    y_true, y_pred = [], []
    cer_scores, gleu_scores = [], []

    # --- KRİTİK SAYAÇLAR (Senkronizasyon İçin) ---
    oc_count = 0  # Over-Correction (Doğruyu bozma)
    none_total_count = 0  # Toplam "none" etiketli veri
    none_correct_count = 0  # "none" olup modelin doğru bıraktığı

    # 4. Tahmin Döngüsü
    print(f"🧪 {len(test_data)} örnek üzerinde mT5 performansı ölçülüyor...")
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()
        error_type = str(item.get("error_type", "genel")).lower().strip()

        # Giriş metnine prefix ekle [cite: 7]
        input_text = "gec: " + original_input
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=128,
                num_beams=5,
                early_stopping=True  # Üretim tutarlılığı için sabitlendi
            )

        predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Metrikler için küçük harf standardı (Accuracy senkronizasyonu)
        y_true.append(ground_truth.lower())
        y_pred.append(predicted_text.lower())

        # Karakter ve Gramer Metrikleri
        cer_val = cer(ground_truth.lower(), predicted_text.lower())
        cer_scores.append(cer_val)

        ref_tokens = nltk.word_tokenize(ground_truth.lower())
        pred_tokens = nltk.word_tokenize(predicted_text.lower())
        gleu_val = sentence_gleu([ref_tokens], pred_tokens)
        gleu_scores.append(gleu_val)

        # --- SEÇİCİ MÜDAHALE VE OC ANALİZİ [cite: 49, 56-58] ---
        is_match = predicted_text.lower() == ground_truth.lower()

        if error_type == "none":
            none_total_count += 1
            if is_match:
                none_correct_count += 1
            else:
                oc_count += 1

        all_results.append({
            "Hata Türü": error_type,
            "Girdi": original_input,
            "Hedef": ground_truth,
            "Model Tahmini": predicted_text,
            "Durum": "BAŞARILI" if is_match else "HATALI",
            "CER": cer_val,
            "GLEU": gleu_val
        })

    # 5. Metrik Hesaplama
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    accuracy = (sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)) * 100
    avg_cer = sum(cer_scores) / len(cer_scores)
    avg_gleu = sum(gleu_scores) / len(gleu_scores)
    oc_rate = (oc_count / none_total_count * 100) if none_total_count > 0 else 0

    # 6. Raporlama
    report_content = f"""
==================================================
      ADVANCED EVALUATION REPORT (mT5-BASE)
==================================================
Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: mT5-Base (Multilingual)
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

---------------- DETAYLI ANALİZ ------------------
🔍 "None" (Zaten Doğru) Analizi:
- Toplam None Sayısı : {none_total_count}
- Doğru Korunan (TP) : {none_correct_count}
- Gereksiz Düzeltilen (FP/OC): {oc_count}

💡 Not: Seçici müdahale başarısı %{(none_correct_count / none_total_count * 100):.2f} seviyesindedir.
==================================================
"""
    with open(text_report, "w", encoding="utf-8") as f:
        f.write(report_content)

    # Excel Çıktısı
    pd.DataFrame(all_results).to_excel(excel_output, index=False)

    print(report_content)
    print(f"💾 Detaylı Excel ve Metin raporu '{reports_dir}' klasörüne kaydedildi.")


if __name__ == "__main__":
    evaluate_mt5_model()
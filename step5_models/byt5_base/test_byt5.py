import json
import torch
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sklearn.metrics import precision_recall_fscore_support
import datetime
import nltk
from nltk.translate.gleu_score import sentence_gleu
from jiwer import cer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def test_byt5_advanced_json():
    model_path = "./final_byt5_model"  # Colab'daysan /content/final_byt5_model
    data_path = "./test.json"  # Colab'daysan /content/test.json

    reports_dir = Path("./reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    excel_output = reports_dir / "byt5_advanced_results.xlsx"
    text_report = reports_dir / "byt5_advanced_report.txt"

    if not os.path.exists(model_path):
        print(f"❌ HATA: Model bulunamadı! Yol: {model_path}")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔄 ByT5 Modeli ve Tokenizer Yükleniyor... (Donanım: {str(device).upper()})")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)
    model.eval()

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    all_results = []
    y_true, y_pred = [], []
    cer_scores, gleu_scores = [], []
    oc_count, none_total, none_correct = 0, 0, 0

    print(f"🧪 {len(test_data)} örnek üzerinde CER, GLEU ve F1 hesaplanıyor...")
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()
        error_type = str(item.get("error_type", "genel")).lower().strip()

        # ByT5 yutma koruması
        padded_input = " " + original_input
        inputs = tokenizer(padded_input, return_tensors="pt", max_length=256, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=256, num_beams=5, early_stopping=True)

        predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        y_true.append(ground_truth.lower())
        y_pred.append(predicted_text.lower())

        cer_val = cer(ground_truth.lower(), predicted_text.lower())
        cer_scores.append(cer_val)

        ref_tokens = nltk.word_tokenize(ground_truth.lower())
        pred_tokens = nltk.word_tokenize(predicted_text.lower())
        gleu_val = sentence_gleu([ref_tokens], pred_tokens)
        gleu_scores.append(gleu_val)

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

    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    accuracy = (sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)) * 100
    avg_cer = sum(cer_scores) / len(cer_scores) if cer_scores else 0
    avg_gleu = sum(gleu_scores) / len(gleu_scores) if gleu_scores else 0
    oc_rate = (oc_count / none_total * 100) if none_total > 0 else 0

    report_content = f"""
==================================================
      GELİŞMİŞ METRİK RAPORU (ByT5)
==================================================
Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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

---------------- SEÇİCİ MÜDAHALE (NONE) ----------
- Toplam 'None' Verisi : {none_total}
- Doğru Korunan (TP)   : {none_correct}
- Gereksiz Düzeltilen  : {oc_count}
==================================================
"""
    with open(text_report, "w", encoding="utf-8") as f:
        f.write(report_content)
    pd.DataFrame(all_results).to_excel(excel_output, index=False)

    print(report_content)
    print(f"✅ ByT5 Gelişmiş test tamamlandı. Dosyalar kaydedildi.")


if __name__ == "__main__":
    test_byt5_advanced_json()
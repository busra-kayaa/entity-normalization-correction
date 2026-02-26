import torch
import os
import pandas as pd
from transformers import AutoTokenizer, MT5ForConditionalGeneration
from pathlib import Path
from datetime import datetime


def test_mt5_categorized():
    # 1. Klasör ve Yol Ayarları
    current_file_path = Path(__file__).resolve()
    mt5_folder = current_file_path.parent
    reports_dir = mt5_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    model_path = mt5_folder / "final_mt5_base_model"
    output_excel = reports_dir / "mt5_manual_test_results.xlsx"
    output_text = reports_dir / "mt5_manual_test_report.txt"

    if not model_path.exists():
        print(f"❌ Hata: Model yolu bulunamadı! {model_path}")
        return

    print("🔄 mT5-Base Modeli ve Tokenizer yükleniyor...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = MT5ForConditionalGeneration.from_pretrained(model_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()

    # 2. Kategori Bilgisi Eklenmiş Test Örnekleri
    test_cases = [
        ("Turkiye is a bridge between Europe and Asia.", "Türkiye is a bridge between Europe and Asia.", "deascii"),
        ("TURKIYE is now the official name.", "TÜRKİYE is now the official name.", "deascii"),  # Büyük harf testi
        ("We are going to Istanbul for the summit.", "We are going to İstanbul for the summit.", "deascii"),
        # i -> İ karmaşası
        ("The weather in Izmir is very hot.", "The weather in İzmir is very hot.", "deascii"),
        ("Besiktas won the match last night.", "Beşiktaş won the match last night.", "deascii"),
        ("President Erdogan will visit the site.", "President Erdoğan will visit the site.", "deascii"),

        # --- 2) TERMINOLOGY (Uluslararası İsim Değişimleri)
        ("The flight was from London to Turkey.", "The flight was from London to Türkiye.", "terminology"),
        ("The government of Burma is under pressure.", "The government of Myanmar is under pressure.", "terminology"),
        ("Swaziland has changed its name to Eswatini.", "Eswatini has changed its name to Eswatini.", "terminology"),

        # --- 3) TYPOGRAPHIC (Harf Dizilimi ve Yazım Hataları)
        ("President Erdğan will speak soon.", "President Erdoğan will speak soon.", "omission"),  # Erdoğan -> Erdğan
        ("The Prsident made a choice.", "The President made a choice.", "omission"),  # President -> Prsident
        ("The poliitcal situation is unstable.", "The political situation is unstable.", "insertion"),
        # Political -> Poliitcal
        ("Irsaeli officials reported the news.", "Israeli officials reported the news.", "transposition"),
        # Israeli -> Irsaeli
        ("Sülyeman visited the office.", "Süleyman visited the office.", "transposition"),  # Süleyman -> Sülyeman
        ("The Taliban is in control of Takiban.", "The Taliban is in control of Taliban.", "substitution"),
        # Taliban -> Takiban (k->l)
        ("Ankara and Abkara are different.", "Ankara and Ankara are different.", "substitution"),  # Ankara -> Abkara

        # --- 4) SPACE/PUNCTUATION (Birleşik Yazım)
        ("NewYork is the city that never sleeps.", "New York is the city that never sleeps.", "space"),
        ("AbdullahGul was the former president.", "Abdullah Gül was the former president.", "space"),

        # --- 5) COMMON (Genel İngilizce Yazım Hataları)
        ("I did not recieve your email.", "I did not receive your email.", "common"),
        ("The goverment announced a new policy.", "The government announced a new policy.", "common"),
        ("The enviroment is our priority.", "The environment is our priority.", "common"),

        # --- 6) IDENTITY & AMBIGUITY (Over-Correction Kısıtları)
        ("The month of May is beautiful.", "The month of May is beautiful.", "none"),  # Belirsizlik: May (ay ismi)
        ("Bill is a common name in the US.", "Bill is a common name in the US.", "none"),
        # Belirsizlik: Bill (isim vs fatura)
        ("The weather in London is rainy today.", "The weather in London is rainy today.", "none"),  # Doğru cümle
        ("This is a correctly written English sentence.", "This is a correctly written English sentence.", "none")
    ]

    results_list = []
    category_stats = {}

    print(f"🧪 {len(test_cases)} manuel senaryo kategorilere göre test ediliyor...")

    for input_raw, target, category in test_cases:
        if category not in category_stats:
            category_stats[category] = {"total": 0, "correct": 0}

        inputs = tokenizer("gec: " + input_raw, return_tensors="pt", max_length=128, truncation=True).to(device)
        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=128, num_beams=5, early_stopping=True)

        predicted = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        is_correct = predicted.lower() == target.lower().strip()

        # İstatistikleri Güncelle
        category_stats[category]["total"] += 1
        if is_correct:
            category_stats[category]["correct"] += 1

        results_list.append({
            "Kategori": category,
            "Girdi": input_raw,
            "Hedef": target,
            "Tahmin": predicted,
            "Durum": "✅" if is_correct else "❌"
        })

    # 3. Kategori Bazlı Özet Raporu Oluşturma
    summary_list = []
    for cat, stats in category_stats.items():
        acc = (stats["correct"] / stats["total"]) * 100
        summary_list.append({
            "Kategori": cat,
            "Toplam": stats["total"],
            "Doğru": stats["correct"],
            "Başarı (%)": f"%{acc:.2f}"
        })

    # 4. Kayıt ve Çıktı İşlemleri
    df_results = pd.DataFrame(results_list)
    df_summary = pd.DataFrame(summary_list)

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name="Test Detayları", index=False)
        df_summary.to_excel(writer, sheet_name="Kategori Özeti", index=False)

    total_accuracy = (sum(s["correct"] for s in category_stats.values()) / len(test_cases)) * 100

    report_header = f"""
==================================================
      mT5 MANUEL TEST KATEGORİ RAPORU
==================================================
Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Genel Accuracy: %{total_accuracy:.2f}

---------------- KATEGORİ ÖZETİ ------------------
{df_summary.to_string(index=False)}
==================================================
"""
    with open(output_text, "w", encoding="utf-8") as f:
        f.write(report_header + "\n\nDETAYLI TEST LİSTESİ:\n" + df_results.to_string(index=False))

    print(report_header)
    print(f"✅ Raporlar 'reports' klasörüne kaydedildi.")


if __name__ == "__main__":
    test_mt5_categorized()
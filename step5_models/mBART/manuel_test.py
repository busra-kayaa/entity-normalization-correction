import torch
import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
from datetime import datetime


def test_mbart_manual_categorized():
    # 1. Klasör ve Yol Ayarları
    current_file_path = Path(__file__).resolve()
    mbart_folder = current_file_path.parent

    # Reports klasörünü oluştur
    reports_dir = mbart_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Model Yolu (Windows hatalarını önlemek için as_posix kullanımı)
    # Kendi bilgisayarındaki mbart modelinin klasör adını buraya yaz (örn: final_mbart_model)
    model_path = (mbart_folder / "final_mbart_model").as_posix()

    # Çıktı Dosya Yolları
    output_excel = reports_dir / "mbart_manual_test_results.xlsx"
    output_text = reports_dir / "mbart_manual_test_report.txt"

    if not os.path.exists(model_path):
        print(f"❌ Hata: mBART Model yolu bulunamadı! Lütfen yolu kontrol et: {model_path}")
        return

    print("🔄 mBART Modeli ve Tokenizer yükleniyor...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"💻 Cihaz: {str(device).upper()}")
    model.to(device).eval()

    # 2. Kategorize Edilmiş Test Senaryoları
    test_cases = [
        # --- 1) DE-ASCII (Karakter Dönüşümü)
        ("Turkiye is a bridge between Europe and Asia.", "Türkiye is a bridge between Europe and Asia.", "deascii"),
        ("TURKIYE is now the official name.", "TÜRKİYE is now the official name.", "deascii"),
        ("We are going to Istanbul for the summit.", "We are going to İstanbul for the summit.", "deascii"),
        ("The weather in Izmir is very hot.", "The weather in İzmir is very hot.", "deascii"),
        ("Besiktas won the match last night.", "Beşiktaş won the match last night.", "deascii"),
        ("President Erdogan will visit the site.", "President Erdoğan will visit the site.", "deascii"),

        # --- 2) TERMINOLOGY (İsim Değişimleri)
        ("The flight was from London to Turkey.", "The flight was from London to Türkiye.", "terminology"),
        ("The government of Burma is under pressure.", "The government of Myanmar is under pressure.", "terminology"),
        ("Swaziland has changed its name to Eswatini.", "Eswatini has changed its name to Eswatini.", "terminology"),

        # --- 3) TYPOGRAPHIC (Yazım Hataları)
        ("President Erdğan will speak soon.", "President Erdoğan will speak soon.", "omission"),
        ("The Prsident made a choice.", "The President made a choice.", "omission"),
        ("The poliitcal situation is unstable.", "The political situation is unstable.", "insertion"),
        ("Irsaeli officials reported the news.", "Israeli officials reported the news.", "transposition"),
        ("Sülyeman visited the office.", "Süleyman visited the office.", "transposition"),
        ("The Taliban is in control of Takiban.", "The Taliban is in control of Taliban.", "substitution"),
        ("Ankara and Abkara are different.", "Ankara and Ankara are different.", "substitution"),

        # --- 4) SPACE (Birleşik Yazım)
        ("NewYork is the city that never sleeps.", "New York is the city that never sleeps.", "space"),
        ("AbdullahGul was the former president.", "Abdullah Gül was the former president.", "space"),

        # --- 5) COMMON (Genel İngilizce Hataları)
        ("I did not recieve your email.", "I did not receive your email.", "common"),
        ("The goverment announced a new policy.", "The government announced a new policy.", "common"),
        ("The enviroment is our priority.", "The environment is our priority.", "common"),

        # --- 6) NONE (Identity / Over-Correction Testi)
        ("The month of May is beautiful.", "The month of May is beautiful.", "none"),
        ("Bill is a common name in the US.", "Bill is a common name in the US.", "none"),
        ("The weather in London is rainy today.", "The weather in London is rainy today.", "none"),
        ("This is a correctly written English sentence.", "This is a correctly written English sentence.", "none")
    ]

    results_list = []
    category_stats = {}

    print(f"\n🧪 {len(test_cases)} manuel senaryo mBART ile test ediliyor...\n" + "=" * 80)

    for input_raw, target, category in test_cases:
        if category not in category_stats:
            category_stats[category] = {"total": 0, "correct": 0}

        # DİKKAT: mBART eğitiminde "gec:" YOK. Girdiyi saf veriyoruz.
        input_text = input_raw.strip()

        inputs = tokenizer(input_text, return_tensors="pt", max_length=256, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=256,
                num_beams=5,
                early_stopping=True
            )

        predicted = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        is_correct = predicted.lower() == target.lower().strip()

        # İstatistikleri Güncelle
        category_stats[category]["total"] += 1
        if is_correct:
            category_stats[category]["correct"] += 1

        results_list.append({
            "Kategori": category.upper(),
            "Girdi": input_raw,
            "Beklenen": target,
            "Tahmin": predicted,
            "Durum": "✅ DOĞRU" if is_correct else "❌ YANLIŞ"
        })

        print(f"[{category.upper()}] Girdi: {input_raw}")
        print(f"Tahmin: {predicted} {'✅' if is_correct else '❌'}")
        print("-" * 80)

    # 3. Özet Raporu Oluşturma
    summary_list = []
    for cat, stats in category_stats.items():
        acc = (stats["correct"] / stats["total"]) * 100
        summary_list.append({
            "Hata Türü": cat.upper(),
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

    total_accuracy = (df_summary["Doğru"].sum() / df_summary["Toplam"].sum()) * 100
    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report_header = f"""
==================================================
      mBART MANUEL TEST KATEGORİ RAPORU
==================================================
Tarih: {report_time}
Genel Accuracy: %{total_accuracy:.2f}

---------------- KATEGORİ ÖZETİ ------------------
{df_summary.to_string(index=False)}
==================================================
"""
    with open(output_text, "w", encoding="utf-8") as f:
        f.write(report_header + "\n\nDETAYLI TEST LİSTESİ:\n" + df_results.to_string(index=False))

    print(report_header)
    print(f"✅ Test tamamlandı. Raporlar kaydedildi: {reports_dir}")


if __name__ == "__main__":
    test_mbart_manual_categorized()
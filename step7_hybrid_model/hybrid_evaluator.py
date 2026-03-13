import pandas as pd
from hybrid_normalizer import HybridPipeline

# Llama'nın tek başına tökezlediği o meşhur 14 test cümlemiz!
test_data = [
    {"kategori": "DEASCII", "girdi": "Turkiye is a bridge between Europe and Asia.",
     "hedef": "Türkiye is a bridge between Europe and Asia."},
    {"kategori": "DEASCII", "girdi": "TURKIYE is now the official name.", "hedef": "Türkiye is now the official name."},
    {"kategori": "DEASCII", "girdi": "We are going to Istanbul for the summit.",
     "hedef": "We are going to İstanbul for the summit."},  # Llama bilememişti!
    {"kategori": "TERMINOLOGY", "girdi": "The flight was from London to Turkey.",
     "hedef": "The flight was from London to Türkiye."},
    {"kategori": "TERMINOLOGY", "girdi": "The government of Burma is under pressure.",
     "hedef": "The government of Myanmar is under pressure."},  # Llama bilememişti!
    {"kategori": "TERMINOLOGY", "girdi": "Swaziland has changed its name to Eswatini.",
     "hedef": "Eswatini has changed its name to Eswatini."},  # Llama bilememişti!
    {"kategori": "OMISSION", "girdi": "President Erdğan will speak soon.",
     "hedef": "President Erdoğan will speak soon."},
    {"kategori": "OMISSION", "girdi": "The Prsident made a choice.", "hedef": "The President made a choice."},
    {"kategori": "INSERTION", "girdi": "The poliitcal situation is unstable.",
     "hedef": "The political situation is unstable."},
    {"kategori": "TRANSPOSITION", "girdi": "Irsaeli officials reported the news.",
     "hedef": "Israeli officials reported the news."},
    {"kategori": "SPACE", "girdi": "NewYork is the city that never sleeps.",
     "hedef": "New York is the city that never sleeps."},
    {"kategori": "COMMON", "girdi": "The goverment announced a new policy.",
     "hedef": "The government announced a new policy."},
    {"kategori": "NONE", "girdi": "The month of May is beautiful.", "hedef": "The month of May is beautiful."},
    {"kategori": "NONE", "girdi": "This is a correctly written English sentence.",
     "hedef": "This is a correctly written English sentence."}
]

if __name__ == "__main__":
    pipeline = HybridPipeline()
    results = []
    dogru_sayisi = 0

    print("\n🚀 Hibrit Sistem Performans Testi Başlıyor (14 Cümle)...")

    for i, item in enumerate(test_data, 1):
        print(f"[{i}/{len(test_data)}] İşleniyor ({item['kategori']}): {item['girdi']}")

        # Hibrit Pipeline'ı çağır
        sonuc = pipeline.normalize_text(item['girdi'])

        tahmin = sonuc['final_sonuc']
        hedef = item['hedef']
        durum = "✅ DOĞRU" if tahmin == hedef else "❌ YANLIŞ"

        if tahmin == hedef:
            dogru_sayisi += 1

        # Rapor için kaydet
        results.append({
            "Kategori": item["kategori"],
            "Girdi (Orijinal)": item["girdi"],
            "1. Katman Çıktısı (Regex)": sonuc['regex_sonrasi'],
            "2. Katman Çıktısı (Llama)": tahmin,
            "Hedef (Olması Gereken)": hedef,
            "Durum": durum
        })

    # Doğruluk (Accuracy) Hesaplama
    accuracy = (dogru_sayisi / len(test_data)) * 100

    print("\n" + "=" * 50)
    print(f"🏆 HİBRİT SİSTEM DOĞRULUK ORANI: %{accuracy:.2f} ({dogru_sayisi}/{len(test_data)})")
    print("=" * 50)

    # Sonuçları Excel'e kaydet
    df = pd.DataFrame(results)
    output_file = "step7_hybrid_model/hybrid_test_raporu.xlsx"

    # Hata almamak için klasör içinden mi yoksa ana dizinden mi çalıştığına göre yolu ayarla
    try:
        df.to_excel(output_file, index=False)
        print(f"💾 Tüm çıktılar kaydedildi: {output_file}")
    except:
        df.to_excel("hybrid_test_raporu.xlsx", index=False)
        print(f"💾 Tüm çıktılar kaydedildi: hybrid_test_raporu.xlsx")
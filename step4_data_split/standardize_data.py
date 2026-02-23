import json
from pathlib import Path


def standardize():
    base_path = Path(r"")
    files = ["train.json", "validation.json", "test.json"]

    print("✨ Veri Standardizasyonu Başlıyor ")

    for file_name in files:
        file_path = base_path / file_name

        if not file_path.exists():
            print(f"⚠️ {file_name} bulunamadı!")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            # KURAL 1: Hedef (Target) her koşulda 'Türkiye' olmalı.
            item["target"] = item["target"].replace("Turkey", "Türkiye")

            # KURAL 2: Eğer hata türü 'terminology' ise input 'Turkey' kalsın.
            # Böylece model 'Turkey' gördüğünde 'Türkiye' yapmayı öğrenir.
            if item.get("error_type") == "terminology":
                # Input'u Turkey olarak bırakıyoruz, müdahale etmiyoruz.
                pass

                # KURAL 3: Diğer tüm durumlarda (is_noisy: False veya diğer hatalar)
            # input içindeki 'Turkey' kelimelerini 'Türkiye' yapıyoruz.
            else:
                item["input"] = item["input"].replace("Turkey", "Türkiye")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ {file_name} temizlendi.")


if __name__ == "__main__":
    standardize()
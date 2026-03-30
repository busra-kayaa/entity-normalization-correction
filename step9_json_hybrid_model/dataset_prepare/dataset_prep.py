import json
import difflib


def get_diff_words(noisy_text, clean_text):
    """İki cümle arasındaki TÜM farklı kelimeleri bulur ve liste olarak döner"""
    words_noisy = noisy_text.split()
    words_clean = clean_text.split()
    matcher = difflib.SequenceMatcher(None, words_noisy, words_clean)

    diffs = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ['replace', 'delete', 'insert']:
            old_w = " ".join(words_noisy[i1:i2])
            new_w = " ".join(words_clean[j1:j2])
            diffs.append((old_w, new_w))

    return diffs


# Sistemimizin kabul ettiği 8 Yasal Etiket ve açıklamaları
EXPLANATIONS = {
    "transposition": "Harflerin yer değiştirmesi düzeltildi.",
    "insertion": "Kelime içindeki fazla harf çıkarıldı.",
    "omission": "Kelime içindeki eksik harf eklendi.",
    "substitution": "Yanlış yazılan harf düzeltildi.",
    "deascii": "Türkçe karakter hatası düzeltildi.",
    "space": "Boşluk hatası giderildi.",
    "terminology": "Terminolojik kullanım güncellendi.",
    "common": "Genel yazım veya noktalama hatası düzeltildi."
}

# Kabul edilen 8 etiketin listesi
VALID_LABELS = set(EXPLANATIONS.keys())


def convert_to_llama_format(input_file, output_file):
    print(f"📂 {input_file} okunuyor...")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ HATA: {input_file} bulunamadı! Bu dosyayı atlıyorum.")
        return

    formatted_dataset = []

    for item in data:
        orijinal_metin = item.get("input", "")
        duzeltilmis_metin = item.get("target", "")
        hata_turu = item.get("error_type", "none")
        is_noisy = item.get("is_noisy", False)

        corrections_list = []

        if is_noisy and hata_turu != "none":
            # 🛡️ GÜVENLİK DUVARI: Etiket bizim 8'li sistemde yoksa (örn: punctuation) -> 'common' yap
            if hata_turu not in VALID_LABELS:
                hata_turu = "common"

            # Cümledeki tüm değişiklikleri al
            diff_list = get_diff_words(orijinal_metin, duzeltilmis_metin)

            for eski_kelime, yeni_kelime in diff_list:
                if eski_kelime or yeni_kelime:
                    corrections_list.append({
                        "original": eski_kelime,
                        "corrected": yeni_kelime,
                        "type": hata_turu,
                        "explanation": EXPLANATIONS.get(hata_turu, "Yazım hatası düzeltildi.")
                    })

        # Mizan v2 JSON Objesi
        target_json_obj = {
            "originalText": orijinal_metin,
            "correctedText": duzeltilmis_metin,
            "corrections": corrections_list
        }

        # JSON objesini metne çeviriyoruz (Llama metin üretsin diye)
        target_json_string = json.dumps(target_json_obj, ensure_ascii=False, indent=2)

        formatted_dataset.append({
            "input_text": orijinal_metin,
            "target_json": target_json_string
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(formatted_dataset, f, ensure_ascii=False, indent=4)

    print(f"✅ Başarılı! {len(formatted_dataset)} satır dönüştürüldü -> 💾 {output_file}")


if __name__ == "__main__":
    print("🚀 Veri Seti Dönüştürme İşlemi Başlıyor...\n" + "=" * 40)

    # 1. Eğitim Seti
    convert_to_llama_format("train.json", "mizan_v2_train.json")

    # 2. Doğrulama Seti
    convert_to_llama_format("validation.json", "mizan_v2_validation.json")

    # 3. Test Seti
    convert_to_llama_format("test.json", "mizan_v2_test.json")

    print("=" * 40 + "\n🎉 Tüm dosyalar Mizan v2 formatına başarıyla dönüştürüldü!")
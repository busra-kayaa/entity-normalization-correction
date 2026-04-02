import json
import os


def inject_clean_examples_to_all():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # İşlem yapılacak setlerin listesi
    splits = [
        {
            "name": "EĞİTİM (TRAIN)",
            "raw": "mizan_6class_train.jsonl",
            "atomic": "mizan_v4_atomic_train.jsonl"
        },
        {
            "name": "DOĞRULAMA (VALIDATION)",
            "raw": "mizan_6class_validation.jsonl",
            "atomic": "mizan_v4_atomic_validation.jsonl"
        },
        {
            "name": "TEST",
            "raw": "mizan_6class_test.jsonl",
            "atomic": "mizan_v4_atomic_test.jsonl"
        }
    ]

    instruction = (
        "You are an expert text correction system. Fix ALL errors in the input text and output a detailed JSON. "
        "CRITICAL RULE: List EVERY single changed word as a SEPARATE object. DO NOT output full sentences in the corrections array. "
        "Use ONLY these types: 'typographic', 'punctuation', 'grammar', 'lexical', 'deascii', 'terminology'."
    )

    print("🚀 Temiz veri enjeksiyonu tüm setler için başlıyor...\n")

    for split in splits:
        raw_path = os.path.join(current_dir, split["raw"])
        atomic_path = os.path.join(current_dir, split["atomic"])

        if not os.path.exists(raw_path):
            print(f"⚠️ Uyarı: {split['raw']} bulunamadı, bu set atlanıyor.")
            continue

        clean_count = 0
        # Mevcut atomik dosyaya 'a' (append) moduyla ekleme yapıyoruz
        with open(raw_path, 'r', encoding='utf-8') as f_raw, \
                open(atomic_path, 'a', encoding='utf-8') as f_atomic:

            for line in f_raw:
                try:
                    data = json.loads(line)
                    input_text = data['input']
                    output_json = json.loads(data['output'])
                    target_text = output_json['correctedText']

                    # Eğer girdi ve çıktı aynıysa (Hata yoksa)
                    if input_text.strip() == target_text.strip():
                        atomic_entry = {
                            "instruction": instruction,
                            "input": input_text,
                            "output": json.dumps({
                                "originalText": input_text,
                                "correctedText": target_text,
                                "corrections": []
                            }, ensure_ascii=False)
                        }
                        f_atomic.write(json.dumps(atomic_entry, ensure_ascii=False) + '\n')
                        clean_count += 1
                except Exception as e:
                    print(f"❌ Satır işlenirken hata: {e}")

        print(f"✅ {split['name']}: {clean_count} adet temiz cümle atomik sete eklendi.")

    print(f"\n🎉 İşlem tamamlandı! Artık tüm setlerin (Train/Val/Test) hem hatalı hem temiz örnekleri var.")


if __name__ == "__main__":
    inject_clean_examples_to_all()
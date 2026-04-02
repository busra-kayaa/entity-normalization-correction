import json

booster_data = [
    {
        "input": "The goverment in Turkiye ascension process struck by the crisis",
        "correctedText": "The government in Türkiye's accession process were struck by the crisis.",
        "corrections": [
            {"original": "goverment", "corrected": "government", "type": "lexical",
             "explanation": "Genel İngilizce yazım hatası (lexical spelling)."},
            {"original": "Turkiye", "corrected": "Türkiye's", "type": "grammar",
             "explanation": "Hem deascii hem iyelik eki (possessive) hatası gramer bağlamında düzeltildi."},
            {"original": "ascension", "corrected": "accession", "type": "lexical",
             "explanation": "Bağlama uymayan kelime (ascension -> accession) değiştirildi."},
            {"original": "[Eksik]", "corrected": "were", "type": "grammar",
             "explanation": "Edilgen çatı (passive voice) için yardımcı fiil eklendi."},
            {"original": "[Eksik]", "corrected": ".", "type": "punctuation",
             "explanation": "Cümle sonu noktası eklendi."}
        ]
    },
    {
        "input": "Istanbul is big city and President of the usa visited AbdullahGül yestarday",
        "correctedText": "İstanbul is a big city, and the President of the USA visited Abdullah Gül yesterday.",
        "corrections": [
            {"original": "Istanbul", "corrected": "İstanbul", "type": "deascii",
             "explanation": "Türkçe karakter (İ) düzeltildi."},
            {"original": "[Eksik]", "corrected": "a", "type": "grammar", "explanation": "Eksik artikel (a) eklendi."},
            {"original": "[Eksik]", "corrected": ",", "type": "punctuation",
             "explanation": "Bağımsız cümlecikler arasına virgül eklendi."},
            {"original": "[Eksik]", "corrected": "the", "type": "grammar",
             "explanation": "Unvan öncesi eksik artikel (the) eklendi."},
            {"original": "usa", "corrected": "USA", "type": "typographic",
             "explanation": "Kısaltma büyük harfe çevrildi."},
            {"original": "AbdullahGül", "corrected": "Abdullah Gül", "type": "typographic",
             "explanation": "Birleşik yazım hatası düzeltildi (boşluk eklendi)."},
            {"original": "yestarday", "corrected": "yesterday", "type": "lexical",
             "explanation": "Genel İngilizce yazım hatası düzeltildi."},
            {"original": "[Eksik]", "corrected": ".", "type": "punctuation",
             "explanation": "Cümle sonu noktası eklendi."}
        ]
    },
    {
        "input": "Some of the episodes has been released in United Kingdom as region 2 DVDs",
        "correctedText": "Some of the episodes have been released in the United Kingdom as region 2 DVDs.",
        "corrections": [
            {"original": "has", "corrected": "have", "type": "grammar",
             "explanation": "Özne-yüklem uyumu: Çoğul özne (episodes) için 'have' kullanıldı."},
            {"original": "[Eksik]", "corrected": "the", "type": "grammar",
             "explanation": "Ülke ismi öncesi eksik artikel (the) eklendi."},
            {"original": "[Eksik]", "corrected": ".", "type": "punctuation",
             "explanation": "Cümle sonu noktası eklendi."}
        ]
    },
    {
        "input": "Swaziland goverment decided to change its name to eSwatini but enviroment is still hostile",
        "correctedText": "Eswatini government decided to change its name to Eswatini, but the environment is still hostile.",
        "corrections": [
            {"original": "Swaziland", "corrected": "Eswatini", "type": "terminology",
             "explanation": "Uluslararası isim değişikliği."},
            {"original": "goverment", "corrected": "government", "type": "lexical",
             "explanation": "Genel İngilizce yazım hatası."},
            {"original": "eSwatini", "corrected": "Eswatini", "type": "typographic",
             "explanation": "Büyük/küçük harf dizilimi düzeltildi."},
            {"original": "[Eksik]", "corrected": ",", "type": "punctuation",
             "explanation": "Bağlaç öncesi virgül eklendi."},
            {"original": "[Eksik]", "corrected": "the", "type": "grammar", "explanation": "Eksik artikel eklendi."},
            {"original": "enviroment", "corrected": "environment", "type": "lexical",
             "explanation": "Genel İngilizce yazım hatası."},
            {"original": "[Eksik]", "corrected": ".", "type": "punctuation",
             "explanation": "Cümle sonu noktası eklendi."}
        ]
    }
]

SYSTEM_INSTRUCTION = (
    "You are an expert text correction system. Fix ALL errors in the input text and output a detailed JSON. "
    "CRITICAL RULE: List EVERY single changed word as a SEPARATE object. DO NOT output full sentences in the corrections array. "
    "Use ONLY these error types exactly as defined: 'deascii', 'typographic', 'terminology', 'lexical', 'grammar', 'punctuation'."
)


def append_booster_to_train(train_file_path):
    print(f"🚀 Takviye verileri {train_file_path} dosyasına ekleniyor...")

    with open(train_file_path, 'a', encoding='utf-8') as f:
        for data in booster_data:
            expected_json_output = {
                "originalText": data["input"],
                "correctedText": data["correctedText"],
                "corrections": data["corrections"]
            }

            jsonl_line = {
                "instruction": SYSTEM_INSTRUCTION,
                "input": data["input"],
                "output": json.dumps(expected_json_output, ensure_ascii=False)
            }
            f.write(json.dumps(jsonl_line, ensure_ascii=False) + "\n")

    print("✅ İŞLEM TAMAM! 6 Sınıflı Gramer ve Noktalama takviyesi eğitim setine eklendi.")


if __name__ == "__main__":
    append_booster_to_train("mizan_v4_atomic_train.jsonl")
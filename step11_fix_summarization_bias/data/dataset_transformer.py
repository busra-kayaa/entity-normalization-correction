import json
import re
import difflib

NEW_INSTRUCTION = (
    "You are an expert text correction system. Fix ALL errors in the input text and output a detailed JSON. "
    "CRITICAL RULE: List EVERY single changed word as a SEPARATE object. DO NOT output full sentences in the corrections array. "
    "Use ONLY these types: 'typographic', 'punctuation', 'grammar', 'lexical', 'deascii', 'terminology'."
)


def extract_word_diffs(original, corrected):
    """Eski tüm cümleyi alan sistemi, kelime kelime parçalara ayırır."""
    corrections = []
    orig_words = re.findall(r"[\w']+|[.,!?;]", original)
    corr_words = re.findall(r"[\w']+|[.,!?;]", corrected)

    matcher = difflib.SequenceMatcher(None, orig_words, corr_words)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            corrections.append({
                "original": " ".join(orig_words[i1:i2]),
                "corrected": " ".join(corr_words[j1:j2]),
                "type": "typographic",  # Çoğunluk typo olduğu için varsayılan
                "explanation": "Hatalı kullanım düzeltildi."
            })
        elif tag == 'insert':
            corrections.append({
                "original": "[Eksik]",
                "corrected": " ".join(corr_words[j1:j2]),
                "type": "grammar",
                "explanation": "Eksik ifade eklendi."
            })
        elif tag == 'delete':
            corrections.append({
                "original": " ".join(orig_words[i1:i2]),
                "corrected": "[Silindi]",
                "type": "lexical",
                "explanation": "Gereksiz ifade çıkarıldı."
            })
    return corrections


def transform_dataset(input_file, output_file):
    print(f"🔄 '{input_file}' okunuyor ve atomik formata dönüştürülüyor...")

    transformed_count = 0
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        for line in infile:
            if not line.strip(): continue

            try:
                data = json.loads(line)

                # Eski veriden input ve output'u alıyoruz
                original_text = data.get("input", "")

                # Eğer eski output string ise (Alpaca formatı) onu parse edelim
                raw_output = data.get("output", "{}")
                if isinstance(raw_output, str):
                    try:
                        parsed_output = json.loads(raw_output)
                        corrected_text = parsed_output.get("correctedText", original_text)
                    except:
                        continue  # Bozuk JSON varsa atla
                else:
                    corrected_text = raw_output.get("correctedText", original_text)

                # Metin değişmemişse veri setine katmaya gerek yok
                if original_text == corrected_text:
                    continue

                atomic_corrections = extract_word_diffs(original_text, corrected_text)

                new_expected_output = {
                    "originalText": original_text,
                    "correctedText": corrected_text,
                    "corrections": atomic_corrections
                }

                new_jsonl_line = {
                    "instruction": NEW_INSTRUCTION,
                    "input": original_text,
                    "output": json.dumps(new_expected_output, ensure_ascii=False)
                }

                outfile.write(json.dumps(new_jsonl_line, ensure_ascii=False) + "\n")
                transformed_count += 1

            except Exception as e:
                pass  # Hatalı satırları yoksay

    print(f"✅ İŞLEM TAMAM! {transformed_count} satır başarıyla atomik formata çevrildi.")
    print(f"📁 Yeni veri setin: {output_file}")


if __name__ == "__main__":
    print("🚀 BÜYÜK VERİ DÖNÜŞÜMÜ BAŞLIYOR...\n")

    # 1. Eğitim (Train) Seti
    print("1️⃣ EĞİTİM (TRAIN) SETİ DÖNÜŞTÜRÜLÜYOR...")
    transform_dataset("mizan_6class_train.jsonl", "mizan_v4_atomic_train.jsonl")

    # 2. Doğrulama (Validation) Seti
    print("\n2️⃣ DOĞRULAMA (VALIDATION) SETİ DÖNÜŞTÜRÜLÜYOR...")
    transform_dataset("mizan_6class_validation.jsonl", "mizan_v4_atomic_validation.jsonl")

    # 3. Test Seti
    print("\n3️⃣ TEST SETİ DÖNÜŞTÜRÜLÜYOR...")
    # Test dosyanın adını aşağıya kendi proyendeki ismine göre yazabilirsin
    transform_dataset("mizan_6class_test.jsonl", "mizan_v4_atomic_test.jsonl")

    print("\n🎉 İŞLEM TAMAM! TÜM VERİ SETLERİ (TRAIN, VAL, TEST) ATOMİK EĞİTİME HAZIR!")
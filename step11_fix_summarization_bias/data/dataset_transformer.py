import json
import os
import re
import random
import glob
from collections import Counter
from difflib import SequenceMatcher

# ==================== KONFİGÜRASYON VE SÖZLÜKLER ====================
EXPLANATIONS = {
    "deascii": "Türkçe karakter eksikliği veya hatası düzeltildi.",
    "lexical": "Yaygın kelime yazım hatası düzeltildi.",
    "typographic": "Tipografik harf veya klavye hatası düzeltildi.",
    "punctuation": "Noktalama işareti hatası veya eksiği düzeltildi.",
    "grammar": "Dilbilgisi veya edat kullanımı düzeltildi.",
    "terminology": "Özel isim veya terminoloji hatası düzeltildi."
}

GRAMMAR_WORDS = ["in", "on", "at", "to", "for", "with", "the", "a", "an"]


def tokenize(text):
    return re.findall(r"[\w]+|[^\s\w]", text)


def determine_error_type(original, corrected, sentence_labels):
    orig_lower = original.lower()
    corr_lower = corrected.lower()

    if not orig_lower.isalnum() and not corr_lower.isalnum(): return "punctuation"
    if corr_lower in GRAMMAR_WORDS or orig_lower in GRAMMAR_WORDS: return "grammar"
    if any(c in "çğıöşüÇĞİÖŞÜ" for c in corrected) and not any(c in "çğıöşüÇĞİÖŞÜ" for c in original): return "deascii"
    if "terminology" in sentence_labels and (corrected.istitle() or original.istitle()): return "terminology"
    if "lexical" in sentence_labels: return "lexical"
    return "typographic"


def extract_atomic_corrections(noisy_text, clean_text, sentence_labels):
    noisy_tokens = tokenize(noisy_text)
    clean_tokens = tokenize(clean_text)

    matcher = SequenceMatcher(None, noisy_tokens, clean_tokens)
    corrections = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            max_len = max(i2 - i1, j2 - j1)
            for k in range(max_len):
                orig_word = noisy_tokens[i1 + k] if (i1 + k) < i2 else ""
                corr_word = clean_tokens[j1 + k] if (j1 + k) < j2 else ""

                if not orig_word and not corr_word: continue

                err_type = determine_error_type(orig_word, corr_word, sentence_labels)
                corrections.append({
                    "original": orig_word, "corrected": corr_word,
                    "type": err_type, "explanation": EXPLANATIONS.get(err_type, "Hatalı kullanım düzeltildi.")
                })

        elif tag == 'insert':
            for k in range(j1, j2):
                corr_word = clean_tokens[k]
                err_type = determine_error_type("", corr_word, sentence_labels)
                corrections.append({
                    "original": "", "corrected": corr_word,
                    "type": err_type, "explanation": EXPLANATIONS.get(err_type, "Eksik kelime veya noktalama eklendi.")
                })

        elif tag == 'delete':
            for k in range(i1, i2):
                orig_word = noisy_tokens[k]
                err_type = determine_error_type(orig_word, "", sentence_labels)
                corrections.append({
                    "original": orig_word, "corrected": "",
                    "type": err_type, "explanation": "Fazladan veya hatalı kullanım silindi."
                })

    return corrections


def analyze_split(train, val, test):
    """Kullanıcının çok sevdiği o muhteşem dağılım raporunu basar."""
    total_all = len(train) + len(val) + len(test)

    md_report = f"# SPLİT RAPORU (Step 11 - {total_all} Balanced Multi-Error)\n\n"
    md_report += f"## 📊 Genel İstatistikler\n\n"
    md_report += f"- **Toplam cümle:** {total_all}\n"
    md_report += f"- **Train:** {len(train)} (%{len(train) / total_all * 100:.1f})\n"
    md_report += f"- **Validation:** {len(val)} (%{len(val) / total_all * 100:.1f})\n"
    md_report += f"- **Test:** {len(test)} (%{len(test) / total_all * 100:.1f})\n"
    md_report += f"- **Random seed:** 42\n\n"
    md_report += f"## 🔍 Hata Tipi Dağılımı (Çoklu Hatalar ve Temiz Metinler Dahil)\n\n"

    print("\n" + "=" * 60)
    print("📊 FULL SPLİT İSTATİSTİKLERİ (Çoklu Hata Destekli)")
    print("=" * 60)

    for name, data_set in [('Train', train), ('Validation', val), ('Test', test)]:
        set_total = len(data_set)
        error_counts = Counter()
        for item in data_set:
            for err in item.get('error_types', ['none']):
                error_counts[err] += 1

        print(f"\n   {name} Seti ({set_total} toplam cümle):")
        md_report += f"### {name} Seti ({set_total} toplam cümle)\n"

        for err_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / set_total * 100) if set_total > 0 else 0
            print(f"      • {err_type}: {count} (Cümlelerin %{percentage:.1f}'inde var)")
            md_report += f"- **{err_type}:** {count} (Cümlelerin %{percentage:.1f}'inde var)\n"
        md_report += "\n"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'split_report.md'), 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f"\n📁 Rapor güncellendi: split_report.md")


def process_and_save(dataset, filename):
    """Veriyi alır, atomik parçalara böler ve JSONL olarak kaydeder."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)

    system_instruction = (
        "You are an expert text correction system. Fix ALL errors and output JSON. "
        "SEQUENTIAL ORDER RULE: List corrections in the EXACT order they appear. "
        "STRICT ATOMIC RULE: Split corrections into single words or punctuation marks. DO NOT group multiple words together. "
        "If a word or punctuation is missing, use an empty string '' as the original text."
    )

    with open(filepath, 'w', encoding='utf-8') as out_f:
        for item in dataset:
            noisy = item["input"]
            clean = item["target"]
            labels = item.get("error_types", ["none"])

            corrections = []
            if item.get("is_noisy", False):
                corrections = extract_atomic_corrections(noisy, clean, labels)

            output_json = {
                "originalText": noisy,
                "correctedText": clean,
                "corrections": corrections
            }

            alpaca_entry = {
                "instruction": system_instruction,
                "input": noisy,
                "output": json.dumps(output_json, ensure_ascii=False)
            }
            out_f.write(json.dumps(alpaca_entry, ensure_ascii=False) + "\n")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Ana dosyayı bul
    search_pattern = os.path.join(current_dir, 'data_*_multi_error_balanced.json')
    files = glob.glob(search_pattern)

    if not files:
        print("❌ HATA: Ana veri seti bulunamadı!")
        return

    input_path = files[0]
    print(f"📦 Ana Veri Seti Okunuyor: {os.path.basename(input_path)}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Veriyi Karıştır ve Böl (80-10-10)
    random.seed(42)
    random.shuffle(data)

    total = len(data)
    train_end = int(total * 0.80)
    val_end = train_end + int(total * 0.10)

    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]

    # 3. İSTATİSTİK RAPORUNU BAS (Senin istediğin kısım!)
    analyze_split(train_data, val_data, test_data)

    # 4. JSONL Dönüşümlerini Yap ve Kaydet
    print("\n🧩 Cümleler ATOMİK (tek kelime) formata dönüştürülüp kaydediliyor...")
    process_and_save(train_data, 'mizan_v4_train.jsonl')
    process_and_save(val_data, 'mizan_v4_validation.jsonl')
    process_and_save(test_data, 'mizan_v4_test.jsonl')

    print("🎉 İŞLEM TAMAMLANDI! Mizan V4 modelini eğitmeye %100 hazırsın! 🚀🔥")


if __name__ == "__main__":
    main()
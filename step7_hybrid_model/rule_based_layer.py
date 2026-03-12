import re

class RuleBasedCorrector:
    def __init__(self):
        # 1. KESİN Terminoloji (Bağlama ihtiyaç duymayan, %100 değişmesi gerekenler)
        self.strict_map = {
            'Burma': 'Myanmar',
            'Swaziland': 'Eswatini',
            'Czech Republic': 'Czechia',
            'Macedonia': 'North Macedonia',
            'Istanbul': 'İstanbul',
            'Izmir': 'İzmir',
            'Erdogan': 'Erdoğan',
            'Besiktas': 'Beşiktaş'
            # Not: 'Turkey' kelimesini buraya koymuyoruz, onu zeki Llama'ya (2. Katmana) bırakıyoruz!
        }

        # Sadece bu kesin kelimeleri Regex ile derliyoruz (Hız için)
        self.patterns = {
            re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE): correct
            for wrong, correct in self.strict_map.items()
        }

    def process(self, text):
        corrected_text = text
        applied_fixes = []

        for pattern, correct_form in self.patterns.items():
            if pattern.search(corrected_text):
                # Eşleşmeyi bul ve doğru formatla (büyük/küçük harf düzenini koruyarak) değiştir
                corrected_text = pattern.sub(correct_form, corrected_text)
                if correct_form not in applied_fixes:
                    applied_fixes.append(correct_form)

        return corrected_text, applied_fixes


# ==================== TEST AŞAMASI ====================
if __name__ == "__main__":
    corrector = RuleBasedCorrector()

    test_sentences = [
        "President Erdogan visited Istanbul after the meetings in Burma.",
        "The economy of turkey is growing." # Turkey burada var ama Regex dokunmayacak.
    ]

    print("🛡️ 1. KATMAN (REGEX) TESTİ 🛡️\n" + "=" * 50)
    for i, sentence in enumerate(test_sentences, 1):
        result, fixes = corrector.process(sentence)
        print(f"[{i}] Orijinal   : {sentence}")
        print(f"    Çıktı      : {result}")
        print(f"    🛠️ Kurallar : {fixes}\n")
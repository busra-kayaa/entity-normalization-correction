import re


class RuleBasedCorrector:
    def __init__(self):
        # 1. KESİN Terminoloji ve Hata Tipleri
        # Yapı: 'Yanlış Kelime': ('Doğru Kelime', 'Hata_Etiketi')
        self.strict_map = {
            'Burma': ('Myanmar', 'terminology'),
            'Swaziland': ('Eswatini', 'terminology'),
            'Czech Republic': ('Czechia', 'terminology'),
            'Macedonia': ('North Macedonia', 'terminology'),
            'Istanbul': ('İstanbul', 'de-asciification'),
            'Izmir': ('İzmir', 'de-asciification'),
            'Erdogan': ('Erdoğan', 'de-asciification'),
            'Besiktas': ('Beşiktaş', 'de-asciification')
            # Not: 'Turkey' kelimesini buraya koymuyoruz, onu zeki Llama'ya (2. Katmana) bırakıyoruz!
        }

        # Regex derlemesi: Hız için patternleri ve (doğru_kelime, etiket) ikilisini önceden hazırlıyoruz
        self.patterns = {
            re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE): data
            for wrong, data in self.strict_map.items()
        }

    def process(self, text):
        corrected_text = text
        applied_labels = []  # Artık kelimeleri değil, etiketleri toplayacak

        for pattern, (correct_form, error_label) in self.patterns.items():
            # 🚀 OPTİMİZASYON: subn() metodu metni değiştirir ve kaç kez değiştirdiğini (count) döner.
            corrected_text, count = pattern.subn(correct_form, corrected_text)

            # Eğer değişiklik yapıldıysa ve bu etiket listemizde henüz yoksa ekle
            if count > 0 and error_label not in applied_labels:
                applied_labels.append(error_label)

        return corrected_text, applied_labels


# ==================== TEST AŞAMASI ====================
if __name__ == "__main__":
    corrector = RuleBasedCorrector()

    test_sentences = [
        "President Erdogan visited Istanbul after the meetings in Burma.",
        "The economy of turkey is growing."  # Turkey burada var ama Regex dokunmayacak.
    ]

    print("🛡️ 1. KATMAN (REGEX) TESTİ 🛡️\n" + "=" * 50)
    for i, sentence in enumerate(test_sentences, 1):
        result, labels = corrector.process(sentence)
        print(f"[{i}] Orijinal   : {sentence}")
        print(f"    Çıktı      : {result}")
        print(f"    🛠️ Etiketler : {labels}\n")
import re

class RuleBasedCorrector:
    def __init__(self):
        # 8 Kategorili Akademik Sözlük
        self.strict_map = {
            'Burma': ('Myanmar', 'terminology', "Resmi ülke adı 'Myanmar' olarak güncellendi."),
            'Swaziland': ('Eswatini', 'terminology', "Resmi ülke adı 'Eswatini' olarak güncellendi."),
            'Czech Republic': ('Czechia', 'terminology', "Ülkenin kısa resmi adı 'Czechia' olarak güncellendi."),
            'Macedonia': ('North Macedonia', 'terminology', "Resmi isim 'North Macedonia' olarak güncellendi."),
            'Istanbul': ('İstanbul', 'deascii', "Özel isimdeki Türkçe karakter (İ) hatası düzeltildi."),
            'Izmir': ('İzmir', 'deascii', "Özel isimdeki Türkçe karakter (İ) hatası düzeltildi."),
            'Erdogan': ('Erdoğan', 'deascii', "Özel isimdeki Türkçe karakter (ğ) hatası düzeltildi."),
            'Besiktas': ('Beşiktaş', 'deascii', "Özel isimdeki Türkçe karakter (ş) hatası düzeltildi.")
        }

        self.patterns = {
            re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE): data
            for wrong, data in self.strict_map.items()
        }

    def process(self, text):
        corrected_text = text
        corrections_list = []

        for pattern, (correct_form, error_label, explanation) in self.patterns.items():
            matches = list(pattern.finditer(corrected_text))
            if matches:
                for match in matches:
                    original_word = match.group()
                    if not any(c.get('original') == original_word for c in corrections_list):
                        corrections_list.append({
                            "original": original_word,
                            "corrected": correct_form,
                            "type": error_label,
                            "explanation": explanation
                        })
                corrected_text = pattern.sub(correct_form, corrected_text)

        return corrected_text, corrections_list
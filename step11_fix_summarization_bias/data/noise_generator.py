import json
import random
import os
import re
from collections import Counter


# ==================== 1. KONFİGÜRASYON YÜKLEME ====================
def load_config(script_dir):
    config_path = os.path.join(script_dir, 'noise_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"✅ Konfigürasyon yüklendi: {config_path}")
            return config
    except FileNotFoundError:
        print("⚠️ noise_config.json bulunamadı, senin verdiğin değerler kullanılıyor...")
        return {
            "noise_ratio": 0.60,
            "target_count": 10000,
            "error_types": {
                "deascii": 0.15, "terminology": 0.15, "punctuation": 0.15, "grammar": 0.15,
                "lexical": 0.10, "substitution": 0.08, "omission": 0.07,
                "transposition": 0.06, "space": 0.05, "insertion": 0.04
            }
        }


# ==================== 2. GENİŞLETİLMİŞ SÖZLÜKLER ====================
DEASCII_MAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")

TERMINOLOGY_MAP = {
    'Turkey': 'Türkiye',
    'Burma': 'Myanmar',
    'Swaziland': 'Eswatini'
}

COMMON_ERRORS = {
    'government': 'goverment', 'environment': 'enviroment',
    'political': 'politcal', 'receive': 'recieve',
    'separate': 'seperate', 'independent': 'independant',
    'accommodation': 'accomodation', 'definitely': 'definately',
    'believe': 'beleive', 'necessary': 'neccessary',
    'immediately': 'immediatly', 'business': 'buisness',
    'successful': 'succesful', 'professional': 'proffesional',
    'occurrence': 'occurence', 'beginning': 'begining'
}

SPACE_ERRORS = {
    'New York': 'NewYork', 'United States': 'UnitedStates',
    'White House': 'WhiteHouse', 'prime minister': 'primeminister',
    'Social Media': 'SocialMedia', 'High School': 'HighSchool',
    'Human Rights': 'HumanRights', 'Middle East': 'MiddleEast',
    'North Korea': 'NorthKorea', 'South Korea': 'SouthKorea',
    'Climate Change': 'ClimateChange', 'World War': 'WorldWar',
    'Real Estate': 'RealEstate', 'European Union': 'EuropeanUnion'
}

GRAMMAR_WORDS = ["in", "on", "at", "to", "for", "with", "the", "a", "an"]
KEYBOARD_NEIGHBORS = {'a': 'sqz', 's': 'adwz', 'd': 'sfewx', 'f': 'dgrtv', 'g': 'fhtby', 'h': 'gjnyu'}

# 6'LI SINIFLANDIRMA (TAXONOMY) FİLTRESİ
LABEL_MAP = {
    'deascii': 'deascii',
    'terminology': 'terminology',
    'grammar': 'grammar',
    'punctuation': 'punctuation',
    'common': 'lexical',
    'space': 'typographic',
    'omission': 'typographic',
    'insertion': 'typographic',
    'transposition': 'typographic',
    'substitution': 'typographic'
}


# ==================== 3. GÜRÜLTÜ ÜRETİCİ SINIFI ====================
class NoiseGenerator:
    def __init__(self, config):
        self.config = config
        self.stats = Counter()

    def apply_standardization(self, text):
        for wrong_form, right_form in TERMINOLOGY_MAP.items():
            text = re.sub(r'\b' + re.escape(wrong_form) + r'\b', right_form, text, flags=re.IGNORECASE)
        return text

    def apply_specific_error(self, sentence, error_type):
        noisy_text = sentence
        changed = False

        if error_type == 'terminology':
            for wrong_form, right_form in TERMINOLOGY_MAP.items():
                if right_form in sentence:
                    noisy_text = sentence.replace(right_form, wrong_form, 1)
                    changed = True
                    break

        elif error_type == 'grammar':
            words = sentence.split()
            valid_indices = [i for i, w in enumerate(words) if w.lower() in GRAMMAR_WORDS]
            if valid_indices:
                idx = random.choice(valid_indices)
                words.pop(idx)
                noisy_text = " ".join(words)
                changed = True

        elif error_type == 'punctuation':
            if sentence.endswith('.'):
                noisy_text = sentence[:-1]
                changed = True
            elif ',' in sentence:
                noisy_text = sentence.replace(',', '', 1)
                changed = True

        elif error_type == 'common':
            for key, val in COMMON_ERRORS.items():
                pattern = r'\b' + re.escape(key) + r'\b'
                if re.search(pattern, sentence, re.IGNORECASE):
                    noisy_text = re.sub(pattern, val, sentence, count=1, flags=re.IGNORECASE)
                    changed = True
                    break

        elif error_type == 'space':
            for key, val in SPACE_ERRORS.items():
                if key in sentence:
                    noisy_text = sentence.replace(key, val, 1)
                    changed = True
                    break

        elif error_type == 'deascii':
            if any(c in "çğıöşüÇĞİÖŞÜ" for c in sentence):
                noisy_text = sentence.translate(DEASCII_MAP)
                changed = True

        elif error_type in ['omission', 'insertion', 'transposition', 'substitution']:
            words = sentence.split()
            indices = list(range(len(words)))
            random.shuffle(indices)
            for idx in indices:
                word = words[idx]
                if len(word) >= 5 and word.isalpha():
                    char_list = list(word)
                    pos = random.randint(0, len(char_list) - 1)
                    if error_type == 'omission':
                        char_list.pop(pos)
                    elif error_type == 'insertion':
                        char_list.insert(pos, random.choice('abcde'))
                    elif error_type == 'transposition' and pos < len(char_list) - 1:
                        char_list[pos], char_list[pos + 1] = char_list[pos + 1], char_list[pos]
                    elif error_type == 'substitution':
                        char = char_list[pos].lower()
                        char_list[pos] = random.choice(KEYBOARD_NEIGHBORS.get(char, 'xyz'))
                    words[idx] = "".join(char_list)
                    noisy_text = " ".join(words)
                    changed = True
                    break

        return noisy_text, changed


# ==================== 4. ANA İŞLEME ====================
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config(current_dir)

    input_path = os.path.abspath(os.path.join(
        current_dir,
        'dataset_latest_2.json'
    ))

    if not os.path.exists(input_path):
        print(f"❌ HATA: Veri seti bulunamadı -> {input_path}")
        print("Lütfen 'input_path' değişkenindeki dosya yolunu kontrol et.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    gen = NoiseGenerator(config)
    sentences = data['sentences']
    random.shuffle(sentences)

    target_noisy_total = int(len(sentences) * config.get('noise_ratio', 0.60))
    error_types_config = config.get('error_types', {})

    processed_pairs = []
    used_indices = set()

    # 1. PAS: Spesifik hatalar (Tüm tipler)
    specific_errors = ['terminology', 'common', 'deascii', 'space', 'grammar', 'punctuation']
    for err_type in specific_errors:
        weight = error_types_config.get(err_type, 0.10)
        quota = int(target_noisy_total * weight)
        count = 0
        for i, raw_s in enumerate(sentences):
            if i in used_indices or count >= quota: continue

            standardized_target = gen.apply_standardization(raw_s)
            res, ok = gen.apply_specific_error(standardized_target, err_type)

            if ok:
                # 🚀 Hiyerarşik dönüşüm uygulanıyor
                final_label = LABEL_MAP.get(err_type, err_type)
                processed_pairs.append(
                    {"input": res, "target": standardized_target, "is_noisy": True, "error_type": final_label})
                used_indices.add(i)
                count += 1
                gen.stats[err_type] += 1

    # 2. PAS: Kalan kotayı tipografik hatalarla tamamla
    typo_types = ['substitution', 'omission', 'insertion', 'transposition']
    for i, raw_s in enumerate(sentences):
        if len(used_indices) >= target_noisy_total: break
        if i in used_indices: continue

        standardized_target = gen.apply_standardization(raw_s)
        err_choice = random.choice(typo_types)
        res, ok = gen.apply_specific_error(standardized_target, err_choice)

        if ok:
            # 🚀 Hiyerarşik dönüşüm uygulanıyor
            final_label = LABEL_MAP.get(err_choice, err_choice)
            processed_pairs.append(
                {"input": res, "target": standardized_target, "is_noisy": True, "error_type": final_label})
            used_indices.add(i)
            gen.stats[err_choice] += 1

    # 3. PAS: Kalanlar temiz (Sadece standartlaştırma var)
    for i, raw_s in enumerate(sentences):
        if i not in used_indices:
            standardized_target = gen.apply_standardization(raw_s)
            processed_pairs.append(
                {"input": standardized_target, "target": standardized_target, "is_noisy": False, "error_type": "none"})

    output_file = os.path.join(current_dir, 'data_10000_step10.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_pairs, f, ensure_ascii=False, indent=2)

    print(f"🚀 İşlem Başarıyla Tamamlandı!")
    print(f"📊 Toplam Gürültülü Cümle: {len(used_indices)} / {target_noisy_total}")

    print("\n📁 ÜRETİLEN Alt Hata Sınıfları (Arka Plan):")
    print(dict(gen.stats))

    final_stats = Counter([p['error_type'] for p in processed_pairs if p['is_noisy']])
    print("\n✅ JSON'a YAZILAN 6'lı Hiyerarşik Dağılım:")
    print(dict(final_stats))


if __name__ == "__main__":
    main()
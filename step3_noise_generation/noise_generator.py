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
        print("⚠️ noise_config.json bulunamadı, varsayılan ayarlar kullanılıyor...")
        return {
            "noise_ratio": 0.35,
            "error_types": {
                "deascii": 0.20, "omission": 0.12, "insertion": 0.08,
                "transposition": 0.10, "substitution": 0.15, "space": 0.15,
                "terminology": 0.10, "common": 0.10
            }
        }


# ==================== 2. GENİŞLETİLMİŞ SÖZLÜKLER ====================
# Kategori 1: De-asciification
DEASCII_MAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")

# Kategori 3: Terminoloji (Kesin Kurallar)
TERMINOLOGY_MAP = {
    'Turkey': 'Türkiye',
    'Burma': 'Myanmar',
    'Swaziland': 'Eswatini'
}

# Kategori 4: Genel İngilizce Hataları
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

# Kategori 2: Birleşik/Ayrı Yazım Hataları
SPACE_ERRORS = {
    'New York': 'NewYork', 'United States': 'UnitedStates',
    'White House': 'WhiteHouse', 'prime minister': 'primeminister',
    'Social Media': 'SocialMedia', 'High School': 'HighSchool',
    'Human Rights': 'HumanRights', 'Middle East': 'MiddleEast',
    'North Korea': 'NorthKorea', 'South Korea': 'SouthKorea',
    'Climate Change': 'ClimateChange', 'World War': 'WorldWar',
    'Real Estate': 'RealEstate', 'European Union': 'EuropeanUnion'
}

KEYBOARD_NEIGHBORS = {'a': 'sqz', 's': 'adwz', 'd': 'sfewx', 'f': 'dgrtv', 'g': 'fhtby', 'h': 'gjnyu'}


# ==================== 3. GÜRÜLTÜ ÜRETİCİ SINIFI ====================
class NoiseGenerator:
    def __init__(self, config):
        self.config = config
        self.stats = Counter()

    def apply_specific_error(self, sentence, error_type):
        noisy_text = sentence
        changed = False

        if error_type == 'terminology':
            for key, val in TERMINOLOGY_MAP.items():
                if key in sentence:
                    noisy_text = sentence.replace(key, val, 1)
                    changed = True;
                    break

        elif error_type == 'common':
            for key, val in COMMON_ERRORS.items():
                pattern = r'\b' + re.escape(key) + r'\b'
                if re.search(pattern, sentence, re.IGNORECASE):
                    noisy_text = re.sub(pattern, val, sentence, count=1, flags=re.IGNORECASE)
                    changed = True;
                    break

        elif error_type == 'space':
            for key, val in SPACE_ERRORS.items():
                if key in sentence:
                    noisy_text = sentence.replace(key, val, 1)
                    changed = True;
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
                    changed = True;
                    break

        return noisy_text, changed


# ==================== 4. ANA İŞLEME ====================
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config(current_dir)
    input_path = os.path.join(
        os.path.dirname(current_dir),
        'step2_data_collection',
        'dataset_latest.json')

    if not os.path.exists(input_path):
        print(f"❌ HATA: Veri seti bulunamadı -> {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    gen = NoiseGenerator(config)
    sentences = data['sentences']
    random.shuffle(sentences)

    target_noisy_total = int(len(sentences) * config.get('noise_ratio', 0.35))
    error_types_config = config.get('error_types', {})

    processed_pairs = []
    used_indices = set()

    # 1. PAS: Spesifik hatalar (Kategori 1, 3, 4 ve Space)
    specific_errors = ['terminology', 'common', 'deascii', 'space']
    for err_type in specific_errors:
        weight = error_types_config.get(err_type, 0.10)
        quota = int(target_noisy_total * weight)
        count = 0
        for i, s in enumerate(sentences):
            if i in used_indices or count >= quota: continue
            res, ok = gen.apply_specific_error(s, err_type)
            if ok:
                processed_pairs.append({"input": res, "target": s, "is_noisy": True, "error_type": err_type})
                used_indices.add(i);
                count += 1;
                gen.stats[err_type] += 1

    # 2. PAS: Kalan kotayı tipografik hatalarla tamamla
    typo_types = ['substitution', 'omission', 'insertion', 'transposition']
    for i, s in enumerate(sentences): # i cümle indexi, s cümle metni
        if len(used_indices) >= target_noisy_total: break
        if i in used_indices: continue

        err_choice = random.choice(typo_types)
        res, ok = gen.apply_specific_error(s, err_choice)
        if ok:
            processed_pairs.append({"input": res, "target": s, "is_noisy": True, "error_type": err_choice})
            used_indices.add(i);
            gen.stats[err_choice] += 1

    # 3. Kalanlar temiz
    for i, s in enumerate(sentences):
        if i not in used_indices:
            processed_pairs.append({"input": s, "target": s, "is_noisy": False, "error_type": "none"})

    with open(os.path.join(current_dir, 'train_data_step3.json'), 'w', encoding='utf-8') as f:
        json.dump(processed_pairs, f, ensure_ascii=False, indent=2)

    print(f"🚀 İşlem Başarıyla Tamamlandı!")
    print(f"📊 Toplam Gürültülü: {len(used_indices)} / {target_noisy_total}")
    print(f"📁 Dağılım: {dict(gen.stats)}")


if __name__ == "__main__":
    main()
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
        print("⚠️ HATA: noise_config.json bulunamadı!")
        return {}


# ==================== 2. SÖZLÜKLER ====================
DEASCII_MAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")

TERMINOLOGY_MAP = {
    'Turkey': 'Türkiye', 'Burma': 'Myanmar', 'Swaziland': 'Eswatini',
    'Holland': 'Netherlands', 'Czech Republic': 'Czechia', 'Great Britain': 'United Kingdom',
    'Kiev': 'Kyiv', 'Bombay': 'Mumbai', 'Calcutta': 'Kolkata', 'Madras': 'Chennai',
    'Peking': 'Beijing', 'Canton': 'Guangzhou', 'Zaire': 'Democratic Republic of the Congo',
    'Macedonia': 'North Macedonia', 'Ceylon': 'Sri Lanka', 'Siam': 'Thailand'
}

COMMON_ERRORS = {
    'government': 'goverment', 'environment': 'enviroment', 'political': 'politcal',
    'receive': 'recieve', 'separate': 'seperate', 'independent': 'independant',
    'accommodation': 'accomodation', 'definitely': 'definately', 'believe': 'beleive',
    'necessary': 'neccessary', 'immediately': 'immediatly', 'business': 'buisness',
    'successful': 'succesful', 'professional': 'proffesional', 'occurrence': 'occurence',
    'beginning': 'begining', 'calendar': 'calender', 'colleague': 'collegue',
    'fascinating': 'facinating', 'fluorescent': 'flourescent', 'guarantee': 'garantee',
    'knowledge': 'knowlege', 'maintenance': 'maintainance', 'noticeable': 'noticable',
    'privilege': 'priviledge', 'recommend': 'recomend', 'restaurant': 'restarant',
    'schedule': 'scheduel', 'tomorrow': 'tommorow', 'until': 'untill', 'weather': 'whether'
}

SPACE_ERRORS = {
    'New York': 'NewYork', 'United States': 'UnitedStates', 'White House': 'WhiteHouse',
    'prime minister': 'primeminister', 'Social Media': 'SocialMedia', 'High School': 'HighSchool',
    'Human Rights': 'HumanRights', 'Middle East': 'MiddleEast', 'North Korea': 'NorthKorea',
    'South Korea': 'SouthKorea', 'Climate Change': 'ClimateChange', 'World War': 'WorldWar',
    'Real Estate': 'RealEstate', 'European Union': 'EuropeanUnion'
}

GRAMMAR_WORDS = ["in", "on", "at", "to", "for", "with", "the", "a", "an"]
KEYBOARD_NEIGHBORS = {'a': 'sqz', 's': 'adwz', 'd': 'sfewx', 'f': 'dgrtv', 'g': 'fhtby', 'h': 'gjnyu'}


# ==================== 3. DİNAMİK KOTALI GÜRÜLTÜ ÜRETİCİ ====================
class BalancedMultiNoiseGenerator:
    def __init__(self, target_classes):
        # Sınıfları artık doğrudan Config'den alıyoruz
        self.stats = Counter({cls: 0 for cls in target_classes})

    def apply_standardization(self, text):
        for wrong_form, right_form in TERMINOLOGY_MAP.items():
            text = re.sub(r'\b' + re.escape(wrong_form) + r'\b', right_form, text, flags=re.IGNORECASE)
        return text

    def apply_error(self, sentence, error_type):
        noisy_text = sentence
        success = False

        if error_type == 'deascii':
            if any(c in "çğıöşüÇĞİÖŞÜ" for c in sentence):
                noisy_text = sentence.translate(DEASCII_MAP)
                success = True

        elif error_type == 'lexical':
            for key, val in COMMON_ERRORS.items():
                pattern = r'\b' + re.escape(key) + r'\b'
                if re.search(pattern, sentence, re.IGNORECASE):
                    noisy_text = re.sub(pattern, val, sentence, count=1, flags=re.IGNORECASE)
                    success = True
                    break

        elif error_type == 'terminology':
            for wrong_form, right_form in TERMINOLOGY_MAP.items():
                if right_form in sentence:
                    noisy_text = sentence.replace(right_form, wrong_form, 1)
                    success = True
                    break

        elif error_type == 'punctuation':
            if sentence.endswith('.'):
                noisy_text = sentence[:-1]
                success = True
            elif ',' in sentence:
                noisy_text = sentence.replace(',', '', 1)
                success = True

        elif error_type == 'grammar':
            words = sentence.split()
            valid_indices = [i for i, w in enumerate(words) if w.lower() in GRAMMAR_WORDS]
            if valid_indices:
                idx = random.choice(valid_indices)
                words.pop(idx)
                noisy_text = " ".join(words)
                success = True

        elif error_type == 'typographic':
            space_applied = False
            for key, val in SPACE_ERRORS.items():
                if key in sentence:
                    noisy_text = sentence.replace(key, val, 1)
                    success = True
                    space_applied = True
                    break

            if not space_applied:
                words = sentence.split()
                indices = list(range(len(words)))
                random.shuffle(indices)
                for idx in indices:
                    word = words[idx]
                    if len(word) >= 5 and word.isalpha():
                        char_list = list(word)
                        pos = random.randint(0, len(char_list) - 1)
                        sub_type = random.choice(['omit', 'insert', 'trans', 'sub'])

                        if sub_type == 'omit':
                            char_list.pop(pos)
                        elif sub_type == 'insert':
                            char_list.insert(pos, random.choice('abcde'))
                        elif sub_type == 'trans' and pos < len(char_list) - 1:
                            char_list[pos], char_list[pos + 1] = char_list[pos + 1], char_list[pos]
                        elif sub_type == 'sub':
                            char = char_list[pos].lower()
                            char_list[pos] = random.choice(KEYBOARD_NEIGHBORS.get(char, 'xyz'))

                        words[idx] = "".join(char_list)
                        noisy_text = " ".join(words)
                        success = True
                        break

        return noisy_text, success


# ==================== 4. ANA İŞLEME ====================
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config(current_dir)

    input_path = os.path.abspath(os.path.join(current_dir, 'dataset_augmented.json'))

    if not os.path.exists(input_path):
        print(f"❌ HATA: Veri seti bulunamadı -> {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sentences = data['sentences']
    random.shuffle(sentences)

    # Veri setindeki tüm cümleleri kullanıyoruz
    total_target = len(sentences)
    noise_ratio = config.get('noise_ratio', 0.60)
    target_noisy_total = int(total_target * noise_ratio)

    # 🚀 DÜZELTME: Kotaları tamamen noise_config.json'a göre dinamik hesapla!
    error_types_config = config.get('error_types', {})
    target_classes = list(error_types_config.keys())

    class_quotas = {}
    for cls, ratio in error_types_config.items():
        # Örneğin: 8400 * 0.166 = ~1394 kota belirler
        class_quotas[cls] = int(target_noisy_total * ratio)

    gen = BalancedMultiNoiseGenerator(target_classes)
    processed_pairs = []

    print(f"🚀 Dinamik Veri Seti Algılandı: {total_target} cümle.")
    print(f"🚀 Çoklu Hata Enjeksiyonu Başlıyor (Hedef Gürültü: {target_noisy_total})...")

    for cls in target_classes:
        print(f"   - {cls.upper()} Hedef Kota: {class_quotas[cls]}")

    sentence_idx = 0
    loop_count = 0

    # 1. Hatalı Cümleleri Üret
    while any(gen.stats[cls] < class_quotas[cls] for cls in target_classes):

        if sentence_idx >= len(sentences):
            sentence_idx = 0
            random.shuffle(sentences)
            loop_count += 1
            if loop_count > 50:
                print("\n⚠️ Uyarı: Kotalar dolmakta zorlanıyor, sonsuz döngü kilidi devreye girdi!")
                break

        raw_s = sentences[sentence_idx]
        sentence_idx += 1

        standardized_target = gen.apply_standardization(raw_s)
        noisy_text = standardized_target
        applied_labels = []

        num_errors_to_apply = random.randint(1, 3)

        # Sadece kotası henüz dolmamış sınıflardan seçim yap!
        needed_classes = [cls for cls in target_classes if gen.stats[cls] < class_quotas[cls]]
        random.shuffle(needed_classes)

        for err_type in needed_classes:
            if len(applied_labels) >= num_errors_to_apply:
                break

            new_text, success = gen.apply_error(noisy_text, err_type)
            if success:
                noisy_text = new_text
                applied_labels.append(err_type)
                gen.stats[err_type] += 1

        if applied_labels:
            processed_pairs.append({
                "input": noisy_text,
                "target": standardized_target,
                "is_noisy": True,
                "error_types": applied_labels
            })

    print(f"\n✅ Gürültülü veriler tamamlandı. Şu anki miktar: {len(processed_pairs)}")
    print(f"🧹 Temiz (None) veriler eklenerek {total_target}'e tamamlanıyor...")

    # 2. Geri Kalan Cümleleri Temiz Olarak Ekle
    while len(processed_pairs) < total_target:
        if sentence_idx >= len(sentences):
            sentence_idx = 0
            random.shuffle(sentences)

        raw_s = sentences[sentence_idx]
        sentence_idx += 1
        standardized_target = gen.apply_standardization(raw_s)
        processed_pairs.append({
            "input": standardized_target,
            "target": standardized_target,
            "is_noisy": False,
            "error_types": ["none"]
        })

    output_file = os.path.join(current_dir, f'data_{total_target}_step11_multi_error_balanced.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_pairs, f, ensure_ascii=False, indent=2)

    print(f"\n🚀 İşlem Başarıyla Tamamlandı! -> {output_file}")

    all_final_labels = [label for p in processed_pairs if p['is_noisy'] for label in p['error_types']]
    final_stats = Counter(all_final_labels)
    clean_count = sum(1 for p in processed_pairs if not p['is_noisy'])

    print("\n✅ JSON'a YAZILAN Dağılım (Config Raporu):")
    for cls in target_classes:
        print(f"🔹 {cls.upper():<12}: {final_stats.get(cls, 0)} (Tam Hedef: {class_quotas[cls]})")

    print("-" * 30)
    print(f"🧹 TEMİZ (NONE) VERİ: {clean_count}")
    print(f"📊 TOPLAM VERİ ÇİFTİ : {len(processed_pairs)}")


if __name__ == "__main__":
    main()
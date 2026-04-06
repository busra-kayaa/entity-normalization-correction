import json
import random
import os


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, 'dataset_latest_2.json')
    output_path = os.path.join(current_dir, 'dataset_augmented.json')

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            sentences = data.get('sentences', [])
            print(f"📦 Orijinal cümle sayısı: {len(sentences)}")
    except FileNotFoundError:
        print("⚠️ dataset_latest_2.json bulunamadı! Lütfen ana veri setinin olduğundan emin ol.")
        return

    # 2. LEGO PARÇALARI (Combinatorial Elements)
    subjects = [
        "The committee", "Our organization", "The research team", "Several experts",
        "The local authorities", "Many international tourists", "A group of scientists",
        "The newly elected president", "My university professor", "The regional manager",
        "An independent journalist", "The historical society", "Some foreign investors"
    ]

    verbs = [
        "visited", "closely analyzed", "carefully studied", "conducted a survey about",
        "published an extensive report on", "investigated the situation in",
        "showed a great interest in", "organized a conference in", "reviewed the history of",
        "invested heavily in", "evaluated the resources of", "focused their attention on"
    ]

    contexts = [
        "recently.", "during the last decade.", "with great enthusiasm.",
        "in the latest scientific journal.", "quite thoroughly.", "for a new upcoming project.",
        "despite the financial crisis.", "multiple times.", "at the annual global summit.",
        "to understand the cultural impact.", "before the official announcement."
    ]

    # HEDEF KELİMELER
    tr_words = [
        "İstanbul", "İzmir", "Şanlıurfa", "Eskişehir", "Çanakkale", "Niğde", "Gümüşhane", "Muş", "Şırnak",
        "Kırşehir", "Boğaziçi", "Kadıköy", "Beşiktaş", "Nişantaşı", "Gaziantep", "Şişli", "Ağrı", "Balıkesir",
        "Diyarbakır", "Elazığ", "Kırıkkale", "Kütahya", "Kahramanmaraş", "Muğla", "Tekirdağ", "Zonguldak"
    ]

    term_words = [
        'Turkey', 'Burma', 'Swaziland', 'Holland', 'Czech Republic', 'Great Britain', 'Kiev', 'Bombay',
        'Calcutta', 'Madras', 'Peking', 'Canton', 'Zaire', 'Macedonia', 'Ceylon', 'Siam',
        'Rhodesia', 'Kampuchea', 'East Pakistan', 'Abyssinia', 'Persia', 'Mesopotamia'
    ]

    new_sentences = set()

    print("🧩 Lego parçaları birleştiriliyor...")

    # A) DEASCII İçin 2000 Benzersiz Cümle Üret
    while len(new_sentences) < 2000:
        s = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(tr_words)} {random.choice(contexts)}"
        new_sentences.add(s)

    # B) TERMINOLOGY İçin 2000 Benzersiz Cümle Üret
    term_sentences = set()
    while len(term_sentences) < 2000:
        s = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(term_words)} {random.choice(contexts)}"
        term_sentences.add(s)

    all_new = list(new_sentences) + list(term_sentences)
    random.shuffle(all_new)

    all_sentences = list(set(sentences + all_new))

    # 4. YENİ DOSYAYI KAYDET
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"sentences": all_sentences}, f, ensure_ascii=False, indent=4)

    print(f"✨ Üretilen YENİ ve TAMAMEN BENZERSİZ cümle sayısı: {len(all_new)}")
    print(f"🚀 TOPLAM GÜNCEL CÜMLE SAYISI: {len(all_sentences)}")
    print(f"✅ Yeni veri seti kaydedildi -> {output_path}")


if __name__ == "__main__":
    main()
import json
import random
import os
from collections import Counter

# ==================== KONFİGÜRASYON ====================
RANDOM_SEED = 42
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

random.seed(RANDOM_SEED)


def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, 'data_10000_step10.json')

    if not os.path.exists(input_path):
        print(f"❌ HATA: {input_path} bulunamadı!")
        return []

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✅ Veri yüklendi: {len(data)} cümle")
    return data


def split_data(pairs):
    total = len(pairs)
    indices = list(range(total))
    random.shuffle(indices)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_indices = indices[:train_end]
    val_indices = indices[train_end:val_end]
    test_indices = indices[val_end:]

    return [pairs[i] for i in train_indices], [pairs[i] for i in val_indices], [pairs[i] for i in test_indices]


def save_data(train, val, test):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = {'train.json': train, 'validation.json': val, 'test.json': test}
    for filename, content in files.items():
        with open(os.path.join(current_dir, filename), 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Kaydedilen dosyalar:")
    for f_name, f_content in files.items():
        print(f"   • {f_name}: {len(f_content)} cümle")


def analyze_split(train, val, test):
    total_all = len(train) + len(val) + len(test)

    # MD Raporu Başlangıcı
    md_report = f"# SPLİT RAPORU (Step 10 - 6 Class Hierarchy)\n\n"
    md_report += f"## 📊 Genel İstatistikler\n\n"
    md_report += f"- **Toplam cümle:** {total_all}\n"
    md_report += f"- **Train:** {len(train)} (%{len(train) / total_all * 100:.1f})\n"
    md_report += f"- **Validation:** {len(val)} (%{len(val) / total_all * 100:.1f})\n"
    md_report += f"- **Test:** {len(test)} (%{len(test) / total_all * 100:.1f})\n"
    md_report += f"- **Random seed:** {RANDOM_SEED}\n\n"
    md_report += f"## 🔍 Hata Tipi Dağılımı (Temiz Metinler Dahil)\n\n"

    print("\n" + "=" * 60)
    print("📊 FULL SPLİT İSTATİSTİKLERİ (None dahil)")
    print("=" * 60)

    for name, data_set in [('Train', train), ('Validation', val), ('Test', test)]:
        set_total = len(data_set)
        # 🚀 KRİTİK DEĞİŞİKLİK: Filtre kaldırıldı, tüm error_type'lar sayılıyor
        error_counts = Counter(item.get('error_type', 'none') for item in data_set)

        print(f"\n   {name} seti ({set_total} toplam cümle):")
        md_report += f"### {name} Seti ({set_total} toplam cümle)\n"

        # Dağılımı terminale ve MD rapora yazdır
        for err_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / set_total * 100) if set_total > 0 else 0
            print(f"      • {err_type}: {count} (%{percentage:.1f})")
            md_report += f"- **{err_type}:** {count} (%{percentage:.1f})\n"
        md_report += "\n"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'split_report.md'), 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f"\n📁 Rapor güncellendi: split_report.md")


def main():
    print("🚀 Veri seti bölme işlemi başlıyor...")
    pairs = load_data()
    if not pairs: return
    train, val, test = split_data(pairs)
    save_data(train, val, test)
    analyze_split(train, val, test)
    print("\n✅ İşlem tamamlandı!")


if __name__ == "__main__":
    main()
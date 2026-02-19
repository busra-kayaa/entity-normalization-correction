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
    """Veri setini yükle (train_data_step3.json)"""
    input_path = '../step3_noise_generation/train_data_step3.json'

    if not os.path.exists(input_path):
        input_path = 'train_data_step3.json'

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✅ Veri yüklendi: {len(data)} cümle")

    # Metadata bilgisi (varsa) yazdır
    noisy_count = sum(1 for item in data if item.get('is_noisy', False))
    print(f"   • Gürültülü cümle: {noisy_count} (%{noisy_count / len(data) * 100:.2f})")
    return data


def split_data(pairs):
    """Veriyi train/val/test olarak böl"""
    total = len(pairs)
    indices = list(range(total))
    random.shuffle(indices)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_indices = indices[:train_end]
    val_indices = indices[train_end:val_end]
    test_indices = indices[val_end:]

    train_data = [pairs[i] for i in train_indices]
    val_data = [pairs[i] for i in val_indices]
    test_data = [pairs[i] for i in test_indices]

    return train_data, val_data, test_data


def save_data(train, val, test):
    """Veriyi JSON dosyalarına kaydet"""
    with open('train.json', 'w', encoding='utf-8') as f:
        json.dump(train, f, ensure_ascii=False, indent=2)

    with open('validation.json', 'w', encoding='utf-8') as f:
        json.dump(val, f, ensure_ascii=False, indent=2)

    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(test, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Kaydedilen dosyalar:")
    print(f"   • train.json: {len(train)} cümle")
    print(f"   • validation.json: {len(val)} cümle")
    print(f"   • test.json: {len(test)} cümle")


def analyze_split(train, val, test):
    """Split istatistiklerini analiz et"""
    print("\n" + "=" * 60)
    print("📊 SPLİT İSTATİSTİKLERİ")
    print("=" * 60)

    total = len(train) + len(val) + len(test)
    print(f"\n📈 CÜMLE SAYILARI:")
    print(f"   • Train: {len(train)} (%{len(train) / total * 100:.1f})")
    print(f"   • Validation: {len(val)} (%{len(val) / total * 100:.1f})")
    print(f"   • Test: {len(test)} (%{len(test) / total * 100:.1f})")
    print(f"   • TOPLAM: {total}")

    # Hata tipi dağılımı kontrolü
    print(f"\n🔍 HATA TİPİ DAĞILIMI:")
    for name, data in [('Train', train), ('Validation', val), ('Test', test)]:
        error_counts = Counter()
        for item in data:
            if item.get('is_noisy'):
                err_type = item.get('error_type', 'unknown')
                error_counts[err_type] += 1

        total_noisy = sum(error_counts.values())
        print(f"\n   {name} seti ({total_noisy} gürültülü):")
        for err_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = count / total_noisy * 100 if total_noisy > 0 else 0
            print(f"      • {err_type}: {count} (%{percentage:.1f})")

    # Rapor dosyasına kaydet
    with open('split_report.md', 'w', encoding='utf-8') as f:
        f.write("# SPLİT RAPORU\n\n")
        f.write(f"## 📊 Genel İstatistikler\n")
        f.write(f"- Toplam cümle: {total}\n")
        f.write(f"- Train: {len(train)} (%{len(train) / total * 100:.1f})\n")
        f.write(f"- Validation: {len(val)} (%{len(val) / total * 100:.1f})\n")
        f.write(f"- Test: {len(test)} (%{len(test) / total * 100:.1f})\n")
        f.write(f"- Random seed: {RANDOM_SEED}\n")

    print(f"\n📁 Rapor kaydedildi: split_report.md")


def main():
    print("🚀 Veri seti bölme işlemi başlıyor...")
    print("=" * 60)

    pairs = load_data()
    train, val, test = split_data(pairs)
    save_data(train, val, test)
    analyze_split(train, val, test)

    print("\n" + "=" * 60)
    print("✅ İşlem tamamlandı!")


if __name__ == "__main__":
    main()
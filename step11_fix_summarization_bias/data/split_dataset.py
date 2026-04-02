import json
import random
import os
from collections import Counter

# ==================== KONFİGÜRASYON ====================
RANDOM_SEED = 42
TRAIN_RATIO = 0.80  # Standart Makine Öğrenmesi Dağılımı
VAL_RATIO = 0.10
TEST_RATIO = 0.10

random.seed(RANDOM_SEED)


def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Yeni çoklu hatalı dosyamız okunuyor
    input_path = os.path.join(current_dir, 'data_10000_step11_multi_error.json')

    if not os.path.exists(input_path):
        print(f"❌ HATA: {input_path} bulunamadı!")
        print("Lütfen önce noise_generator_multi.py scriptini çalıştırdığından emin ol.")
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
    # Büyük Dönüştürücü'nün (dataset_transformer.py) beklediği dosya isimleri
    files = {
        'mizan_6class_train.jsonl': train,
        'mizan_6class_validation.jsonl': val,
        'mizan_6class_test.jsonl': test
    }

    for filename, dataset in files.items():
        filepath = os.path.join(current_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in dataset:
                # Alpaca ve Büyük Dönüştürücü formatına uygun JSONL satırı
                alpaca_format = {
                    "input": item["input"],
                    "output": json.dumps({"correctedText": item["target"]}, ensure_ascii=False)
                }
                f.write(json.dumps(alpaca_format, ensure_ascii=False) + '\n')

    print(f"\n💾 Kaydedilen JSONL dosyaları (Dönüşüme Hazır):")
    for f_name, f_content in files.items():
        print(f"   • {f_name}: {len(f_content)} satır")


def analyze_split(train, val, test):
    total_all = len(train) + len(val) + len(test)

    # MD Raporu Başlangıcı
    md_report = f"# SPLİT RAPORU (Step 11 - Multi-Error 6 Class Hierarchy)\n\n"
    md_report += f"## 📊 Genel İstatistikler\n\n"
    md_report += f"- **Toplam cümle:** {total_all}\n"
    md_report += f"- **Train:** {len(train)} (%{len(train) / total_all * 100:.1f})\n"
    md_report += f"- **Validation:** {len(val)} (%{len(val) / total_all * 100:.1f})\n"
    md_report += f"- **Test:** {len(test)} (%{len(test) / total_all * 100:.1f})\n"
    md_report += f"- **Random seed:** {RANDOM_SEED}\n\n"
    md_report += f"## 🔍 Hata Tipi Dağılımı (Çoklu Hatalar ve Temiz Metinler Dahil)\n\n"

    print("\n" + "=" * 60)
    print("📊 FULL SPLİT İSTATİSTİKLERİ (Çoklu Hata Destekli)")
    print("=" * 60)

    for name, data_set in [('Train', train), ('Validation', val), ('Test', test)]:
        set_total = len(data_set)

        # 🚀 KRİTİK DEĞİŞİKLİK: error_types artık bir liste, hepsini düzleştirip sayıyoruz
        error_counts = Counter()
        for item in data_set:
            # Eğer error_types listesi yoksa ['none'] varsay
            for err in item.get('error_types', ['none']):
                error_counts[err] += 1

        print(f"\n   {name} seti ({set_total} toplam cümle):")
        md_report += f"### {name} Seti ({set_total} toplam cümle)\n"

        # Dağılımı terminale ve MD rapora yazdır
        for err_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            # Not: Bir cümlede birden fazla hata olabildiği için, yüzdeler toplamı %100'ü geçebilir.
            # Bu, "Cümlelerin yüzde kaçında bu hata var" anlamına gelir.
            percentage = (count / set_total * 100) if set_total > 0 else 0
            print(f"      • {err_type}: {count} (Cümlelerin %{percentage:.1f}'inde var)")
            md_report += f"- **{err_type}:** {count} (Cümlelerin %{percentage:.1f}'inde var)\n"
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
    print("\n✅ İşlem tamamlandı! Şimdi 'dataset_transformer.py' dosyasını çalıştırabilirsin.")


if __name__ == "__main__":
    main()
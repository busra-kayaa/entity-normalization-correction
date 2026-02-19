import json
import os
import pandas as pd

def find_word_diff(noisy_sent, correct_sent, error_type):
    """Cümle içindeki hatalı kelimeyi ve doğrusunu tespit eder."""
    n_words = noisy_sent.split()
    c_words = correct_sent.split()

    # 1. Normal Hatalar (Kelime sayısı değişmeyenler)
    if len(n_words) == len(c_words):
        for nw, cw in zip(n_words, c_words):
            if nw != cw:
                return nw, cw

    # 2. Boşluk Hataları (Space: "New York" -> "NewYork")
    if error_type == "space":
        for i in range(len(c_words) - 1):
            combined = c_words[i] + c_words[i + 1]
            for nw in n_words:
                if combined in nw:
                    return nw, f"{c_words[i]} {c_words[i + 1]}"

    return "Tespit Edilemedi", "Tespit Edilemedi"

def main():
    input_file = 'train_data_step3.json'
    output_folder = 'error_reports_xlsx'
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(input_file):
        print(f"❌ {input_file} bulunamadı!")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    analysis = []
    for item in data:
        if item.get('is_noisy'):
            err_type = item.get('error_type')
            n_word, c_word = find_word_diff(item['input'], item['target'], err_type)

            analysis.append({
                "Hata Türü": err_type,
                "Hatalı Kelime": n_word,
                "Doğru Kelime": c_word,
                "Gürültülü Cümle": item['input'],
                "Doğru Cümle": item['target']
            })

    df = pd.DataFrame(analysis)

    # 1. TÜMÜNÜ EXCEL OLARAK KAYDET
    full_report_path = f"{output_folder}/full_error_report.xlsx"
    df.to_excel(full_report_path, index=False)
    print(f"✅ Toplu Excel raporu oluşturuldu: {full_report_path}")

    # 2. AYRI AYRI EXCEL OLARAK KAYDET
    print("\n--- 📂 Excel Dosyaları Oluşturuluyor ---")
    for err_type in df["Hata Türü"].unique():
        type_df = df[df["Hata Türü"] == err_type]
        filename = f"{output_folder}/{err_type}_errors.xlsx"
        type_df.to_excel(filename, index=False)
        print(f"✅ Kaydedildi: {filename} ({len(type_df)} örnek)")

if __name__ == "__main__":
    main()
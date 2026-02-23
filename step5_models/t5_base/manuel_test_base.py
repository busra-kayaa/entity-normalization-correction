import torch
import os
import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
from datetime import datetime
from pathlib import Path


def test_t5_expanded_and_save():
    # 1. Klasör ve Yol Ayarları
    current_file_path = Path(__file__).resolve()
    t5_base_folder = current_file_path.parent

    # Raporların kaydedileceği klasör
    reports_dir = t5_base_folder / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Model Yolu
    model_path = r"C:\Users\Busra\entity_normalization\step5_models\t5_base\final_t5_base_model"

    # Çıktı Dosya Yolları (reports klasörü içine)
    output_excel = reports_dir / "expanded_manuel_test_base_results.xlsx"
    output_text = reports_dir / "expanded_manuel_test_base_report.txt"

    if not os.path.exists(model_path):
        print(f"❌ Hata: Model yolu bulunamadı! {model_path}")
        return

    print("🔄 Model ve Tokenizer yükleniyor...")
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    # 2. Genişletilmiş Test Verileri
    test_cases = [
        ("The Republic of Turkey was founded in 1923.", "The Republic of Türkiye was founded in 1923."),
        ("Tourism in turkey is growing fast.", "Tourism in Türkiye is growing fast."),
        ("Made in Turkey", "Made in Türkiye"),
        ("Istanbul very good.", "İstanbul very good."),
        ("The goverment of Türkiye is here.", "The government of Türkiye is here."),
        ("I recieved a new message.", "I received a new message."),
        ("The enviroment protection is key.", "The environment protection is key."),
        ("Natural languge processing is fun.", "Natural language processing is fun."),
        ("NewYork is a crowded place.", "New York is a crowded place."),
        ("He said , hello.", "He said, hello."),
        ("We live in Türkiye.", "We live in Türkiye."),
        ("The weather is nice today.", "The weather is nice today."),
        ("Artificial intelligence is the future.", "Artificial intelligence is the future.")
    ]

    results_list = []
    correct_count = 0

    print("\n🚀 Test Başlatıldı...\n" + "=" * 75)

    for input_raw, target in test_cases:
        input_text = "gec: " + input_raw
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True).to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=128,
                num_beams=5,
                early_stopping=True
            )

        predicted = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        is_correct = predicted.lower() == target.lower().strip()

        if is_correct:
            correct_count += 1
            status = "✅ DOĞRU"
        else:
            status = "❌ YANLIŞ"

        results_list.append({
            "Girdi": input_raw,
            "Beklenen": target,
            "Model Tahmini": predicted,
            "Durum": "DOĞRU" if is_correct else "YANLIŞ"
        })

        print(f"Girdi  : {input_raw}")
        print(f"Tahmin : {predicted} ({status})")
        print("-" * 75)

    # 3. İstatistikler ve Kayıt
    total = len(test_cases)
    accuracy = (correct_count / total) * 100
    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Excel Kaydet
    df = pd.DataFrame(results_list)
    df.to_excel(output_excel, index=False)

    # Metin Raporu Kaydet
    report_text = f"""
==================================================
      GENİŞLETİLMİŞ MANUEL TEST RAPORU (T5-BASE)
==================================================
Tarih: {report_time}
Toplam Test Sayısı: {total}
Doğru Tahmin: {correct_count}
Başarı Oranı: %{accuracy:.2f}

---------------- DETAYLAR -----------------------
"""
    for res in results_list:
        report_text += f"\nGirdi    : {res['Girdi']}\nBeklenen : {res['Beklenen']}\nTahmin   : {res['Model Tahmini']}\nDurum    : {res['Durum']}\n{'-' * 40}\n"

    with open(output_text, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n✅ Test tamamlandı!")
    print(f"📊 Başarı Oranı: %{accuracy:.2f}")
    print(f"💾 Raporlar şuraya kaydedildi: {reports_dir}")


if __name__ == "__main__":
    test_t5_expanded_and_save()
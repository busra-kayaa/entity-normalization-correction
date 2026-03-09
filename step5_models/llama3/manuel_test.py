import torch
import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from pathlib import Path
from datetime import datetime


def test_llama3_manual_categorized():
    # 1. Klasör ve Yol Ayarları
    base_model_id = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
    lora_path = "./final_llama3_lora"

    reports_dir = Path("./reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    output_excel = reports_dir / "llama3_manual_test_results.xlsx"
    output_text = reports_dir / "llama3_manual_test_report.txt"

    if not os.path.exists(lora_path):
        print(f"❌ Hata: LoRA ağırlıkları bulunamadı! Lütfen yolu kontrol et: {lora_path}")
        return

    # 2. Modeli 4-bit ve LoRA ile Yükleme
    print("🔄 1/3: Llama 3.1 Temel Modeli 4-bit olarak yükleniyor...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    # Llama 3 durma tokenleri
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )

    print("🔄 2/3: Eğittiğin LoRA adaptörleri (Beyin) modele entegre ediliyor...")
    model = PeftModel.from_pretrained(base_model, lora_path)
    model.eval()

    # 3. Test Senaryoları (mBART ile birebir aynı)
    test_cases = [
        ("Turkiye is a bridge between Europe and Asia.", "Türkiye is a bridge between Europe and Asia.", "deascii"),
        ("TURKIYE is now the official name.", "Türkiye is now the official name.", "deascii"),
        ("We are going to Istanbul for the summit.", "We are going to İstanbul for the summit.", "deascii"),
        ("The weather in Izmir is very hot.", "The weather in İzmir is very hot.", "deascii"),
        ("Besiktas won the match last night.", "Beşiktaş won the match last night.", "deascii"),
        ("President Erdogan will visit the site.", "President Erdoğan will visit the site.", "deascii"),
        ("The flight was from London to Turkey.", "The flight was from London to Türkiye.", "terminology"),
        ("The government of Burma is under pressure.", "The government of Myanmar is under pressure.", "terminology"),
        ("Swaziland has changed its name to Eswatini.", "Eswatini has changed its name to Eswatini.", "terminology"),
        ("President Erdğan will speak soon.", "President Erdoğan will speak soon.", "omission"),
        ("The Prsident made a choice.", "The President made a choice.", "omission"),
        ("The poliitcal situation is unstable.", "The political situation is unstable.", "insertion"),
        ("Irsaeli officials reported the news.", "Israeli officials reported the news.", "transposition"),
        ("Sülyeman visited the office.", "Süleyman visited the office.", "transposition"),
        ("The Taliban is in control of Takiban.", "The Taliban is in control of Taliban.", "substitution"),
        ("Ankara and Abkara are different.", "Ankara and Ankara are different.", "substitution"),
        ("NewYork is the city that never sleeps.", "New York is the city that never sleeps.", "space"),
        ("AbdullahGul was the former president.", "Abdullah Gül was the former president.", "space"),
        ("I did not recieve your email.", "I did not receive your email.", "common"),
        ("The goverment announced a new policy.", "The government announced a new policy.", "common"),
        ("The enviroment is our priority.", "The environment is our priority.", "common"),
        ("The month of May is beautiful.", "The month of May is beautiful.", "none"),
        ("Bill is a common name in the US.", "Bill is a common name in the US.", "none"),
        ("The weather in London is rainy today.", "The weather in London is rainy today.", "none"),
        ("This is a correctly written English sentence.", "This is a correctly written English sentence.", "none")
    ]

    results_list = []
    category_stats = {}

    print(f"\n🧪 3/3: {len(test_cases)} manuel senaryo Llama 3.1 ile test ediliyor...\n" + "=" * 80)

    for input_raw, target, category in test_cases:
        if category not in category_stats:
            category_stats[category] = {"total": 0, "correct": 0}

        # Llama 3 Prompt Formatı
        prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Please correct the typographical, de-asciification, and terminology errors in the following text. Do not add any extra comments.
Text: {input_raw.strip()}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=128,
                eos_token_id=terminators,
                temperature=0.1,  # Doğruluk için düşük tutuyoruz
                do_sample=True
            )

        # Sadece asistanın ürettiği yeni tokenleri al (Prompt'u kesip at)
        input_length = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_length:]
        predicted = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

        is_correct = predicted.lower() == target.lower().strip()

        category_stats[category]["total"] += 1
        if is_correct:
            category_stats[category]["correct"] += 1

        results_list.append({
            "Kategori": category.upper(),
            "Girdi": input_raw,
            "Beklenen": target,
            "Tahmin": predicted,
            "Durum": "✅ DOĞRU" if is_correct else "❌ YANLIŞ"
        })

        print(f"[{category.upper()}] Girdi: {input_raw}")
        print(f"Tahmin: {predicted} {'✅' if is_correct else '❌'}")
        print("-" * 80)

    summary_list = []
    for cat, stats in category_stats.items():
        acc = (stats["correct"] / stats["total"]) * 100
        summary_list.append({"Hata Türü": cat.upper(), "Toplam": stats["total"], "Doğru": stats["correct"],
                             "Başarı (%)": f"%{acc:.2f}"})

    df_results = pd.DataFrame(results_list)
    df_summary = pd.DataFrame(summary_list)

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name="Test Detayları", index=False)
        df_summary.to_excel(writer, sheet_name="Kategori Özeti", index=False)

    total_accuracy = (df_summary["Doğru"].sum() / df_summary["Toplam"].sum()) * 100

    report_header = f"""
==================================================
      LLAMA 3.1 QLORA MANUEL TEST KATEGORİ RAPORU
==================================================
Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Genel Accuracy: %{total_accuracy:.2f}

---------------- KATEGORİ ÖZETİ ------------------
{df_summary.to_string(index=False)}
==================================================
"""
    with open(output_text, "w", encoding="utf-8") as f:
        f.write(report_header + "\n\nDETAYLI TEST LİSTESİ:\n" + df_results.to_string(index=False))

    print(report_header)
    print(f"✅ Test tamamlandı. Raporlar kaydedildi: {reports_dir}")


if __name__ == "__main__":
    test_llama3_manual_categorized()
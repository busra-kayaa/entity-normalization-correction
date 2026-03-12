import json
import torch
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from sklearn.metrics import precision_recall_fscore_support
import datetime
import nltk
from nltk.translate.gleu_score import sentence_gleu
from jiwer import cer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def test_llama3_advanced_json_local():
    base_model_id = "unsloth/Meta-Llama-3.1-8B-bnb-4bit"
    lora_path = "./lora_adaptorum"
    data_path = "./test.json"

    reports_dir = Path("./reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    excel_output = reports_dir / "llama3_advanced_results.xlsx"
    text_report = reports_dir / "llama3_advanced_report.txt"

    if not os.path.exists(lora_path):
        print(f"❌ HATA: LoRA ağırlıkları bulunamadı! Yol: {lora_path}")
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🔄 Llama 3.1 ve Adaptörler Yükleniyor... (Donanım: {device.upper()})")

    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4",
                                    bnb_4bit_compute_dtype=torch.bfloat16)
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_id, quantization_config=bnb_config, device_map="auto")

    model = PeftModel.from_pretrained(base_model, lora_path)
    model.eval()

    with open(data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    all_results, y_true, y_pred, cer_scores, gleu_scores = [], [], [], [], []
    oc_count, none_total, none_correct = 0, 0, 0

    system_instruction = (
        "You are an expert text normalization and error correction AI. "
        "Correct any spelling, grammar, punctuation, and specific entity terminology errors in the text. "
        "Apply standard entity normalization rules (e.g., 'Turkey' to 'Türkiye'). "
        "If the input is already correct, return it exactly as is."
    )
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:\n"""

    print(f"🧪 {len(test_data)} örnek üzerinde Llama 3.1 analizi başlatıldı...")
    for item in tqdm(test_data):
        original_input = item["input"].strip()
        ground_truth = item["target"].strip()
        error_type = str(item.get("error_type", "genel")).lower().strip()

        prompt = alpaca_prompt.format(system_instruction, original_input)
        inputs = tokenizer([prompt], return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, use_cache=True, temperature=0.1)

        decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        predicted_text = decoded_output.split("### Response:\n")[-1].strip()

        y_true.append(ground_truth.lower())
        y_pred.append(predicted_text.lower())

        cer_val = cer(ground_truth.lower(), predicted_text.lower())
        cer_scores.append(cer_val)

        ref_tokens = nltk.word_tokenize(ground_truth.lower())
        pred_tokens = nltk.word_tokenize(predicted_text.lower())
        gleu_val = sentence_gleu([ref_tokens], pred_tokens)
        gleu_scores.append(gleu_val)

        is_match = predicted_text.lower() == ground_truth.lower()
        if error_type == "none":
            none_total += 1
            if is_match:
                none_correct += 1
            else:
                oc_count += 1

        all_results.append(
            {"Hata Türü": error_type.upper(), "Girdi": original_input, "Hedef": ground_truth, "Tahmin": predicted_text,
             "Durum": "BAŞARILI" if is_match else "HATALI", "CER": round(cer_val, 4), "GLEU": round(gleu_val, 4)})

    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    accuracy = (sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)) * 100

    report_content = f"""
==================================================
      GELİŞMİŞ METRİK RAPORU (Llama 3.1 Alpaca)
==================================================
Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 Accuracy (Tam Eşleşme): %{accuracy:.2f}
🏆 F1-Score: {f1:.4f}
📉 Avg CER: {sum(cer_scores) / len(cer_scores) if cer_scores else 0:.4f}
🧩 Avg GLEU: {sum(gleu_scores) / len(gleu_scores) if gleu_scores else 0:.4f}
⚠️ Over-Correction Rate: %{(oc_count / none_total * 100) if none_total > 0 else 0:.2f}
==================================================
"""
    with open(text_report, "w", encoding="utf-8") as f:
        f.write(report_content)
    pd.DataFrame(all_results).to_excel(excel_output, index=False)
    print(report_content)


if __name__ == "__main__":
    test_llama3_advanced_json_local()
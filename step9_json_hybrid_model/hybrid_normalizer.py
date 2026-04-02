import os
import sys
import json
import torch

ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ana_dizin not in sys.path:
    sys.path.append(ana_dizin)

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

from step9_json_hybrid_model.rule_based_layer import RuleBasedCorrector


class HybridPipeline:
    def __init__(self, base_model_id="unsloth/Meta-Llama-3.1-8B-bnb-4bit"):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        lora_path = os.path.join(current_dir, "mizan_multi_label_v2")

        print("⚙️ 1. Katman: Regex Motoru Yükleniyor...")
        self.regex_layer = RuleBasedCorrector()

        print(f"🧠 2. Katman: Llama 3.1 v2 Yükleniyor... (Yol: {lora_path})")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        self.tokenizer = AutoTokenizer.from_pretrained(base_model_id)
        base_model = AutoModelForCausalLM.from_pretrained(base_model_id, quantization_config=bnb_config,
                                                          device_map="auto")
        self.model = PeftModel.from_pretrained(base_model, lora_path)
        self.model.eval()

        self.prompt_template = """You are an expert text correction system. Correct the input text and provide a detailed JSON analysis.
Use ONLY these 8 error types: "deascii", "omission", "insertion", "transposition", "substitution", "space", "terminology", "common".

### Input:
{}

### Response:
"""
        print("✅ Mizan v2 Hibrit Sistem (Zero-Shot JSON Mode) Hazır!")

    def normalize_text(self, text):
        regex_result, regex_corrections = self.regex_layer.process(text)

        prompt = self.prompt_template.format(regex_result)
        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=512, temperature=0.1,
                                          pad_token_id=self.tokenizer.eos_token_id)

        decoded_output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

        try:
            raw_json_str = decoded_output.split("### Response:\n")[-1].strip()
            if "```json" in raw_json_str:
                raw_json_str = raw_json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_json_str:
                raw_json_str = raw_json_str.split("```")[1].split("```")[0].strip()

            result_data = json.loads(raw_json_str)
            ai_corrections = result_data.get("corrections", [])
            final_corrected_text = result_data.get("correctedText", regex_result)
        except (json.JSONDecodeError, IndexError):
            ai_corrections = []
            final_corrected_text = regex_result

        # Regex ve AI bulgularını birleştir ve tekilleştir
        all_corrections = regex_corrections + ai_corrections
        seen_words = set()
        unique_corrections = []
        for c in all_corrections:
            orig_word = c.get("original", "")
            if orig_word and orig_word not in seen_words:
                unique_corrections.append(c)
                seen_words.add(orig_word)

        return {
            "originalText": text,
            "correctedText": final_corrected_text,
            "corrections": unique_corrections
        }


# ==================== TEST AŞAMASI ====================
if __name__ == "__main__":
    pipeline = HybridPipeline()

    test_text = "Prezident Erdogan visited Istanbul after the meetings in Burma."

    print("\n" + "=" * 50)
    print(f"❌ Orijinal Metin : {test_text}")
    print("=" * 50)

    sonuc = pipeline.normalize_text(test_text)

    print("✅ MİZAN V2 JSON ÇIKTISI:")
    print(json.dumps(sonuc, indent=4, ensure_ascii=False))
    print("=" * 50)
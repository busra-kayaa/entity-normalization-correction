import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from step7_hybrid_model.rule_based_layer import RuleBasedCorrector


class HybridPipeline:
    def __init__(self, base_model_id="unsloth/Meta-Llama-3.1-8B-bnb-4bit"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lora_path = os.path.join(current_dir, "mizan_multi_label_model")

        print("⚙️ 1. Katman: Regex Motoru Yükleniyor...")
        self.regex_layer = RuleBasedCorrector()

        print(f"🧠 2. Katman: Llama 3.1 (Multi-Label) Yükleniyor... (Yol: {lora_path})")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        self.tokenizer = AutoTokenizer.from_pretrained(base_model_id)
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            quantization_config=bnb_config,
            device_map="auto"
        )

        self.model = PeftModel.from_pretrained(base_model, lora_path)
        self.model.eval()

        self.prompt_template = """Aşağıdaki hatalı metni profesyonelce düzelt ve bulduğun TÜM farklı hata türlerini bir liste (array) olarak belirt. 
Yanıtını mutlaka şu JSON formatında ver: {{"corrected": "...", "error_types": ["hata1", "hata2"]}}

### Giriş:
{}

### Yanıt:
"""
        print("✅ Mizan Hibrit Sistem (Regex + Multi-Label AI) Hazır!\n" + "=" * 65)

    def normalize_text(self, text):
        # --- AŞAMA 1: REGEX (Kesin kurallar) ---
        regex_result, applied_rules = self.regex_layer.process(text)

        # --- AŞAMA 2: LLAMA (Bağlamsal düzeltme ve çoklu teşhis) ---
        prompt = self.prompt_template.format(regex_result)
        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                use_cache=True,
                temperature=0.1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        decoded_output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

        try:
            raw_json_str = decoded_output.split("### Yanıt:\n")[-1].strip()
            result_data = json.loads(raw_json_str)

            final_corrected = result_data.get("corrected", regex_result)
            llama_errors = result_data.get("error_types", [])

            if isinstance(llama_errors, str):
                llama_errors = [llama_errors]

        except (json.JSONDecodeError, IndexError):
            print(f"⚠️ Kritik Hata: JSON formatı bozuldu! Çıktı: {decoded_output[:100]}...")
            final_corrected = regex_result
            llama_errors = ["ai_parsing_error"]

        tum_hatalar = list(set(applied_rules + llama_errors))

        return {
            "orijinal": text,
            "final_sonuc": final_corrected,
            "tespit_edilen_hatalar": tum_hatalar
        }


# ==================== TEST DÖNGÜSÜ ====================
if __name__ == "__main__":
    pipeline = HybridPipeline()

    test_sentences = [
        "The economy of turkey is growing fastly.",  # Terminology + Grammar
        "President Erdogan visited Istanbul today.",  # Regex kuralları
        "They signed a new deal in Burma last week",  # Regex (Myanmar) + AI (Punctuation)
        "Prezident Barrack Obamma met with Chancelor Angela Merkal in Berln to discuss the Europeen Union's econimic policies."
    ]

    for i, sentence in enumerate(test_sentences, 1):
        print(f"🧪 Test {i}")
        sonuc = pipeline.normalize_text(sentence)

        print(f"❌ Orijinal       : {sonuc['orijinal']}")
        print(f"✅ Final Düzeltme : {sonuc['final_sonuc']}")
        print(f"🏷️ Tespit Edilen  : {sonuc['tespit_edilen_hatalar']}")
        print("-" * 65)
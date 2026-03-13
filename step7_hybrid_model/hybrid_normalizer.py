import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from rule_based_layer import RuleBasedCorrector  # Senin yazdığın o harika Regex kas gücü!


class HybridPipeline:
    def __init__(self, base_model_id="unsloth/Meta-Llama-3.1-8B-bnb-4bit"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lora_path = os.path.join(current_dir, "lora_adaptorum")

        print("⚙️ 1. Katman: Kural Tabanlı (Regex) Motor Yükleniyor...")
        self.regex_layer = RuleBasedCorrector()

        print(f"🧠 2. Katman: Llama 3.1 Yapay Zeka Beyni Yükleniyor... (Yol: {lora_path})")
        print("⏳ Bu işlem bilgisayarın donanımına göre 1-2 dakika sürebilir, lütfen bekleyin...\n")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 4-bit yükleme ayarları (Ekran kartını yormamak için)
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

        # Eğitimde kullandığımız sihirli Alpaca şablonumuz
        self.system_instruction = (
            "You are an expert text normalization and error correction AI. "
            "Correct any spelling, grammar, punctuation, and specific entity terminology errors in the text. "
            "Apply standard entity normalization rules (e.g., 'Turkey' to 'Türkiye'). "
            "If the input is already correct, return it exactly as is."
        )
        self.prompt_template = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:\n"""

        print("✅ Hibrit Sistem (Regex + Llama) Tamamen Hazır!\n" + "=" * 65)

    def normalize_text(self, text):
        # --- AŞAMA 1: REGEX (Temizlik) ---
        regex_result, applied_rules = self.regex_layer.process(text)

        # --- AŞAMA 2: LLAMA (Ütüleme ve Bağlam) ---
        prompt = self.prompt_template.format(self.system_instruction, regex_result)
        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                use_cache=True,
                temperature=0.1  # Net ve ezberci cevaplar için düşük sıcaklık
            )

        decoded_output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        final_text = decoded_output.split("### Response:\n")[-1].strip()

        return {
            "orijinal": text,
            "regex_sonrasi": regex_result,
            "regex_kurallari": applied_rules,
            "final_sonuc": final_text
        }


# ==================== UÇTAN UCA TEST ====================
if __name__ == "__main__":
    pipeline = HybridPipeline()

    # Her iki katmanın da sınırlarını zorlayacak, projemizin özeti olan 3 cümle:
    test_sentences = [
        "President Erdogan met with Irsaeli officials in Istanbul to discuss the poliitcal crisis.",
        "The economy of turkey is growing fastly.",
        # Llama'nın bağlamı (hindi vs ülke) anlayıp anlamayacağını test ediyoruz!
        "They signed a new deal in Burma last week",  # Regex isimi değiştirip, Llama da sonuna noktayı koyacak.
        "Prezident Barrack Obamma met with Chancelor Angela Merkal in Berln to discuss the Europeen Union's econimic policies. The meting was held at the Bundestg building, where they also adressed the situaton in Ukrain and the role of the Untied Nations."
    ]

    for i, sentence in enumerate(test_sentences, 1):
        print(f"🧪 Test {i}")
        sonuc = pipeline.normalize_text(sentence)

        print(f"❌ Orijinal       : {sonuc['orijinal']}")
        print(f"🧹 1. Katman (Rx) : {sonuc['regex_sonrasi']} (Tetiklenenler: {sonuc['regex_kurallari']})")
        print(f"🧠 2. Katman (AI) : {sonuc['final_sonuc']}")
        print("-" * 65)
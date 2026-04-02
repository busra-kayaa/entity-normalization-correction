import os
import sys
import json
from llama_cpp import Llama

# 1. Klasör Yolunu Ayarlama (Step 10'u bulabilmesi için)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Step 10 klasöründeki hiyerarşik kural motorunu çekiyoruz
try:
    from step10_hierarchical_6class.rule_based_layer import RuleBasedCorrector

    print("🎯 Step 10: RuleBasedCorrector başarıyla entegre edildi.")
except ImportError as e:
    print(f"⚠️ Hata: RuleBasedCorrector yüklenemedi! {e}")
    RuleBasedCorrector = None

# 2. Orijinal Alpaca Eğitim Promptu
ALPACA_PROMPT = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""


class MizanV3Step10Pipeline:
    def __init__(self, gguf_path="Mizan_V3_Final_Model.gguf"):
        # Regex Katmanı (Hiyerarşik Kurallar)
        self.regex_layer = RuleBasedCorrector() if RuleBasedCorrector else None

        # GGUF Katmanı (Neural Engine)
        print(f"🧠 Mizan V3 GGUF Yükleniyor... ({gguf_path})")
        self.model = Llama(
            model_path=gguf_path,
            n_gpu_layers=-1,  # GPU varsa tam kapasite kullanır
            n_ctx=2048,
            n_threads=8,  # Monster işlemci çekirdek sayısı
            verbose=False
        )

        # Eğitimde kullandığın sistem talimatı
        self.system_instruction = (
            "You are an expert text correction system. Correct the input text and provide a detailed JSON analysis. "
            "Use ONLY these error types: 'deascii', 'omission', 'insertion', 'transposition', 'substitution', 'space', 'terminology', 'common'."
        )

    def normalize_text(self, text):
        # --- KATMAN 1: Step 10 Regex Motoru ---
        regex_result = text
        regex_corrections = []
        if self.regex_layer:
            # Senin hiyerarşik kuralların burada devreye giriyor
            regex_result, regex_corrections = self.regex_layer.process(text)

        # --- KATMAN 2: Alpaca Prompt Hazırlığı ---
        prompt = ALPACA_PROMPT.format(
            self.system_instruction,
            regex_result,
            ""  # Response kısmı boş kalıyor
        )

        # --- KATMAN 3: Llama Çıkarımı ---
        output = self.model(
            prompt,
            max_tokens=512,
            stop=["###", "</s>"],
            temperature=0.1
        )

        raw_response = output["choices"][0]["text"].strip()

        # --- KATMAN 4: JSON Ayıklama ve Birleştirme ---
        try:
            # JSON bloğunu metnin içinden cımbızlıyoruz
            start_idx = raw_response.find("{")
            end_idx = raw_response.rfind("}")
            if start_idx != -1 and end_idx != -1:
                raw_json_str = raw_response[start_idx:end_idx + 1]
                ai_data = json.loads(raw_json_str)
                ai_corrections = ai_data.get("corrections", [])
                final_text = ai_data.get("correctedText", regex_result)
            else:
                raise ValueError("JSON formatı bozuk")
        except (json.JSONDecodeError, ValueError):
            ai_corrections = []
            final_text = regex_result

        # İki katmanın bulgularını birleştir ve tekilleştir
        all_corrections = regex_corrections + ai_corrections

        return {
            "originalText": text,
            "correctedText": final_text,
            "corrections": self._unique_results(all_corrections)
        }

    def _unique_results(self, corrections):
        seen = set()
        unique = []
        for c in corrections:
            # Hem kelime hem hata tipi bazında kontrol
            key = (c.get("original", "").lower(), c.get("type", ""))
            if key not in seen:
                unique.append(c)
                seen.add(key)
        return unique


# ==================== MİZAN TEST ====================
if __name__ == "__main__":
    # GGUF dosyan bu dosya ile aynı dizinde olmalı
    mizan_v3 = MizanV3Step10Pipeline(gguf_path="Mizan_V3_Final_Model.gguf")

    test_text = "Prezident Erdogan visited Istanbul after the meetings in Burma."

    print("\n" + "=" * 50)
    print(f"📝 GİRİŞ: {test_text}")
    print("=" * 50)

    sonuc = mizan_v3.normalize_text(test_text)

    print("🎯 MİZAN V3 HİBRİT ÇIKTI (Step 10 Kuralları Dahil):")
    print(json.dumps(sonuc, indent=4, ensure_ascii=False))
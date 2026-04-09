import os
import sys
import json
import re
from llama_cpp import Llama
from difflib import SequenceMatcher

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from step10_hierarchical_6class.rule_based_layer import RuleBasedCorrector
    print("✅ Step 10: RuleBasedCorrector (Regex Layer) başarıyla bağlandı.")
except ImportError:
    print("⚠️ Uyarı: RuleBasedCorrector bulunamadı, sistem sadece Neural modda çalışacak.")
    RuleBasedCorrector = None


class MizanV4HybridPipeline:
    def __init__(self, gguf_path="Meta-Llama-3.1-8B.Q4_K_M.gguf"):
        self.regex_layer = RuleBasedCorrector() if RuleBasedCorrector else None

        print(f"🧠 Mizan V4 Neural Engine Yükleniyor... ({gguf_path})")
        self.model = Llama(
            model_path=gguf_path,
            n_gpu_layers=-1,
            n_ctx=2048,
            n_threads=8,
            verbose=False
        )

        self.system_instruction = (
            "You are an expert text correction system. Fix ALL errors and output JSON. "
            "SEQUENTIAL ORDER RULE: List corrections in the EXACT order they appear. "
            "STRICT ATOMIC RULE: Split corrections into single words or punctuation marks. DO NOT group multiple words together. "
            "If a word or punctuation is missing, use an empty string '' as the original text."
        )

    def _build_prompt(self, text):
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{self.system_instruction}

### Input:
{text}

### Response:
"""

    def _determine_error_type(self, original, corrected, is_start_of_sentence=False):
        """Hata türlerini benzerlik oranına ve bağlama göre akıllıca sınıflandıran fonksiyon"""
        orig_l = original.lower() if original else ""
        corr_l = corrected.lower() if corrected else ""

        # 0. SADECE BÜYÜK/KÜÇÜK HARF FARKI VARSA
        if orig_l == corr_l and original != corrected:
            if not is_start_of_sentence:
                return "terminology"  # Özel isim büyütülmüş
            else:
                return "capitalization"  # Sadece cümle başı büyütülmüş

        # 1. Punctuation (Noktalama)
        if (original and not original.isalnum()) or (corrected and not corrected.isalnum()):
            return "punctuation"

        # 2. Deascii (Türkçe Karakter)
        turkish_chars = "çğıöşüÇĞİÖŞÜ"
        if any(c in turkish_chars for c in corrected) and not any(c in turkish_chars for c in original):
            return "deascii"

        # 3. Grammar (Dilbilgisi, Edat ve Sık Karıştırılan Kelimeler)
        grammar_words = {
            "a", "an", "the", "in", "on", "at", "to", "for", "of", "with", "by", "from",
            "is", "are", "am", "was", "were", "has", "have", "had", "do", "does", "did",
            "their", "there", "they're", "its", "it's", "your", "you're", "whose", "who's",
            "affect", "effect", "accept", "except", "than", "then", "loose", "lose"
        }
        if orig_l in grammar_words or corr_l in grammar_words:
            return "grammar"

        # 4. ÖZEL İSİM YAZIM HATALARI (Senin bulgunla eklenen yeni kural!)
        if corrected and corrected[0].isupper() and not is_start_of_sentence:
            return "terminology"

        # 5. Lexical vs Typographic (Akıllı Benzerlik Algoritması)
        similarity = SequenceMatcher(None, orig_l, corr_l).ratio()
        if similarity >= 0.70:
            return "typographic"  # Basit harf/klavye hatası
        else:
            return "lexical"  # Kelime tamamen değişmiş

    def _get_explanation(self, err_type):
        """Frontend veya loglar için detaylandırılmış hata açıklamaları"""
        EXPLANATIONS = {
            "deascii": "Türkçe karakter eksikliği veya hatası düzeltildi.",
            "lexical": "Yaygın kelime yazım hatası düzeltildi.",
            "typographic": "Tipografik harf veya klavye hatası düzeltildi.",
            "punctuation": "Noktalama işareti hatası veya eksiği düzeltildi.",
            "grammar": "Dilbilgisi veya edat kullanımı düzeltildi.",
            "terminology": "Özel isim veya terminoloji hatası düzeltildi.",
            "capitalization": "Cümle başı büyük harf kullanımı düzeltildi."
        }
        return EXPLANATIONS.get(err_type, "Sözdizimi veya yapısal bir hata düzeltildi.")

    def process(self, text):
        regex_result = text
        regex_corrections = []
        if self.regex_layer:
            regex_result, regex_corrections = self.regex_layer.process(text)

        prompt = self._build_prompt(regex_result)

        output = self.model(
            prompt,
            max_tokens=1024,
            stop=["###", "</s>"],
            temperature=0.1,
            echo=False
        )

        raw_response = output["choices"][0]["text"].strip()
        final_text = regex_result
        try:
            start_idx = raw_response.find("{")
            end_idx = raw_response.rfind("}")
            if start_idx != -1 and end_idx != -1:
                ai_data = json.loads(raw_response[start_idx:end_idx + 1])
                final_text = ai_data.get("correctedText", regex_result)
        except (json.JSONDecodeError, ValueError):
            final_text = raw_response

        orig_tokens = re.findall(r"[\w]+|[^\s\w]", regex_result)
        corr_tokens = re.findall(r"[\w]+|[^\s\w]", final_text)

        orig_tokens_lower = [t.lower() for t in orig_tokens]
        corr_tokens_lower = [t.lower() for t in corr_tokens]

        matcher = SequenceMatcher(None, orig_tokens_lower, corr_tokens_lower)
        verified_corrections = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == 'equal':
                for k in range(i2 - i1):
                    o = orig_tokens[i1 + k]
                    c = corr_tokens[j1 + k]
                    if o != c:
                        current_j = j1 + k
                        is_start = (current_j == 0) or (
                                    current_j > 0 and corr_tokens[current_j - 1] in ['.', '!', '?', '\n'])
                        err_type = self._determine_error_type(o, c, is_start_of_sentence=is_start)

                        if err_type != "capitalization":
                            verified_corrections.append({
                                "original": o, "corrected": c, "type": err_type,
                                "explanation": self._get_explanation(err_type),
                                "_pos": current_j
                            })

            elif tag == 'replace':
                for k in range(max(i2 - i1, j2 - j1)):
                    o = orig_tokens[i1 + k] if (i1 + k) < i2 else ""
                    c = corr_tokens[j1 + k] if (j1 + k) < j2 else ""
                    if o != c:
                        current_j = j1 + k if (j1 + k) < j2 else j2
                        is_start = (current_j == 0) or (
                                    current_j > 0 and corr_tokens[current_j - 1] in ['.', '!', '?', '\n'])
                        err_type = self._determine_error_type(o, c, is_start_of_sentence=is_start)
                        verified_corrections.append({
                            "original": o, "corrected": c, "type": err_type,
                            "explanation": self._get_explanation(err_type),
                            "_pos": current_j
                        })

            elif tag == 'insert':
                for k in range(j1, j2):
                    c = corr_tokens[k]
                    err_type = self._determine_error_type("", c)
                    verified_corrections.append({
                        "original": "", "corrected": c, "type": err_type,
                        "explanation": self._get_explanation(err_type),
                        "_pos": k
                    })

            elif tag == 'delete':
                for k in range(i1, i2):
                    o = orig_tokens[k]
                    err_type = self._determine_error_type(o, "")
                    verified_corrections.append({
                        "original": o, "corrected": "", "type": err_type,
                        "explanation": self._get_explanation(err_type),
                        "_pos": j1
                    })

        combined_corrections = self._merge_and_sort_corrections(regex_corrections, verified_corrections)

        return {
            "originalText": text,
            "correctedText": final_text,
            "corrections": combined_corrections,
            "metadata": {
                "regex_count": len(regex_corrections),
                "neural_count": len(verified_corrections)
            }
        }

    def _merge_and_sort_corrections(self, regex_list, ai_list):
        seen_keys = set()
        merged = []
        for c in ai_list + regex_list:
            k = (c.get("original", "").lower(), c.get("corrected", "").lower())
            if k not in seen_keys:
                merged.append(c)
                seen_keys.add(k)

        def get_sort_key(correction):
            return correction.get('_pos', 9999)

        merged.sort(key=get_sort_key)
        for m in merged:
            m.pop('_pos', None)

        return merged


# ==================== HİBRİT TEST ====================
if __name__ == "__main__":
    pipeline = MizanV4HybridPipeline(gguf_path="Meta-Llama-3.1-8B.Q4_K_M.gguf")

    test_input = "Prezident Barrack Obamma met with Chancelor Angela Merkal in Berln to discuss the Europeen Union's econimic policies."

    print("\n🚀 MİZAN V4 HİBRİT SİSTEM ÇALIŞIYOR...")
    print(f"📥 GİRDİ: {test_input}")

    result = pipeline.process(test_input)

    print("\n🎯 ANALİZ SONUCU:")
    output_json = json.dumps(result, indent=4, ensure_ascii=False)
    print(output_json)

    output_filename = "mizan_v4_test_output.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"\n✅ Çıktı başarıyla proje klasöründeki '{output_filename}' dosyasına kaydedildi!")
    except Exception as e:
        print(f"\n❌ Dosya kaydedilirken bir hata oluştu: {e}")
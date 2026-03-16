import sys
import os
import time
import difflib
from pathlib import Path
from typing import List, Optional, Literal

# --- 1. YOL VE ORTAM AYARLARI ---
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv(dotenv_path=root_path / ".env")

VALID_API_KEY = os.getenv("MIZAN_API_KEY")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"

from step7_hybrid_model.hybrid_normalizer import HybridPipeline

app = FastAPI(
    title="Mizan AI API",
    description="Haber metinleri için 6 kategorili profesyonel normalizasyon servisi.",
    version="2.7.0",
    debug=DEBUG_MODE
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"🧠 Yapay Zeka Motoru Yükleniyor... (Mode: {'Debug' if DEBUG_MODE else 'Production'})")
pipeline = HybridPipeline()

# --- 2. ŞEMALAR ---
ErrorType = Literal[
    "de-asciification",
    "typographical",
    "terminology",
    "lexical_spelling",
    "grammar",
    "punctuation"
]


class CorrectionEntry(BaseModel):
    original: str
    corrected: str
    type: ErrorType
    explanation: Optional[str] = None


class MizanRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class MizanResponse(BaseModel):
    originalText: str
    correctedText: str
    corrections: List[CorrectionEntry]
    performance: Optional[dict] = None


# --- 3. AKILLI KATEGORİZASYON MANTIĞI ---
def categorize_error(original: str, corrected: str) -> ErrorType:
    orig_l, corr_l = original.lower(), corrected.lower()

    # 1. Terminology (Örn: Turkey -> Türkiye)
    term_map = {"turkey": "türkiye", "burma": "myanmar", "swaziland": "eswatini"}
    if orig_l in term_map or corr_l in term_map.values():
        return "terminology"

    # 2. De-asciification (Sadece karakter değişimi varsa - Örn: Istanbul -> İstanbul)
    tr_map = str.maketrans("çşğöüıÇŞĞÖÜİ", "csgouiCSGOUI")
    if original.translate(tr_map).lower() == corrected.lower():
        return "de-asciification"

    # 3. Punctuation
    if any(c in original or c in corrected for c in ".,;:!?") or original.capitalize() == corrected:
        return "punctuation"

    # 4. Typographical (Karakter farkı az ise)
    if abs(len(original) - len(corrected)) <= 3:
        return "typographical"

    return "grammar"


# --- 4. ENDPOINT ---
@app.post("/api/correct", response_model=MizanResponse)
async def correct_text(request: MizanRequest, x_api_key: str = Header(None)):
    # API Key Güvenlik Kontrolü
    if not VALID_API_KEY:
        raise HTTPException(status_code=500, detail="Server Configuration Error: API Key not set.")

    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        start_time = time.time()

        # Hibrit işlem başlasın
        result = pipeline.normalize_text(request.text)

        final_corrections = []

        # 1. Regex katmanından gelenleri sınıflandır
        for rule in result.get("regex_kurallari", []):
            try:
                parts = rule.split("->")
                orig, corr = parts[0].strip(), parts[1].strip()
                final_corrections.append(CorrectionEntry(
                    original=orig,
                    corrected=corr,
                    type=categorize_error(orig, corr),
                    explanation="Automated detection based on TRT news standards."
                ))
            except:
                continue

        # 🚀 2. YENİ BÖLÜM: Llama'nın yaptığı değişiklikleri kelime kelime bul (Diffing)
        if result["regex_sonrasi"] != result["final_sonuc"]:
            orig_words = result["regex_sonrasi"].split()
            corr_words = result["final_sonuc"].split()

            matcher = difflib.SequenceMatcher(None, orig_words, corr_words)
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == 'replace':
                    o_text = " ".join(orig_words[i1:i2])
                    c_text = " ".join(corr_words[j1:j2])
                    final_corrections.append(CorrectionEntry(
                        original=o_text,
                        corrected=c_text,
                        type=categorize_error(o_text, c_text),
                        explanation="Llama 3.1 Refinement"
                    ))
                elif tag == 'delete':
                    o_text = " ".join(orig_words[i1:i2])
                    final_corrections.append(CorrectionEntry(
                        original=o_text,
                        corrected="[Silindi]",
                        type="grammar",
                        explanation="Removed unnecessary word"
                    ))
                elif tag == 'insert':
                    c_text = " ".join(corr_words[j1:j2])
                    final_corrections.append(CorrectionEntry(
                        original="[Eklendi]",
                        corrected=c_text,
                        type="grammar",
                        explanation="Added missing word"
                    ))

        process_time = round(time.time() - start_time, 3)

        return MizanResponse(
            originalText=result["orijinal"],
            correctedText=result["final_sonuc"],
            corrections=final_corrections,
            performance={"process_time_ms": process_time * 1000}
        )
    except Exception as e:
        if DEBUG_MODE:
            raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    print(f"🚀 Mizan API Server starting on http://{API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
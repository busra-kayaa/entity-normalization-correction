import sys
import os
import time
import difflib
import re  # 🚀 Noktalamaları ayırmak için eklendi
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

    # 1. Punctuation (Noktalama)
    orig_alnum = "".join(c for c in original if c.isalnum())
    corr_alnum = "".join(c for c in corrected if c.isalnum())
    if (orig_alnum == corr_alnum and original != corrected) or original in ".,!?;:" or corrected in ".,!?;:":
        return "punctuation"

    # 2. De-asciification
    tr_map = str.maketrans("çşğöüıÇŞĞÖÜİ", "csgouiCSGOUI")
    if original.translate(tr_map).lower() == corrected.translate(tr_map).lower() and orig_l != corr_l:
        return "de-asciification"

    # 3. Terminology
    term_map = {"burma": "myanmar", "turkey": "türkiye", "kiev": "kyiv", "holland": "netherlands",
                "swaziland": "eswatini"}
    if orig_l in term_map or corr_l in term_map.values():
        return "terminology"
    if (original.istitle() or corrected.istitle()) and difflib.SequenceMatcher(None, orig_l, corr_l).ratio() < 0.6:
        return "terminology"

    # 4. Lexical Spelling
    lexical_pairs = [("affect", "effect"), ("their", "there"), ("then", "than"), ("economic", "economical")]
    for p1, p2 in lexical_pairs:
        if (p1 in orig_l or p2 in orig_l) and (p1 in corr_l or p2 in corr_l):
            return "lexical_spelling"

    # 5. Grammar
    grammar_words = {"is", "are", "am", "was", "were", "the", "a", "an", "in", "on", "at"}
    if orig_l in grammar_words or corr_l in grammar_words:
        return "grammar"

    # 6. Typographical
    if difflib.SequenceMatcher(None, orig_l, corr_l).ratio() > 0.6:
        return "typographical"

    return "lexical_spelling"


# --- 4. ENDPOINT ---
@app.post("/api/correct", response_model=MizanResponse)
async def correct_text(request: MizanRequest, x_api_key: str = Header(None)):
    if not VALID_API_KEY:
        raise HTTPException(status_code=500, detail="Server Configuration Error: API Key not set.")

    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        start_time = time.time()
        result = pipeline.normalize_text(request.text)

        print("\n" + "🔥" * 25)
        print("🤖 HİBRİT MOTORUN HAM (RAW) ÇIKTISI:")
        print(result)
        print("🔥" * 25 + "\n")

        final_corrections = []

        if result["orijinal"] != result["final_sonuc"]:
            # 🚀 AKILLI PARÇALAYICI: Kelimeleri ve noktalamaları ayırır
            def tokenize(text):
                return re.findall(r"[\w']+|[.,!?;:]", text)

            orig_words = tokenize(result["orijinal"])
            corr_words = tokenize(result["final_sonuc"])

            matcher = difflib.SequenceMatcher(None, orig_words, corr_words)
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                o_text = " ".join(orig_words[i1:i2])
                c_text = " ".join(corr_words[j1:j2])

                if tag == 'replace':
                    final_corrections.append(CorrectionEntry(
                        original=o_text,
                        corrected=c_text,
                        type=categorize_error(o_text, c_text),
                        explanation="System Refinement"
                    ))
                elif tag == 'delete':
                    is_punct = any(c in o_text for c in ".,;:!?")
                    final_corrections.append(CorrectionEntry(
                        original=o_text,
                        corrected="[Silindi]",
                        type="punctuation" if is_punct else "grammar",
                        explanation="Removed unnecessary item"
                    ))
                elif tag == 'insert':
                    is_punct = any(c in c_text for c in ".,;:!?")
                    final_corrections.append(CorrectionEntry(
                        original="[Eklendi]",
                        corrected=c_text,
                        type="punctuation" if is_punct else "grammar",
                        explanation="Added missing item"
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
import os
import sys

ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ana_dizin not in sys.path:
    sys.path.append(ana_dizin)

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

load_dotenv()

MIZAN_API_KEY = os.getenv("MIZAN_API_KEY")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

from step9_json_hybrid_model.hybrid_normalizer import HybridPipeline

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == MIZAN_API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Geçersiz veya eksik API Anahtarı! (MIZAN_API_KEY)")


# Global Model Değişkeni
mizan_pipeline = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global mizan_pipeline
    print("🚀 API Başlatılıyor... Mizan v2 (JSON Hybrid) RAM/VRAM'e yükleniyor...")
    mizan_pipeline = HybridPipeline()
    print(f"✅ Model yüklendi. API {API_HOST}:{API_PORT} adresinde dinliyor.")
    yield
    print("🛑 Sunucu kapatılıyor...")


# FastAPI Uygulamasını Başlat
app = FastAPI(
    title="Mizan v2 Backend",
    description="Regex ve Llama 3.1 destekli, Zero-Shot JSON metin düzeltme motoru",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
#  Pydantic Şemaları (JSON formatına göre uyarlandı)
# ==========================================
class AnalyzeRequest(BaseModel):
    text: str


class CorrectionDetail(BaseModel):
    original: str
    corrected: str
    type: str
    explanation: str


class AnalyzeResponse(BaseModel):
    originalText: str
    correctedText: str
    corrections: List[CorrectionDetail] = []


# ==========================================
#  ANA ENDPOINT
# ==========================================
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, api_key: str = Depends(verify_api_key)):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Boş metin gönderilemez.")

    try:
        sonuc = mizan_pipeline.normalize_text(request.text)

        return AnalyzeResponse(
            originalText=sonuc.get("originalText", request.text),
            correctedText=sonuc.get("correctedText", request.text),
            corrections=sonuc.get("corrections", [])
        )

    except Exception as e:
        print(f"❌ API Hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Model işleme sırasında bir hata oluştu.")


if __name__ == "__main__":
    print("🌐 Mizan API Uvicorn sunucusunda başlatılıyor...")
    uvicorn.run("newapi:app", host=API_HOST, port=API_PORT, reload=os.getenv("DEBUG_MODE") == "True")
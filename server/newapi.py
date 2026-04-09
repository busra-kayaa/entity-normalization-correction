import os
import sys
import time
import uvicorn
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

# --- LOGGING AYARI ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. YOL AYARLARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

# --- 2. V4 HİBRİT MOTORU İMPORT ---
try:
    from step11_fix_summarization_bias.mizan_inference_v4 import MizanV4HybridPipeline
    logger.info("✅ Mizan V4 Hibrit Pipeline entegre edildi.")
except ImportError as e:
    raise RuntimeError(f"Import hatası: {e}")

load_dotenv()

# --- 3. AYARLAR ---
API_PORT = int(os.getenv("API_PORT"))
API_HOST = os.getenv("API_HOST")

# Hız sınırlayıcı (Rate Limiter)
limiter = Limiter(key_func=get_remote_address)

# --- 4. MODEL YÖNETİMİ (LIFESPAN) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Mizan V4 API başlatılıyor...")

    model_path = os.path.join(
        project_root,
        "step11_fix_summarization_bias",
        "Meta-Llama-3.1-8B.Q4_K_M.gguf"
    )

    logger.info(f"🔍 Model aranıyor: {model_path}")

    if not os.path.exists(model_path):
        raise RuntimeError(f"Model bulunamadı: {model_path}")

    try:
        app.state.mizan_v4 = MizanV4HybridPipeline(gguf_path=model_path)
        logger.info(f"✅ Model hazır: {API_HOST}:{API_PORT}")
    except Exception as e:
        raise RuntimeError(f"Model yüklenemedi: {str(e)}")

    yield
    logger.info("🛑 API kapatılıyor...")


# --- 5. FASTAPI YAPILANDIRMASI ---
app = FastAPI(
    title="Mizan V4 API",
    description="V4 Hibrit Normalizasyon Motoru",
    version="4.0.1",
    lifespan=lifespan
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Çok fazla istek attınız, biraz bekleyin."}
    )

# --- 6. CORS GÜVENLİĞİ (KRİTİK) ---
ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


# --- 7. ŞEMALAR ---
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)

class CorrectionDetail(BaseModel):
    original: str
    corrected: str
    type: str
    explanation: Optional[str] = "Düzeltildi."

class AnalyzeResponse(BaseModel):
    originalText: str
    correctedText: str
    corrections: List[CorrectionDetail]
    metadata: Optional[dict] = None


# --- 8. MIDDLEWARE (LOGGING) ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url} - {duration}ms")
    return response


# --- 9. ENDPOINTS ---
@app.get("/health", tags=["System"])
async def health_check(request: Request):
    model_loaded = hasattr(request.app.state, "mizan_v4")
    return {
        "status": "online",
        "version": "4.0.1",
        "model_loaded": model_loaded
    }

@app.post("/api/v4/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
@limiter.limit("20/minute")
async def analyze_text(
    request: Request,
    payload: AnalyzeRequest,
):
    # Model kontrolü
    if not hasattr(request.app.state, "mizan_v4"):
        raise HTTPException(status_code=503, detail="Model henüz yüklenmedi, lütfen bekleyin.")

    model = request.app.state.mizan_v4
    start_time = time.time()

    try:
        sonuc = model.process(payload.text)
        process_time_ms = round((time.time() - start_time) * 1000, 2)

        meta = sonuc.get("metadata", {})
        meta.update({
            "processing_time_ms": process_time_ms,
            "char_count": len(payload.text)
        })

        return AnalyzeResponse(
            originalText=sonuc["originalText"],
            correctedText=sonuc["correctedText"],
            corrections=sonuc["corrections"],
            metadata=meta
        )

    except Exception as e:
        logger.error(f"❌ Model İşleme Hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Metin işlenirken bir hata oluştu.")


# --- 10. CALIŞTIRMA ---
if __name__ == "__main__":
    uvicorn.run("newapi:app", host=API_HOST, port=API_PORT, reload=True)
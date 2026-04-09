import os
import sys
import time
import uvicorn
import logging
import secrets
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
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

# --- 3. GÜVENLİK VE AYARLAR ---
MIZAN_API_KEY = os.getenv("MIZAN_API_KEY")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
limiter = Limiter(key_func=get_remote_address)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or not MIZAN_API_KEY:
        raise HTTPException(status_code=401, detail="API anahtarı eksik!")

    # timing attack koruması
    if not secrets.compare_digest(api_key, MIZAN_API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Geçersiz API Anahtarı!",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    return api_key


# --- 4. MODEL YÖNETİMİ ---
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


# --- 5. FASTAPI ---
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

# CORS (Production için kısıtla!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # PROD'da değiştir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 6. ŞEMALAR ---
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


# --- 7. MIDDLEWARE (REQUEST LOGGING) ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)

    logger.info(f"{request.method} {request.url} - {duration}ms")
    return response


# --- 8. ENDPOINTS ---
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
    api_key: str = Depends(verify_api_key)
):
    if not hasattr(request.app.state, "mizan_v4"):
        raise HTTPException(status_code=503, detail="Model hazır değil")

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
        logger.error(f"❌ Hata: {str(e)}")
        raise HTTPException(status_code=500, detail="Model işleme hatası")


# --- 9. MAIN ---
if __name__ == "__main__":
    uvicorn.run("newapi:app", host=API_HOST, port=API_PORT)
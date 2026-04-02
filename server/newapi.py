import os
import sys
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

# --- 2. IMPORTLAR ---
try:
    from step10_hierarchical_6class.mizan_inference_v3 import MizanV3Step10Pipeline
except ImportError as e:
    print(f"❌ Import Hatası: {e}")
    sys.exit(1)

load_dotenv()

# --- 3. AYARLAR ---
MIZAN_API_KEY = os.getenv("MIZAN_API_KEY")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == MIZAN_API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Geçersiz API Anahtarı!")


# --- 4. MODEL YÖNETİMİ ---
mizan_v3 = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global mizan_v3
    print("🚀 API Başlatılıyor...")

    model_path = os.path.join(project_root, "step10_hierarchical_6class", "Mizan_V3_Final_Model.gguf")

    print(f"🧠 Mizan V3 Yükleniyor: {model_path}")

    if not os.path.exists(model_path):
        print(f"❌ HATA: Model dosyası bu yolda yok: {model_path}")
        sys.exit(3)

    mizan_v3 = MizanV3Step10Pipeline(gguf_path=model_path)
    print(f"✅ Mizan V3 Hazır. {API_HOST}:{API_PORT} üzerinden istekleri bekliyor.")
    yield
    print("🛑 API Kapatılıyor...")


# --- 5. FASTAPI UYGULAMASI ---
app = FastAPI(
    title="Mizan V3 API",
    description="GGUF & Step 10 Hiyerarşik Regex Destekli Normalizasyon Motoru",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 6. ŞEMALAR ---
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
    corrections: List[CorrectionDetail]


# --- 7. ENDPOINTS ---
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, api_key: str = Depends(verify_api_key)):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Metin boş olamaz.")

    try:
        # Mizan V3 motorunu çalıştır
        sonuc = mizan_v3.normalize_text(request.text)

        return AnalyzeResponse(
            originalText=sonuc["originalText"],
            correctedText=sonuc["correctedText"],
            corrections=sonuc["corrections"]
        )

    except Exception as e:
        print(f"❌ İşlem Hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Model işleme sırasında hata oluştu.")


if __name__ == "__main__":
    # ÖNEMLİ: "newapi:app" kısmı dosya adınla aynı olmalı
    uvicorn.run("newapi:app", host=API_HOST, port=API_PORT, reload=False)
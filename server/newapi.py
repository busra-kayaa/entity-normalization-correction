import os
import sys

# Python'un bir üst klasörü (ana projeyi) de görmesini sağlıyoruz
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ana_dizin not in sys.path:
    sys.path.append(ana_dizin)

import difflib
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

load_dotenv()

MIZAN_API_KEY = os.getenv("MIZAN_API_KEY")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

from step8_structured_modeL.hybrid_normalizer import HybridPipeline

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
    print("🚀 API Başlatılıyor... Mizan AI Modeli RAM/VRAM'e yükleniyor...")
    mizan_pipeline = HybridPipeline()
    print(f"✅ Model yüklendi. API {API_HOST}:{API_PORT} adresinde dinliyor.")
    yield
    print("🛑 Sunucu kapatılıyor...")


# FastAPI Uygulamasını Başlat
app = FastAPI(
    title="Mizan AI Backend",
    description="Regex ve Llama 3.1 destekli metin düzeltme motoru",
    version="1.0.0",
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


# Şemalar
class AnalyzeRequest(BaseModel):
    text: str


class CorrectionDetail(BaseModel):
    original: str
    corrected: str
    type: str
    description: str


class AnalyzeResponse(BaseModel):
    original_text: str
    result: str
    error_types: List[str]
    details: List[CorrectionDetail] = []


def generate_diff_details(original: str, corrected: str, ai_tags: List[str]) -> List[CorrectionDetail]:
    words1 = original.split()
    words2 = corrected.split()
    matcher = difflib.SequenceMatcher(None, words1, words2)
    details = []

    # 🚀 AKADEMİK KATEGORİ SÖZLÜĞÜ
    tag_info = {
        "de-asciification": ("De-asciification",
                             "Türkçe karakterlerin (ç,ğ,ı,ö,ş,ü) veya I/i dönüşüm hataları düzeltildi."),
        "typography": ("Harf Dizilimi", "Özel isimlerde veya genel kullanımda harf eksikliği/fazlalığı giderildi."),
        "terminology": ("Terminoloji", "Uluslararası isim değişimleri veya resmi kurum adları güncellendi."),
        "lexical_spelling": ("Genel Yazım Hatası",
                             "Özel isim olmayan standart kelimelerdeki yazım hataları düzeltildi."),
        "grammar": ("Gramer ve Sözdizimi", "Eksik artikeller, edatlar veya özne-yüklem uyumsuzlukları giderildi."),
        "punctuation": ("Noktalama İşaretleri", "Cümle sınırı ve duraklama işaretleri (virgül vb.) düzenlendi.")
    }

    # Gramer ve Terminoloji için "Zeka" Kümeleri
    grammar_keywords = {"is", "are", "was", "were", "a", "an", "the", "in", "on", "at", "has", "have", "had", "to",
                        "of"}
    terminology_keywords = {"Türkiye", "Myanmar", "Eswatini", "Kyiv", "Czechia", "Netherlands"}
    terminology_old = {"Turkey", "Burma", "Swaziland", "Kiev", "Holland"}

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            old_w = " ".join(words1[i1:i2])
            new_w = " ".join(words2[j1:j2])

            # 🧠 KELİME BAZLI DİNAMİK ANALİZ

            # 1. Noktalama
            if old_w.strip(".,!?:;'\"") == new_w.strip(".,!?:;'\""):
                d_type, d_desc = tag_info["punctuation"]

            # 2. De-asciification (Büyük/Küçük harf, I/i dönüşümleri)
            elif old_w.lower() == new_w.lower() or old_w.replace('ı', 'i').replace('İ', 'I').replace('ş',
                                                                                                     's').lower() == new_w.lower():
                d_type, d_desc = tag_info["de-asciification"]

            # 3. Terminoloji
            elif new_w in terminology_keywords or old_w in terminology_old:
                d_type, d_desc = tag_info["terminology"]

            # 4. Gramer
            elif old_w.lower() in grammar_keywords or new_w.lower() in grammar_keywords or "'" in old_w or "'" in new_w:
                d_type, d_desc = tag_info["grammar"]

            # 5. Harf Dizilimi vs Genel Yazım Hatası
            else:
                if old_w.islower() and new_w.islower():
                    d_type, d_desc = tag_info["lexical_spelling"]
                else:
                    d_type, d_desc = tag_info["typography"]

            details.append(CorrectionDetail(original=old_w, corrected=new_w, type=d_type, description=d_desc))

        elif tag == 'delete':
            details.append(CorrectionDetail(original=" ".join(words1[i1:i2]), corrected="---", type="Gereksiz",
                                            description="Anlatımı bozan gereksiz ifade metinden çıkarıldı."))
        elif tag == 'insert':
            details.append(CorrectionDetail(original="---", corrected=" ".join(words2[j1:j2]), type="Eksik Kelime",
                                            description="Cümle anlamını tamamlamak için eksik olan kelime eklendi."))

    return details


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, api_key: str = Depends(verify_api_key)):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Boş metin gönderilemez.")

    try:
        sonuc = mizan_pipeline.normalize_text(request.text)

        orijinal_metin = sonuc.get("orijinal", request.text)
        final_metin = sonuc.get("final_sonuc", request.text)

        hatalar = sonuc.get("tespit_edilen_hatalar", sonuc.get("regex_kurallari", []))

        frontend_details = generate_diff_details(orijinal_metin, final_metin, hatalar)

        return AnalyzeResponse(
            original_text=orijinal_metin,
            result=final_metin,
            error_types=hatalar,
            details=frontend_details
        )
    except Exception as e:
        print(f"❌ API Hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Model işleme sırasında bir hata oluştu.")


if __name__ == "__main__":
    print("🌐 Mizan API Uvicorn sunucusunda başlatılıyor...")
    uvicorn.run("newapi:app", host=API_HOST, port=API_PORT, reload=os.getenv("DEBUG_MODE") == "True")
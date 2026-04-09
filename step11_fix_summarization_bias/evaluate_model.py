import os
import sys
import json
import time

# Eğer klasör yollarında sorun çıkarsa diye current_dir ekliyoruz
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from mizan_inference_v4 import MizanV4HybridPipeline


def run_evaluation(jsonl_path="data/mizan_v4_test.jsonl", gguf_path="Meta-Llama-3.1-8B.Q4_K_M.gguf"):
    print("🚀 Mizan V4 Test Veri Seti Değerlendirmesi Başlıyor...")

    if not os.path.exists(jsonl_path):
        print(f"❌ HATA: Test dosyası bulunamadı: {jsonl_path}")
        return

    # Modeli Yükle
    pipeline = MizanV4HybridPipeline(gguf_path=gguf_path)

    # Değerlendirme Metrikleri
    total_samples = 0
    exact_matches = 0
    total_time = 0
    failed_parses = 0

    detailed_results = []

    print(f"\n📂 Dosya okunuyor: {jsonl_path}")
    print("-" * 50)

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_samples = len(lines)

    for idx, line in enumerate(lines, 1):
        try:
            data = json.loads(line)
            # Alpaca formatında hatalı metin genellikle 'input' içindedir
            buggy_text = data.get("input", "")

            # Beklenen (Doğru) çıktı 'output' içindedir (JSON string veya düz metin olabilir)
            expected_output_raw = data.get("output", "")

            # Eğer output'un kendisi bir JSON string ise, içinden correctedText'i alalım
            try:
                expected_json = json.loads(expected_output_raw)
                expected_corrected_text = expected_json.get("correctedText", expected_output_raw)
            except (json.JSONDecodeError, TypeError):
                expected_corrected_text = expected_output_raw

            if not buggy_text:
                continue

            # --- TAHMİN (INFERENCE) BAŞLIYOR ---
            start_time = time.time()
            result = pipeline.process(buggy_text)
            end_time = time.time()
            # --- TAHMİN BİTTİ ---

            process_time = end_time - start_time
            total_time += process_time

            actual_corrected_text = result.get("correctedText", "")

            # Birebir Eşleşme (Exact Match) Kontrolü
            is_match = (actual_corrected_text.strip() == expected_corrected_text.strip())
            if is_match:
                exact_matches += 1

            # Detaylı rapora ekle
            detailed_results.append({
                "id": idx,
                "original": buggy_text,
                "expected": expected_corrected_text,
                "predicted": actual_corrected_text,
                "is_match": is_match,
                "time_seconds": round(process_time, 2),
                "ai_corrections": result.get("corrections", [])
            })

            # Konsola canlı ilerleme yazdır (Her 10 cümlede bir)
            if idx % 10 == 0 or idx == total_samples:
                print(f"🔄 İşlenen: {idx}/{total_samples} | Anlık Doğruluk: %{round((exact_matches / idx) * 100, 2)}")

        except Exception as e:
            print(f"⚠️ Satır {idx} işlenirken hata oluştu: {e}")
            failed_parses += 1

    # --- SONUÇLARI HESAPLA VE YAZDIR ---
    accuracy = (exact_matches / total_samples) * 100 if total_samples > 0 else 0
    avg_time = total_time / total_samples if total_samples > 0 else 0

    print("\n" + "=" * 50)
    print("🏆 MİZAN V4 TEST RAPORU 🏆")
    print("=" * 50)
    print(f"📊 Toplam Test Edilen Cümle: {total_samples}")
    print(f"✅ Birebir Doğru Çeviri (Exact Match): {exact_matches}")
    print(f"🎯 Model Doğruluk Oranı (Accuracy): %{accuracy:.2f}")
    print(f"⏱️ Toplam İşlem Süresi: {total_time:.2f} saniye")
    print(f"⚡ Cümle Başına Ortalama Hız: {avg_time:.2f} saniye")
    if failed_parses > 0:
        print(f"⚠️ Hatalı Format Yüzünden Atlanan: {failed_parses}")
    print("=" * 50)

    # Detaylı raporu JSON olarak kaydet
    report_file = "mizan_v4_evaluation_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            "metrics": {
                "total_samples": total_samples,
                "exact_matches": exact_matches,
                "accuracy_percent": accuracy,
                "average_latency_seconds": avg_time
            },
            "results": detailed_results
        }, f, ensure_ascii=False, indent=4)

    print(
        f"\n💾 Detaylı karşılaştırma raporu '{report_file}' dosyasına kaydedildi. Hangi cümlelerde hata yaptığını oradan inceleyebilirsin!")


if __name__ == "__main__":
    run_evaluation()
import json
import re
import nltk
import time
from nltk.tokenize import sent_tokenize # metni anlamlı cümleler halinde bölmek için
from collections import defaultdict
from datetime import datetime

# NLTK verilerini indir
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Wikipedia kütüphanesi
try:
    import wikipedia
    import warnings
    from bs4 import GuessedAtParserWarning
    warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
    wikipedia.set_lang('en')
    print("✓ wikipedia kütüphanesi yüklendi")
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'wikipedia'])
    import wikipedia
    wikipedia.set_lang('en')
    print("✓ wikipedia kütüphanesi yüklendi")

successful_pages_list = [
    "United States", "United Kingdom", "World War II", "World War I", "American Revolution",
    "Renaissance", "Middle Ages", "Ancient Greece", "Egypt", "Brazil", "Donald Trump",
    "Angela Merkel", "Winston Churchill", "Napoleon", "Albert Einstein", "Isaac Newton",
    "Internet", "Artificial intelligence", "Technology", "Physics", "Chemistry",
    "Biology", "Medicine", "Psychology", "Economics", "Philosophy", "Sociology",
    "Anthropology", "History", "Literature", "Art", "Film", "Architecture",
    "Harvard University", "Oxford University", "Cambridge University", "NASA",
    "Microsoft", "Climate change", "Environment", "Renewable energy", "Moon landing", "International Space Station",
    "Election", "Parliament", "Foreign policy", "International relations", "NATO",
    "Treaty", "International sanctions", "Diplomacy", "Summit (meeting)",
    "Political party", "Constitution", "Human rights", "Sovereignty",
    "Government", "Legislature", "Executive", "Judiciary", "Monarchy",
    "Republic", "Federalism", "Separation of powers", "Civil rights",
    "Freedom of speech", "Freedom of the press", "Universal suffrage", "Prime minister",
    "Turkey", "Politics of Turkey", "President of Turkey",
    "Grand National Assembly of Turkey", "Istanbul", "İzmir", "Turkish Armed Forces", "Foreign relations of Turkey",
    "History of Turkey", "Constitution of Turkey", "Recep Tayyip Erdoğan", "Mustafa Kemal Atatürk", "Turkish War of Independence",
    "Ottoman Empire", "Byzantine Empire", "Constantinople", "Cappadocia", "Antalya", "Adana", "Trabzon", "Konya", "Gaziantep",
    "Turkish language", "Secularism in Turkey",
    "President of the United States", "Prime Minister of the United Kingdom", "Chancellor of Germany", "President of France",
    "Secretary-General of the United Nations", "Prime Minister of Canada", "President of China", "President of Brazil",
    "President of Argentina", "Prime Minister of Japan", "President of South Korea", "President of Mexico", "Chancellor of Austria",
    "Prime Minister of Spain", "President of Egypt", "President of South Africa",
    "Rights", "Supreme Court", "International law", "Criminal law", "Philosophy of law", "Legal history", "Globalization",
    "International trade", "World Bank", "Socialism", "Communism", "Conservatism", "Abraham Lincoln", "George Washington",
    "Franklin D. Roosevelt", "John F. Kennedy", "Martin Luther King Jr.", "Nelson Mandela", "Mahatma Gandhi", "Charles Darwin",
    "Stephen Hawking", "Marie Curie", "William Shakespeare", "Leonardo da Vinci", "Vincent van Gogh", "Mozart",
    "Beethoven", "The Beatles", "Elvis Presley", "Michael Jackson", "Coca-Cola", "McDonald's",
    "Facebook", "Twitter", "YouTube", "Netflix", "Disney", "Hollywood", "Broadway",
    "Olympic Games", "FIFA World Cup", "Super Bowl", "NBA", "NFL", "Harvard Law School", "Stanford University", "MIT", "Yale University",
    "Climate change mitigation", "Carbon footprint", "Sustainability", "Renewable energy transition",
    "Greenhouse gas emissions", "Digital transformation", "Smart city", "Circular economy",
    "Environmental impact of aviation", "Carbon offsets and credits", "Deforestation",
    "Ocean acidification", "Global warming", "Wind power", "Solar energy", "Electric vehicle", "Sustainable agriculture",
    "Large language model", "Natural language processing", "Machine translation",
    "Transformer (machine learning model)", "Deep learning", "Artificial neural network", "Data structure",
    "Algorithm", "SQL", "Parallel computing", "Computer architecture", "Python (programming language)", "C (programming language)",
    "Relational database", "Graph theory", "Wearable technology",
    "May (month)", "Theresa May", "Bill Clinton", "Bill (law)", "Brown University",
    "Gordon Brown", "Apple Inc.", "Apple (fruit)", "Amazon (company)", "Amazon River", "Turkey (bird)", "Georgia (U.S. state)",
    "Georgia (country)", "Jordan (country)", "Michael Jordan", "Chase Bank", "Chase (name)", "Ford Motor Company",
    "Inflation", "Stock market", "Cryptocurrency", "Gross domestic product", "World Health Organization", "European Central Bank",
    "Reuters", "Associated Press", "Journalism", "Breaking news", "International Monetary Fund", "Supply chain", "Interest rate",
    "Foreign exchange market", "Venture capital", "Startup company",

    # Global Brands & Figures (Normalization test sets)
    "Google", "Tencent", "Alibaba Group", "Warren Buffett", "Steve Jobs", "Bill Gates", "Elon Musk",
    "Mark Zuckerberg", "Indra Nooyi", "Sheryl Sandberg",
    # Cities & Logistics
    "New York City", "Los Angeles", "Chicago", "Toronto", "Paris", "Berlin", "Tokyo", "Hong Kong", "Singapore",
    "Sydney", "Dubai", "Beijing", "Moscow", "Logistics", "Supply chain management",
    # Science & Space
    "Galaxy", "Big Bang", "Quantum mechanics", "General relativity", "Human genome", "DNA", "CRISPR", "Vaccine",
    "Evolutionary biology", "Space exploration", "James Webb Space Telescope",
    # International Organizations
    "European Union", "African Union", "ASEAN", "G20", "G7", "World Trade Organization", "UNICEF", "UNESCO", "Red Cross", "Amnesty International"
                                                                                                                          "Advanced Micro Devices",
    "Intel Core", "Nvidia GeForce", "ASML Holding", "TSMC",
    "ARM architecture family", "Instruction set architecture", "Field-programmable gate array",
    "Application-specific integrated circuit", "Digital signal processor", "Verilog", "VHDL",

    "Friedrich Merz", "European Parliament election 2024", "Politics of Germany",
    "G7 summit", "BRICS", "United States Senate", "House of Commons of the United Kingdom",

    "Artemis program", "James Webb Space Telescope", "SpaceX Starship", "Blue Origin",
    "Boeing 787 Dreamliner", "Airbus A350", "Lockheed Martin F-35 Lightning II",

    "Togg", "Bayraktar TB2", "Anka (unmanned aerial vehicle)", "Borsa Istanbul",
    "Central Bank of the Republic of Turkey", "Geography of Turkey", "Turkish Riviera",

    "Federal Reserve", "Wall Street Journal", "Financial Times", "NASDAQ-100",
    "S&P 500", "Gold as an investment", "Oil prices", "Renewable energy in the European Union",

    "ByteDance", "OpenAI", "DeepMind", "Twitter under Elon Musk", "Instagram", "Reddit",
    "Netflix", "Spotify", "Tesla Gigafactory", "Berkshire Hathaway"
                                               "GPT-4", "Claude (chatbot)", "Mistral AI", "Hugging Face",
    "Reinforcement learning from human feedback", "Prompt engineering",

    "RISC-V", "X86 architecture", "MIPS architecture", "Semiconductor fabrication",
    "Extreme ultraviolet lithography", "Photolithography",
    "ASELSAN", "ROKETSAN", "HAVELSAN", "TUSAŞ", "Baykar Bayraktar Kızılelma",

    "Friedrich Merz", "Olaf Scholz", "Emmanuel Macron", "Joe Biden",
    "European Central Bank", "Federal Reserve System", "World Economic Forum",

    "Silicon Valley", "Wall Street", "City of London", "Brussels",
    "Eskişehir", "Muğla", "Denizli", "Kocaeli", "Gaziantep",

    "Nvidia", "TSMC", "ASML Holding", "Qualcomm", "Broadcom Inc.", "Oracle Corporation",

    "Electric vehicle adoption", "Smart grid", "Hydrogen economy",
    "Sustainable fashion", "Vertical farming", "Edge computing", "5G", "6G (network)"
]

def get_page_safely(title):
    try:
        return wikipedia.page(title)
    except wikipedia.DisambiguationError as e:
        for option in e.options[:2]:
            try:
                return wikipedia.page(option)
            except:
                continue
        return None
    except:
        return None

def clean_sentence(text):
    """Metin temizleme"""
    if not text or len(text.strip()) < 10:
        return None

    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[\w+\]', '', text)
    text = re.sub(r'\[citation needed\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[edit\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\s+,', ',', text)
    text = text.strip()

    return text if len(text) > 20 else None

def is_valid_sentence(sentence):
    """Cümle geçerlilik kriterleri"""
    if not sentence or len(sentence) < 20:
        return False

    words = sentence.split()
    if not (6 <= len(words) <= 45):
        return False

    if not sentence[0].isupper():
        return False

    if not any(sentence.rstrip().endswith(p) for p in ['.', '!', '?']):
        return False

    invalid_patterns = [
        r'^[\[\(]', r'^http', r'^ISBN', r'^Redirect',
        r'^Category:', r'^File:', r'^Image:', r'may refer to:',
    ]

    return not any(re.match(p, sentence, re.IGNORECASE) for p in invalid_patterns)

def extract_sentences_from_text(text, max_sentences=50):
    """Metinden cümleleri çıkar - her sayfadan MAX 50 cümle"""
    if not text:
        return []

    sentences = []
    paragraphs = text.split('\n')

    for para in paragraphs:
        if len(para.strip()) < 50:
            continue

        try:
            raw_sentences = sent_tokenize(para)
        except:
            raw_sentences = re.split(r'(?<=[.!?]) +', para)

        for s in raw_sentences:
            cleaned = clean_sentence(s)
            if cleaned and is_valid_sentence(cleaned):
                sentences.append(cleaned)
                if len(sentences) >= max_sentences:
                    return sentences

    return sentences[:max_sentences]

TARGET_SENTENCES = 10000
all_sentences = {}
sentences_with_metadata = []
category_stats = defaultdict(int)
failed_list = []

print("=" * 60)
print(f"🚀 VERİ TOPLAMA - HEDEF: {TARGET_SENTENCES} CÜMLE")
print(f"📚 Toplam Sayfa: {len(successful_pages_list)}")
print("=" * 60)

# MEVCUT VERİYİ YÜKLE (varsa)
try:
    with open('dataset_latest_2.json', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
        for s in old_data.get('sentences', []):
            all_sentences[s] = {
                'text': s,
                'source_page': 'previous_run',
                'category': 'existing',
                'word_count': len(s.split()),
                'char_count': len(s),
                'collected_at': datetime.now().isoformat()
            }
            sentences_with_metadata.append(all_sentences[s])
    print(f"📂 Mevcut veri yüklendi: {len(all_sentences)} cümle")
except:
    print("📂 Yeni veri seti oluşturuluyor...")

print("\n" + "=" * 60)
print("📥 SAYFALAR İŞLENİYOR...")
print("=" * 60)

for i, title in enumerate(successful_pages_list, 1):
    if len(all_sentences) >= TARGET_SENTENCES:
        break

    print(f"  [{i:3}/{len(successful_pages_list)}] {title[:35]:<35}...", end=" ")
    try:
        page = get_page_safely(title)
        if not page:
            print("❌")
            failed_list.append(title)
            continue

        page_content = page.content

        # Her sayfadan MAX 50 cümle al
        sentences = extract_sentences_from_text(page_content, max_sentences=50)

        page_sentences = 0
        for sentence in sentences:
            if sentence not in all_sentences:
                all_sentences[sentence] = {
                    'text': sentence,
                    'source_page': title,
                    'category': 'collected',
                    'word_count': len(sentence.split()),
                    'char_count': len(sentence),
                    'collected_at': datetime.now().isoformat()
                }
                sentences_with_metadata.append(all_sentences[sentence])
                page_sentences += 1

        print(f"✓ +{page_sentences:2} (Toplam: {len(all_sentences):5})")
    except Exception as e:
        print(f"❌ (API Hatası: {str(e)[:20]}...)")
        time.sleep(1)
        continue

    time.sleep(0.5)

# ============ İSTATİSTİKLER ============
total_sentences = len(all_sentences)
completion = (total_sentences / TARGET_SENTENCES) * 100

print("\n" + "=" * 60)
print("📊 VERİ SETİ KAYDEDİLİYOR...")
print("=" * 60)

if total_sentences > 0:
    word_counts = [s['word_count'] for s in sentences_with_metadata]

    stats = {
        "total_sentences": total_sentences,
        "target": TARGET_SENTENCES,
        "completion_percentage": round(completion, 1),
        "successful_pages": i - len(failed_list),
        "average_word_count": round(sum(word_counts) / total_sentences, 2),
        "collection_date": datetime.now().isoformat(),
        "version": "2"
    }

    # Veri setini kaydet
    dataset = {
        "metadata": {
            "total": total_sentences,
            "target": TARGET_SENTENCES,
            "source": "Wikipedia",
            "statistics": stats
        },
        "sentences": sentences_with_metadata
    }

    with open('dataset_10000_target.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    with open('dataset_latest_2.json', 'w', encoding='utf-8') as f:
        json.dump({
            "total": total_sentences,
            "target": TARGET_SENTENCES,
            "sentences": [s['text'] for s in sentences_with_metadata]
        }, f, ensure_ascii=False, indent=2)

    # İlerleme çubuğu
    bar_length = 40
    filled = int(bar_length * total_sentences / TARGET_SENTENCES)
    bar = '█' * filled + '░' * (bar_length - filled)

    print(f"""
    ╔════════════════════════════════════════════════╗
    ║           VERİ SETİ DURUMU                     ║
    ╠════════════════════════════════════════════════╣
    ║  🎯 Hedef: {TARGET_SENTENCES:>6} cümle                           
    ║  📈 Toplam: {total_sentences:>6} cümle ({completion:.1f}%)     
    ║  {bar}     
    ║  📄 İşlenen Sayfa: {i:>6}                       
    ║  ✅ Başarılı: {stats['successful_pages']:>6}                       
    ║  ❌ Başarısız: {len(failed_list):>6}                       
    ║  📊 Ort. Kelime: {stats['average_word_count']:>6}                
    ╚════════════════════════════════════════════════╝
    """)

    if total_sentences < TARGET_SENTENCES:
        eksik = TARGET_SENTENCES - total_sentences
        print(f"\n⚠️  KALAN: {eksik} cümle")
        print(f"💡 Bu kodu TEKRAR çalıştır! Her çalıştırmada ~500-1000 cümle eklenir")
        print(f"📁 Kayıt: dataset_10000_target.json")
    else:
        print(f"\n✅ HEDEFE ULAŞILDI! 🎉")
        print(f"📁 {total_sentences} cümle kaydedildi")

print(f"\n✅ İşlem tamamlandı! Toplam: {total_sentences} cümle")
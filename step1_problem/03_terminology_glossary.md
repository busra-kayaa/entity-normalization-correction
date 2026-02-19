# 📚 TERMINOLOGY GLOSSARY
## Entity Normalization & Correction

| **Son Güncelleme** | 19.02.2026 |
|:-------------------|:-----------|
| **Toplam Terim**   | 38         |
| **Hazırlayan**     | Büşra Kaya |

---

## 📋 İÇİNDEKİLER

| # | Bölüm                                               | Durum |
|:--|:----------------------------------------------------|:------|
| 1 | [STEP 1 - PROBLEM TANIMI](#step-1---problem-tanimi) | ✅ |
| 2 | [STEP 2 - VERİ TOPLAMA](#step-2---veri-toplama)     | ✅ |
| 3 | [STEP 3 - GÜRÜLTÜ EKLEME](#step-3---gürültü-ekleme) | ✅ |

---

## STEP 1 - PROBLEM TANIMI
*Literatür taraması ve problem tanımı sürecinde öğrenilen terimler*

---

### 📌 De-asciification

| | |
| :--- |:---|
| **🗓️ Ne zaman?** | 11.02.2026 |
| **📍 Nerede?** | Problem tanımı, Yazım Hataları Sınıflandırması |
| **❓ Ne işe yarar?** | ASCII karakterlere dönüşmüş Türkçe harfleri orijinal haline getirir |
| **💡 Basit örnek** | `Turkiye` → **`Türkiye`**, `Istanbul` → **`İstanbul`**, `Erdogan` → **`Erdoğan`** |
| **📚 Benzer terimler** | Turkish character normalization, ASCII conversion, Unicode normalization |

---

### 📌 OOV
*Out-of-Vocabulary*

| | |
| :--- |:---|
| **🗓️ Ne zaman?** | 11.02.2026 |
| **📍 Nerede?** | Problem Kısıtları (Kısıt 3) |
| **❓ Ne işe yarar?** | Modelin eğitim verisinde **olmayan** kelimeleri ifade eder |
| **💡 Basit örnek** | Yeni seçilen bir bakanın soyadı, yeni kurulan bir şirket, yapay isimler |
| **📚 Benzer terimler** | Unknown words, Unseen tokens, Rare words |

---

### 📌 Entity Normalization

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 11.02.2026 |
| **📍 Nerede?** | Problem tanımı, Yazım Hataları Sınıflandırması |
| **❓ Ne işe yarar?** | Aynı varlığın farklı yazımlarını standart forma getirir |
| **💡 Basit örnek** | `Turkiye`, `Turkey`, `TURKIYE`, `Türkiye Cumhuriyeti` → **`Türkiye`** |
| **🧠 Neden gerekli?** | Bilgisayar `Apple`, `Apple Inc.`, `apple`'ı **4 farklı şirket** sanar. Normalizasyon hepsini tek ID altında birleştirir. |
| **🛠️ Nasıl çalışır?** | **1. Yazımsal temizlik:** Büyük/küçük harf, noktalama, boşluk <br> **2. Sözlük eşleştirme:** `ABD` = `USA` = `Amerika` <br> **3. Belirsizlik çözümü:** "Amazon" → orman mı? şirket mi? |
| **🎯 Entity Linking farkı?** | **Normalization:** Standart forma sokar (`RTE` → `Recep Tayyip Erdoğan`) <br> **Linking:** Bilgi bankasına bağlar (`Recep Tayyip Erdoğan` → `wikidata.org/Q57418`) |
| **📚 Benzer terimler** | Entity resolution, Entity linking, Entity alignment, Name normalization, Record linkage |


---

### 📌 NER
*Named Entity Recognition*

| |                                                                        |
| :--- |:-----------------------------------------------------------------------|
| **🗓️ Ne zaman?** | 11.02.2026                                                             |
| **📍 Nerede?** | Problem tanımı, Hata Sınıflandırması                                   |
| **❓ Ne işe yarar?** | Metindeki özel isimleri (kişi, yer, kurum) bulur ve kategorize eder    |
| **💡 Basit örnek** | `"Joe Biden Washington'da"` → `[Joe Biden: KİŞİ]`, `[Washington: YER]` |
| **📚 Benzer terimler** | NER tagging, IOB tagging, Span detection, Entity extraction            |

---

### 📌 Context-Aware Spelling Correction

| | |
| :--- |:---|
| **🗓️ Ne zaman?** | 11.02.2026 |
| **📍 Nerede?** | Problem tanımı, Genel İngilizce Yazım Hataları |
| **❓ Ne işe yarar?** | Cümlenin bağlamına bakarak yazım hatalarını düzeltir |
| **💡 Basit örnek** | `"The goverment announced"` → **`"The government announced"`** |
| | `"I have a brown cat"` → ❌ **Düzeltmez** (çünkü `"brown"` doğru) |
| **📚 Benzer terimler** | Grammatical Error Correction (GEC), Spell checking, Proofreading |

### 📌 Noisy Text Normalization

| | |
| :--- |:---|
| **🗓️ Ne zaman?** | 11.02.2026 |
| **📍 Nerede?** | Problem tanımı, De-asciification |
| **❓ Ne işe yarar?** | OCR, klavye, sosyal medya gibi kaynaklardan gelen **kirli metni** temizler |
| **💡 Basit örnek** | `"Th3 c@p1t@l 0f Turkiye is Ankara."` → **`"The capital of Türkiye is Ankara."`** |
| **📚 Benzer terimler** | Text cleaning, Text preprocessing, De-asciification, Text denoising |

---

### 📌 BERT
*Bidirectional Encoder Representations from Transformers*

| |                                                                                      |
| :--- |:-------------------------------------------------------------------------------------|
| **🗓️ Ne zaman?** | 12.02.2026                                                                           |
| **📍 Nerede?** | Literatür taraması                                                                   |
| **❓ Ne işe yarar?** | Metindeki kelimeleri çift yönlü okuyarak bağlamı anlar                               |
| **💡 Basit örnek** | `"Erdoğan cumhurbaşkanıdır"` → `"Erdoğan"` kelimesinin kişi olduğunu bağlamdan anlar |
| **📚 Benzer terimler** | RoBERTa, ALBERT, DistilBERT, Transformer                                             |

---

### 📌 GECToR
*Grammatical Error Correction: Tag, Not Rewrite*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 12.02.2026 |
| **📍 Nerede?** | Literatür taraması |
| **❓ Ne işe yarar?** | Metni yeniden yazmak yerine **etiket atayarak** hata düzeltir |
| **💡 Basit örnek** | **Geleneksel yöntem (Seq2Seq):** <br> `"goed"` → `"went"` (tüm kelimeyi sil, yeni kelime yaz) <br><br> **GECToR yöntemi:** <br> `"goed"` → `"$APPEND_went"` (kelimeye etiket ekle, nasıl dönüşeceğini söyle) |
| **🧠 Nasıl çalışır?** | 1. BERT cümleyi vektörlere çevirir <br> 2. Her kelime için bir **etiket** tahmin eder <br> 3. Etiketler dönüşüm kuralını belirtir: <br> &nbsp;&nbsp;&nbsp; • `$KEEP` → olduğu gibi bırak <br> &nbsp;&nbsp;&nbsp; • `$DELETE` → sil <br> &nbsp;&nbsp;&nbsp; • `$APPEND_went` → sonuna "went" ekle <br> &nbsp;&nbsp;&nbsp; • `$REPLACE_went` → "went" ile değiştir |
| **⚡ Seq2Seq'ten farkı?** | **Seq2Seq:** Tüm cümleyi **sıfırdan üretir** → yavaş, pahalı, çok parametre <br> **GECToR:** Sadece **hatalı kısma etiket** atar → hızlı, hafif, az parametre |
| **📊 Performans** | • Seq2Seq'ten **5-10 kat daha hızlı** <br> • Daha az veriyle eğitilir <br> • Benzer veya daha iyi doğruluk |
| **🎯 Neden önemli?** | Gerçek zamanlı düzeltme yapabilir. Haber akışında anında çalışır. |
| **📚 Benzer terimler** | Seq2seq, Transformer, Sequence tagging, BERT |

---

### 📌 Transformer
*"Attention Is All You Need" - Vaswani et al. 2017*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 12.02.2026 |
| **📍 Nerede?** | Literatür taraması |
| **❓ Ne işe yarar?** | **NLP'de devrim yaratan mimari.** <br> • 2017 öncesi: LSTM/RNN (kelimeleri **tek tek** okur, yavaş) <br> • 2017 sonrası: Transformer (kelimeleri **aynı anda** okur, hızlı) |
| **💡 Basit örnek** | **LSTM/RNN:** <br> `"Ben [bugün] [okula] [gittim]"` <br> → 1. "Ben" oku → 2. "bugün" oku → 3. "okula" oku → 4. "gittim" oku <br> ❌ İlk kelimeyi okurken son kelimeyi bilmez <br> ❌ Uzun cümlelerde başı unutur <br><br> **Transformer:** <br> `"Ben bugün okula gittim"` <br> → **Tüm kelimeleri AYNI ANDA görür!** <br> ✅ "gittim" kelimesini okurken "Ben" kelimesini de görür <br> ✅ Bağlamı tam anlar, hiçbir şeyi unutmaz |
| **🧠 Self-Attention nedir?** | Her kelimenin, cümledeki **diğer tüm kelimelerle** ilişkisini hesaplama: <br><br> `"O bankaya para yatırdı."` <br> → "bankaya" kelimesi **"para"** ve **"yatırdı"** ile güçlü ilişkili → 🏦 BANKA <br><br> `"Nehir kenarında oturdu."` <br> → "kenarında" kelimesi **"nehir"** ile güçlü ilişkili → 🌊 NEHİR BANKASI <br><br> ✅ **Aynı kelime ("banka"), farklı bağlamlarda FARKLI vektör temsili alır!** |
| **🏗️ Mimari yapısı** | **Encoder-Decoder:** <br> • **Encoder:** Metni anlar, vektöre çevirir (BERT) <br> • **Decoder:** Vektörden yeni metin üretir (GPT) <br><br> **Multi-head Attention (Çok başlı dikkat):** <br> • 1. baş: Kelimelerin **gramer** ilişkisini öğrenir <br> • 2. baş: Kelimelerin **anlam** ilişkisini öğrenir <br> • 3. baş: Kelimelerin **konum** ilişkisini öğrenir <br> • 4. baş: **Zamir** ilişkisini öğrenir (o/onun) <br> • 5. baş: **Zıtlık** ilişkisini öğrenir <br> • ... 12+ baş farklı özellik öğrenir |
| **📊 LSTM vs Transformer** | **LSTM/RNN:** <br> ❌ Sıralı işlem → 100 kelime = 100 adım <br> ❌ Uzun cümlelerde başı unutur <br> ❌ Paralel işleme yok = GPU'yu tam kullanamaz <br> ❌ 500+ kelimede performans düşer <br><br> **Transformer:** <br> ✅ Paralel işlem → 100 kelime = 1 adım <br> ✅ 1000+ kelimeyi de hatırlar <br> ✅ GPU'yu %100 kullanır, çok hızlı <br> ✅ 10.000 kelimeye kadar çıkabilir |
| **🔧 Kullanan modeller** | • **BERT** - Sadece Encoder (metin anlama) <br> • **GPT** - Sadece Decoder (metin üretme) <br> • **T5** - Encoder + Decoder (çeviri, özet) <br> • **BART** - Encoder + Decoder (metin onarma) <br> • **RoBERTa** - BERT'in gelişmişi <br> • **GECToR** - BERT + etiketleme |
| **📚 Benzer terimler** | Self-attention, Multi-head attention, Encoder-Decoder, Positional encoding, BERT, GPT |


---


### 📌 Fine-tuning

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 12.02.2026 |
| **📍 Nerede?** | Literatür taraması |
| **❓ Ne işe yarar?** | Önceden eğitilmiş modeli yeni bir veri setiyle özelleştirme |
| **💡 Basit örnek** | Genel BERT → Haber metinleriyle eğitilmiş BERT |
| **📚 Benzer terimler** | Transfer learning, Pre-training, Domain adaptation |

---

### 📌 OCR
*Optical Character Recognition*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 12.02.2026 |
| **📍 Nerede?** | Literatür taraması, Noisy Text Normalization |
| **❓ Ne işe yarar?** | Taranmış belgeler, PDF'ler veya fotoğraflardaki yazıları dijital metne çevirir |
| **💡 Basit örnek** | Taranmış bir gazete kupürü → `"Türkiye"` yazısı bilgisayarda **düzenlenebilir metin** olur |
| **⚠️ OCR hataları** | **Harf karışıklıkları:** <br> • `"Türkiye"` → `"Turkiye"` (ü→u) <br> • `"İstanbul"` → `"Istanbul"` (İ→I) <br> • `"Erdoğan"` → `"Erdogan"` (ğ→g) <br><br> **Benzer harfler:** <br> • `"O"` ve `"0"` karışması <br> • `"l"` (küçük L) ve `"1"` (bir) karışması <br> • `"rn"` → `"m"` olarak okunması |
| **🧠 Projeyle ilişkisi** | OCR hataları = **Noisy Text**'in ana kaynaklarından biri <br> • Gazete arşivleri (taranmış) <br> • Eski belgeler, PDF'ler <br> • Dijitalleştirilmiş haber metinleri |
| **🔧 Çözüm** | **De-asciification** + **Context-Aware Spelling Correction** ile OCR hataları düzeltilir |
| **📚 Benzer terimler** | Document scanning, Text digitization, Document analysis, OCR post-correction |

---

### 📌 Multi-Head Attention
*Çok Başlı Dikkat Mekanizması*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, Transformer mimarisi |
| **❓ Ne işe yarar?** | Cümledeki kelimeler arasındaki **farklı ilişki türlerini** aynı anda öğrenir |
| **💡 Basit örnek** | Bir cümleyi **farklı uzmanlara** aynı anda inceletmek gibi: <br> • 1. uzman: Kim kimi işaret ediyor? (zamirler) <br> • 2. uzman: Hangi kelimeler anlamca yakın? <br> • 3. uzman: Cümledeki zıtlıklar neler? <br> • 4. uzman: Dil bilgisi yapısı nasıl? |
| **🧠 Neden gerekli?** | Tek bir dikkat mekanizması **her şeyi aynı anda** öğrenmek zorunda kalır. <br> Çok başlı dikkat ile **her baş farklı bir özelliğe odaklanır**, sonra hepsi birleştirilir. |
| **🛠️ Nasıl çalışır?** | **Adım 1:** Girdi cümlesi 8 farklı kopyaya çoğaltılır <br> **Adım 2:** Her kopya farklı bir "dikkat başlığı" tarafından işlenir <br> **Adım 3:** Her baş farklı ilişkiler öğrenir <br> **Adım 4:** Tüm başların çıktıları birleştirilir |
| **🔧 Transformer'daki yeri** | • **BERT:** 12 başlı dikkat (base model) <br> • **BERT-large:** 16 başlı dikkat <br> • **GPT-3:** 96 başlı dikkat |
| **📚 Benzer terimler** | Self-attention, Transformer, Attention mechanism, Encoder-Decoder attention |

---
### 📌 Positional Encoding
*Konumsal Kodlama / Pozisyonel Kodlama*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, Transformer mimarisi |
| **❓ Ne işe yarar?** | Transformer modeline **kelimelerin cümle içindeki sırasını** öğretir |
| **💡 Basit örnek** | **Transformer olmadan önce (LSTM/RNN):** <br> Kelimeler sırayla okunur → sıra bilgisi **otomatik** öğrenilir <br><br> **Transformer'da:** <br> Tüm kelimeler **aynı anda** okunur → "Hangi kelime önce geldi?" bilgisini kaybeder <br> → **Positional Encoding** kelimelere "Ben 1. kelimeyim", "Ben 2. kelimeyim" etiketi yapıştırır |
| **🧠 Neden gerekli?** | `"Köpek adamı ısırdı"` ile `"Adam köpeği ısırdı"` aynı kelimeler ama **tam tersi anlam**! <br> Sıra bilgisi olmadan Transformer bunları **ayırt edemez**. |
| **🛠️ Nasıl çalışır?** | **Adım 1:** Her kelimeye bir vektör atanır (anlamı) <br> **Adım 2:** Kelimenin cümledeki sırasına göre bir **pozisyon vektörü** hesaplanır <br> **Adım 3:** Anlam vektörü + Pozisyon vektörü = Transformer'a giren **son vektör** <br><br> `["Ben", "okula", "gidiyorum"]` <br> → "Ben" = anlam vektörü + (1. pozisyon vektörü) <br> → "okula" = anlam vektörü + (2. pozisyon vektörü) <br> → "gidiyorum" = anlam vektörü + (3. pozisyon vektörü) |
| **📐 Formül (Teknik)** | **Sinüzoidal fonksiyonlar** kullanılır: <br> • Çift indeksler için: `sin(pos/10000^(2i/d))` <br> • Tek indeksler için: `cos(pos/10000^(2i/d))` <br><br> *Sebep:* Sinüs ve kosinüs sayesinde model **göreceli pozisyonları** (2. kelime ile 5. kelime arası) öğrenebilir. |
| **🔧 Alternatifler** | **Öğrenilebilir Positional Encoding:** <br> • Sinüzoidal formül yerine modelin **kendi öğrenmesi** sağlanır <br> • GPT gibi modeller bunu kullanır <br><br> **Relative Positional Encoding:** <br> • Mutlak sıra yerine kelimelerin **birbirine göre mesafesi** öğrenilir |
| **📚 Benzer terimler** | Self-attention, Transformer, Position embedding, Sinusoidal encoding, Relative position bias |

---
### 📌 Masked Language Model (MLM)
*Maskeli Dil Modeli*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, BERT mimarisi |
| **❓ Ne işe yarar?** | BERT'in eğitim yöntemi. Cümledeki bazı kelimeleri **maskeler** ve modelden **tahmin etmesini** ister. |
| **💡 Basit örnek** | **Orijinal cümle:** `"İstanbul Türkiye'nin başkenti değildir"` <br> **Maskelenmiş:** `"İstanbul Türkiye'nin [MASK] değildir"` <br> **BERT'in tahmini:** `"başkenti"` ✅ |
| **🧠 Neden gerekli?** | **Geleneksel modeller (GPT):** Soldan sağa okur, bir sonraki kelimeyi tahmin eder <br> → `"Ben okula ___"` → `"gidiyorum"` <br><br> **BERT'in yaptığı:** Çift yönlü okur, **ortadaki** kelimeyi tahmin eder <br> → `"Ben ___ gidiyorum"` → `"okula"` |
| **🛠️ Nasıl çalışır?** | **Adım 1:** Cümledeki kelimelerin **%15'i** rastgele seçilir <br> **Adım 2:** Seçilen kelimelerin: <br> &nbsp;&nbsp;&nbsp; • %80'i `[MASK]` ile değiştirilir <br> &nbsp;&nbsp;&nbsp; • %10'u rastgele başka bir kelimeyle değiştirilir <br> &nbsp;&nbsp;&nbsp; • %10'u **aynen korunur** <br> **Adım 3:** Model maskelenen yerde **hangi kelime olması gerektiğini** tahmin eder |
| **🧪 Neden %100 MASK kullanılmıyor?** | Eğer hep `[MASK]` görürse, BERT **gerçek metinlerde** mask görmeyeceği için şaşırır. <br> • %80 MASK → Maskeyi tahmin etmeyi öğrenir <br> • %10 rastgele kelime → Hataları düzeltmeyi öğrenir <br> • %10 aynı kelime → Her zaman değişmeyeceğini de öğrenir |
| **🔧 BERT'ten sonra gelen modeller** | **RoBERTa:** %15 MASK, ara **hiç rastgele veya aynı kelime yok**, sadece MASK! <br> **SpanBERT:** Tek kelime yerine **kelime gruplarını** maskeler <br> **ELECTRA:** Maskeli kelimeyi tahmin etmek yerine, **hangi kelimenin değiştirildiğini** bulur |
| **📚 Benzer terimler** | Next Sentence Prediction (NSP), Autoregressive model, Denoising autoencoder, SpanBERT, RoBERTa |

---

### 📌 Next Sentence Prediction (NSP)
*Sonraki Cümle Tahmini*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, BERT mimarisi |
| **❓ Ne işe yarar?** | İki cümle arasındaki ilişkiyi öğrenir. İkinci cümlenin birinciyi takip edip etmediğini tahmin eder. |
| **💡 Basit örnek** | **Cümle A:** `"İstanbul çok kalabalık bir şehir."` <br> **Cümle B:** `"Her gün milyonlarca insan trafikte zaman kaybediyor."` <br> **Tahmin:** `IsNext` ✅ (Birbiriyle ilgili) <br><br> **Cümle A:** `"İstanbul çok kalabalık bir şehir."` <br> **Cümle B:** `"Kediler çok sevimli hayvanlardır."` <br> **Tahmin:** `NotNext` ❌ (Alakasız) |
| **📚 Benzer terimler** | Sentence order prediction, Document-level understanding |

---

### 📌 Embeddings from Language Models (ELMo)
*Dil Modellerinden Elde Edilen Gömmeler*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması |
| **❓ Ne işe yarar?** | Kelimelere **cümle içindeki bağlama göre** vektör atar. Aynı kelime farklı cümlelerde farklı vektör temsili alır. |
| **💡 Basit örnek** | **Cümle 1:** `"I read the book yesterday."` (read = geçmiş zaman) <br> **Cümle 2:** `"Can you read the letter now?"` (read = şimdiki zaman) <br><br> **Word2vec/GloVe:** İki cümledeki "read" kelimesine **aynı** vektörü verir ❌ <br> **ELMo:** İki cümledeki "read" kelimesine **farklı** vektörler verir ✅ |
| **🧠 Neden gerekli?** | Word2vec gibi geleneksel yöntemler bir kelimenin **tüm anlamlarını** tek bir vektöre sıkıştırır. <br> `"banka"` kelimesi: <br> • "Para çekmek için bankaya gittim" → 🏦 <br> • "Nehir bankasında oturduk" → 🌊 <br><br> ELMo, cümlenin tamamını okuyarak kelimenin **o cümledeki anlamını** yakalar. |
| **🛠️ Nasıl çalışır?** | **Adım 1:** Çift yönlü LSTM (biLM) eğitilir: <br> &nbsp;&nbsp;&nbsp; • İleri LSTM: soldan sağa okuyarak sonraki kelimeyi tahmin eder <br> &nbsp;&nbsp;&nbsp; • Geri LSTM: sağdan sola okuyarak önceki kelimeyi tahmin eder <br> **Adım 2:** Her kelime için 3 katman vektör üretilir: <br> &nbsp;&nbsp;&nbsp; • Katman 0: Kelimenin kendi embedding'i <br> &nbsp;&nbsp;&nbsp; • Katman 1: İlk LSTM katmanı çıktısı (dil bilgisi, syntax) <br> &nbsp;&nbsp;&nbsp; • Katman 2: İkinci LSTM katmanı çıktısı (anlam, semantics) <br> **Adım 3:** Bu 3 katmanın **ağırlıklı ortalaması** alınır (ağırlıklar göreve göre öğrenilir) |
| **🎯 Katmanların görevi** | • **Alt katman (LSTM1):** Dil bilgisi, sözdizimi (POS tagging, dependency) <br> • **Üst katman (LSTM2):** Anlam, bağlam (sentiment, QA, NER) <br><br> *Not:* Görev neyse, o görev için hangi katman daha önemliyse ağırlığı artar. |
| **⚙️ Teknik detay** | • Karakter seviyesinde CNN ile kelime temsili (OOV sorununa çözüm) <br> • 2 katman biLSTM <br> • 4096 hidden unit, 512 projection <br> • 1 milyar kelime benchmark verisiyle eğitilmiş |
| **📚 Benzer terimler** | BiLM (Bidirectional Language Model), Contextual embeddings, CoVe, LSTM, Character CNN |

---

### 📌 Dynamic Masking
*Dinamik Maskeleme*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, BERT eğitim yöntemleri |
| **❓ Ne işe yarar?** | Her eğitim adımında farklı token'ları rastgele maskeleyerek modelin daha çeşitli örnekler görmesini sağlar |
| **💡 Basit örnek** | **Statik Maskeleme (Eski yöntem):** <br> Aynı cümle her epoch'ta **aynı** maskelenmiş halde görülür <br> `"İstanbul [MASK] en kalabalık şehridir"` (her seferinde aynı) <br><br> **Dinamik Maskeleme (Yeni yöntem):** <br> Her epoch'ta **farklı** maskelenmiş haller görülür <br> • Epoch 1: `"İstanbul [MASK] en kalabalık şehridir"` <br> • Epoch 2: `"[MASK] Türkiye'nin en kalabalık şehridir"` <br> • Epoch 3: `"İstanbul Türkiye'nin [MASK] kalabalık şehridir"` |
| **🧠 Neden gerekli?** | **Statik maskeleme sorunları:** <br> • Token'ların %40'ı **nadiren** maskelenir <br> • %15'i **hiç** maskelenmez <br> • Model aynı maskeye alışır, ezberler <br><br> **Dinamik maskeleme avantajları:** <br> • Her token'ın maskelenme olasılığı artar <br> • 40 epoch sonunda **%99.9** token maskelenir <br> • Model gerçek dil kalıplarını öğrenir, ezberlemez |
| **📊 İstatistiksel fark** | **Statik:** <br> Bir token'ın maskelenme olasılığı = **%15** (sabit) <br><br> **Dinamik (40 epoch sonra):** <br> Bir token'ın maskelenme olasılığı = **1 - (1-0.15)⁴⁰ ≈ %99.9** |
| **📚 Benzer terimler** | Masked LM, Static Masking, BERT pre-training, Data augmentation, Token masking |

---

### 📌 Multi-Task Fine-Tuning
*Çok Görevli İnce Ayar*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, model eğitim yöntemleri |
| **❓ Ne işe yarar?** | Tek bir modeli aynı anda birden fazla görevde (örneğin NER + Spelling Correction + Entity Normalization) eğiterek hem görevler arası bilgi paylaşımını sağlar hem de modelin genel başarımını artırır. |
| **💡 Basit örnek** | **Single-Task Fine-Tuning (Tek Görev):** <br> • Model 1: Sadece NER öğrenir `(Erdoğan → KİŞİ)` <br> • Model 2: Sadece Spelling Correction öğrenir `(goverment → government)` <br> • Model 3: Sadece Entity Normalization öğrenir `(Turkiye → Türkiye)` <br><br> **Multi-Task Fine-Tuning (Çok Görev):** <br> Tek bir model **hepsini aynı anda** öğrenir: <br> • `"Erdogan goverment"` → `"Erdoğan government"` <br> • Aynı model, kelimeyi hem düzeltir (`goverment`) hem normalize eder (`Erdogan`) hem de özel isim olduğunu bilir (`Erdoğan` = KİŞİ) |
| **🧠 Nasıl çalışır?** | **Adım 1:** Modele aynı anda farklı görevler için hazırlanmış veri setleri gösterilir <br> **Adım 2:** Her görev için ayrı bir çıkış katmanı (head) eklenir <br> **Adım 3:** Eğitim sırasında görevler arasında geçiş yapılır veya görevler karışık olarak verilir <br> **Adım 4:** Modelin alt katmanları (gövde/body) tüm görevler için **ortak** özellikleri öğrenirken, üst katmanlar (head) görevlere özgü çıktılar üretir |
| **🎯 Avantajları** | • **Bilgi paylaşımı:** Bir görevde öğrenilen özellikler diğer göreve de fayda sağlar (transfer learning) <br> • **Verimlilik:** Tek model = daha az bellek, daha az işlem gücü <br> • **Genelleme:** Farklı görevler gören model, her bir görevde daha sağlam (robust) hale gelir <br> • **Düşük kaynaklı diller/görevler:** Az verisi olan görevler, çok verisi olan görevlerden öğrenir |
| **⚡ Zorlukları** | • **Negatif transfer:** Görevler birbirine zarar verebilir (çok farklı görevler) <br> • **Görev çakışması:** Farklı görevler aynı girdi için farklı çıktı isteyebilir <br> • **Eğitim zorluğu:** Görevler arası dengeyi kurmak (loss weighting) hassas ayar gerektirir |
| **📚 Benzer terimler** | Multi-task learning (MTL), Transfer learning, Joint training, Multi-head architecture, Negative transfer, Loss weighting, Task balancing |

---

### 📌 Damerau–Levenshtein Distance
*Damerau–Levenshtein Mesafesi*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, yazım düzeltme yöntemleri |
| **❓ Ne işe yarar?** | İki kelime arasındaki **benzerliği** ölçer. Bir kelimeyi diğerine çevirmek için gereken **minimum işlem sayısını** hesaplar. |
| **💡 Basit örnek** | `"Erdogan"` → `"Erdoğan"` dönüşümü için: <br> • `g` → `ğ` (değiştirme) <br> • Toplam işlem = **1** <br><br> `"recieve"` → `"receive"` dönüşümü için: <br> • `ie` → `ei` (yer değiştirme) <br> • Toplam işlem = **1** |
| **🧠 Levenshtein'den farkı?** | **Levenshtein:** 3 işlem <br> • Ekleme (Insert) <br> • Silme (Delete) <br> • Değiştirme (Substitute) <br><br> **Damerau–Levenshtein:** 4 işlem ✅ <br> • Ekleme (Insert) <br> • Silme (Delete) <br> • Değiştirme (Substitute) <br> • **Yer değiştirme (Transposition)** 👈 YENİ! <br><br> **Örnek:** `"ie"` → `"ei"` (iki harfin yer değiştirmesi) |
| **📊 İşlem türleri** | **Ekleme:** `"erdgan"` → `"erdogan"` (o harfi eklendi) <br> **Silme:** `"erdoğann"` → `"erdoğan"` (fazla n silindi) <br> **Değiştirme:** `"erdogan"` → `"erdoğan"` (g → ğ) <br> **Yer değiştirme:** `"recieve"` → `"receive"` (ie → ei) |
| **🔧 Nerede kullanılır?** | • **Yazım düzeltme:** `"turkiye"` ile `"türkiye"` benzer mi? <br> • **OCR hata düzeltme:** `"Türkiye"` → `"Turkiye"` (ü→u) <br> • **De-asciification:** ASCII'ye çevrilmiş kelimeleri geri getirme <br> • **Fonetik benzerlik:** `"erdoan"` ile `"erdoğan"` arasındaki fark |
| **📚 Benzer terimler** | Levenshtein distance, Edit distance, Hamming distance, Jaro-Winkler distance, String similarity, Fuzzy matching |

---

### 📌 String-to-String
*Dizeden Dizeye / Karakter Dizisinden Karakter Dizisine*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, metin işleme yöntemleri |
| **❓ Ne işe yarar?** | Bir metin parçasını (string) başka bir metin parçasına dönüştüren işlemleri veya algoritmaları ifade eder. |
| **💡 Basit örnek** | **String-to-String işlemleri:** <br> • `"Turkiye"` → `"Türkiye"` (de-asciification) <br> • `"goverment"` → `"government"` (spelling correction) <br> • `"Erdogan"` → `"Erdoğan"` (karakter normalizasyonu) <br> • `"Joe Biden Washington'da"` → `"[KİŞİ] [YER]'da"` (NER etiketleme) |
| **🧠 Kullanım alanları** | • **Metin normalizasyonu:** Farklı yazımları standart forma getirme <br> • **Yazım düzeltme:** Hatalı kelimeleri doğru hale getirme <br> • **Makine çevirisi:** Bir dilden başka bir dile çeviri <br> • **Metin sadeleştirme:** Karmaşık metni basitleştirme <br> • **Paraphrase:** Aynı anlamı farklı kelimelerle ifade etme |
| **🔧 String-to-String modelleri** | • **Seq2Seq (Sequence-to-Sequence):** Encoder-Decoder mimarisi ile bir diziyi başka bir diziye çevirir <br> • **Transformer:** Self-attention ile daha başarılı string-to-string dönüşümler <br> • **T5 (Text-to-Text Transfer Transformer):** Tüm NLP görevlerini string-to-string problemi olarak modeller <br> • **GPT:** Verilen string'e uygun devam string'i üretir |
| **📚 Benzer terimler** | Sequence-to-sequence (Seq2Seq), Text-to-text, String transformation, Text normalization, String rewriting |

---

### 📌 Soft-Masked BERT
*Yumuşak Maskeli BERT*

| |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **🗓️ Ne zaman?** | 17.02.2026                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **📍 Nerede?** | Literatür taraması, yazım düzeltme modelleri                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **❓ Ne işe yarar?** | Metin hatalarını düzeltmek için tasarlanmış, **algılama (detection)** ve **düzeltme (correction)** ağlarını birleştiren BERT tabanlı bir modeldir.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **💡 Basit örnek** | **Girdi:** `"Bugün hava çok sıcak, dışarı çıkmak istyorum."` <br> **Soft-Masked BERT:** <br> • **Algılama ağı:** `"istiyorum"` kelimesinde `"i"` harfinin eksik olduğunu tespit eder <br> • **Yumuşak maskeleme:** Hatalı bölgeye odaklanır <br> • **Düzeltme ağı (BERT):** `"istiyorum"` olarak düzeltir <br> **Çıktı:** `"Bugün hava çok sıcak, dışarı çıkmak istiyorum."`                                                                                                                                                                                                                                                                                                                                                   |
| **🧠 Neden gerekli?** | **BERT'in tek başına sorunu:** <br> • BERT, Masked LM ile eğitilirken kelimeleri **rastgele maskeler** <br> • Bu nedenle **bir kelimenin hatalı olup olmadığını tespit etme** konusunda zayıftır <br><br> **Soft-Masked BERT'in çözümü:** <br> • **Algılama ağı** (Bi-GRU) hangi kelimelerin hatalı olduğunu bulur <br> • **Yumuşak maskeleme** ile sadece hatalı bölgelere odaklanılır <br> • **Düzeltme ağı (BERT)** bu odaklanmış bölgeleri düzeltir                                                                                                                                                                                                                                                                        |
| **🛠️ Mimari yapısı** | **1. Algılama Ağı (Detection Network):** <br> • Bi-GRU (Çift yönlü GRU) kullanır <br> • Her karakter için **hata olasılığı** `(p_i)` hesaplar (0-1 arası) <br> • `p_i` 1'e yakınsa hatalı, 0'a yakınsa doğru <br><br> **2. Yumuşak Maskeleme (Soft-Masking):** <br> • Girdi embedding'i `(e_i)` ile maskeleme embedding'i `(e_mask)` arasında geçiş yapar <br> • `e'_i = p_i * e_mask + (1 - p_i) * e_i` <br> • Hatalı bölgeler `e_mask`'e yaklaşır, doğru bölgeler orijinal halini korur <br><br> **3. Düzeltme Ağı (Correction Network):** <br> • BERT tabanlıdır <br> • Yumuşak maskelenmiş embedding'leri alır, doğru karakterleri üretir <br> • Çıkışta **residual connection** ve **softmax** ile karakter tahmini yapar |
| **⚡ Güçlü yönleri** | • **Hata tespiti:** BERT'in zayıf olduğu hata bulma işini özel bir ağ ile çözer <br> • **Yumuşak geçiş:** Keskin maskeleme yerine kademeli geçiş ile daha doğal öğrenme <br> • **Uçtan uca eğitim:** Tüm ağ birlikte eğitilir                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **📚 Benzer terimler** | BERT, Masked LM, Bi-GRU, Sequence tagging, Chinese spelling correction (CSC), Error detection, Residual connection                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

---
### 📌 C2C
*Character-to-Character / Karakterden Karaktere*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 17.02.2026 |
| **📍 Nerede?** | Literatür taraması, metin düzeltme modelleri |
| **❓ Ne işe yarar?** | Bir metindeki hatalı karakterleri tespit edip düzelten, **her bir karaktere odaklanan** yaklaşımları ifade eder. |
| **💡 Basit örnek** | **Örnek 1 - De-asciification:** <br> `"Turkiye"` → `"Türkiye"` <br> • `T` → `T` (doğru) <br> • `u` → `ü` (hatalı → düzelt) <br> • `r` → `r` (doğru) <br> • `k` → `k` (doğru) <br> • `i` → `i` (doğru) <br> • `y` → `y` (doğru) <br> • `e` → `e` (doğru) <br><br> **Örnek 2 - Klavye hatası:** <br> `"Ankara'ya gidiyroum"` → `"Ankara'ya gidiyorum"` <br> • `A n k a r a ' y a   g i d i y r o u m` (her karakter ayrı işlenir) <br> • `r` ve `o` harflerinin yeri değişmiş → `r o` → `o r` olarak düzeltilir |
| **🧠 Neden gerekli?** | • **Kelime seviyesi modeller** bilinmeyen kelimelerde (OOV) başarısız olur <br> • **C2C modeller** her karakteri tek tek işleyerek OOV sorununu çözer <br> • Özellikle **Türkçe karakter dönüşümleri** (ü,ğ,ş,ı,ö,ç) için idealdir <br> • **OCR hataları** gibi karakter bazlı bozulmalarda etkilidir |
| **🛠️ Kullanım alanları** | • **De-asciification:** `"Turkiye"` → `"Türkiye"`, `"Istanbul"` → `"İstanbul"` <br> • **OCR düzeltme:** Karakter tanıma hatalarını düzeltme (`"Türkiye"` → `"Turkiye"` gibi) <br> • **Yazım düzeltme:** `"istiyorum"` → `"istiyorum"` <br> • **Metin normalizasyonu:** Farklı yazım standartlarını birleştirme <br> • **Sosyal medya metinleri:** `"naber gençler nasıl gidiyo"` → `"naber gençler nasıl gidiyor"` |
| **📊 Karşılaştırma** | **Word-level (Kelime seviyesi):** <br> `"Erdogan"` kelime olarak aranır, sözlükte yoksa düzeltemez ❌ <br><br> **C2C (Karakter seviyesi):** <br> `E r d o g a n` karakterleri tek tek işlenir: <br> • `E` (doğru), `r` (doğru), `d` (doğru) <br> • `o` → `ö` olmalı, `g` → `ğ` olmalı ✅ |
| **⚡ Avantajları** | • **OOV sorunu yok:** Hiç görülmemiş kelimeleri bile düzeltebilir <br> • **Dil bağımsız:** Türkçe, İngilizce, Çince fark etmez <br> • **Esnek:** Her türlü karakter hatasını yakalar |
| **⚠️ Dezavantajları** | • **Yavaş:** Kelime seviyesi modellere göre daha yavaş <br> • **Bağlam zayıf:** Kelimenin anlamını tam kavrayamayabilir <br> • **Dil bilgisi:** Cümle yapısını anlamakta zorlanır |
| **📚 Benzer terimler** | Character-level model, Character-based correction, Sequence labeling, Character CNN, Byte-Pair Encoding (BPE), Subword tokenization, Character embedding |

---
### 📌Bidirectional and Auto-Regressive Transformer (BART) 
*Çift Yönlü ve Otoregresif Dönüştürücü* 

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, metin üretim modelleri |
| **❓ Ne işe yarar?** | Metin oluşturma (özetleme, çeviri) ve anlama görevleri için kullanılan, **BERT ve GPT'yi birleştiren** bir modeldir. |
| **💡 Basit örnek** | `"UN Chief Says There Is No <mask> in Syria"` → `"UN Chief Says There Is No Plan to Stop Chemical Weapons in Syria"` |
| **📚 Benzer terimler** | BERT, GPT, T5, RoBERTa, Seq2Seq, Encoder-Decoder |

---

### 📌 Automatic Speech Recognition (ASR)
*Otomatik Konuşma Tanıma*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, konuşma işleme |
| **❓ Ne işe yarar?** | İnsan konuşmasını yazılı metne dönüştürür. |
| **💡 Basit örnek** | Ses kaydı: "Merhaba" → `"Merhaba"` |
| **⚠️ ASR hataları** | Homofonlar, telaffuz farklılıkları, arka plan gürültüsü |
| **📚 Benzer terimler** | Speech-to-Text, Voice Recognition, STT |

---

### 📌 Word Error Rate (WER)
*Kelime Hata Oranı*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, ASR değerlendirme metrikleri |
| **❓ Ne işe yarar?** | ASR sistemlerinin doğruluğunu ölçen en yaygın metriktir. |
| **💡 Basit örnek** | Referans: `"Bugün hava çok güzel"` (4 kelime) <br> ASR: `"Bugün hav çok güzel"` (1 hata) <br> **WER = 1/4 = %25** |
| **🧠 Hesaplama** | WER = (Değiştirme + Silme + Ekleme) / Toplam Kelime |
| **📚 Benzer terimler** | CER, Accuracy, Precision, Recall |

---

### 📌 Heavy Encoder
*Ağır Kodlayıcı / Yoğun Kodlayıcı*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, derin öğrenme mimarileri |
| **❓ Ne işe yarar?** | Genellikle **çok büyük ve karmaşık** encoder modellerini ifade eder. Büyük parametre sayısı, çok sayıda katman ve yüksek işlem gücü gerektiren modeller için kullanılan gayriresmî bir terimdir. |
| **💡 Basit örnek** | ModernBERT-large (28 katman, 395 milyon parametre) gibi büyük encoder modelleri “heavy encoder” sınıfına girer. |
| **🧠 Nerede kullanılır?** | • Uzun metinleri anlama (16.000 token’a kadar) <br> • Karmaşık doğal dil anlama görevleri <br> • Büyük ölçekli metin sınıflandırma <br> • Domain-specific modeller (biyomedikal, klinik, kod) |
| **📚 Benzer terimler** | Large Encoder, Deep Encoder, Transformer Encoder, BERT-large, ModernBERT |

---
### 📌 CANINE
*Character Architecture with No tokenization In Neural Encoders*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, tokenization-free modeller |
| **❓ Ne işe yarar?** | **Açık tokenizasyon adımı (BPE, WordPiece, SentencePiece) kullanmayan** Transformer tabanlı bir dil modelidir. Doğrudan Unicode karakter seviyesinde çalışır. |
| **💡 Basit örnek** | Girdi: `"hello world"` → Her karakter Unicode kod noktasına çevrilir: `[104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]` → Model doğrudan bu karakter ID'leri ile çalışır. |
| **🧠 Nasıl çalışır?** | • **3 Transformer encoder** kullanır: <br> &nbsp;&nbsp; 1. **Shallow encoder (ilk):** Karakter embedding'lerini yerel dikkat ile bağlamlandırır <br> &nbsp;&nbsp; 2. **Deep encoder:** Downsampling sonrası normal BERT benzeri derin encoder uygulanır <br> &nbsp;&nbsp; 3. **Shallow encoder (son):** Upsampling sonrası final karakter embedding'lerini oluşturur <br> • **Downsampling:** 4 kat örnekleme azaltma ile uzun karakter dizilerini yönetilebilir hale getirir |
| **📊 Varyantlar** | • **google/canine-c:** Otoregresif karakter kaybı ile ön eğitim almış model <br> • **google/canine-s:** Subword kaybı ile ön eğitim almış model <br> • Her ikisi de: 12 katman, 768 hidden, 12 başlık, 121M parametre |
| **⚡ Öne çıkan özellik** | • Tokenizer **tamamen opsiyonel** - Python `ord()` ile direkt çalışır <br> • Maksimum dizi uzunluğu: **2048 karakter** <br> • mBERT'e kıyasla **%28 daha az parametre** ile TyDi QA'da **+2.8 F1** |
| **📚 Benzer terimler** | Character-level model, Tokenization-free, ByT5, Charformer, Perceiver, mBERT, Unicode |

---

### 📌 Entity Linking
*Varlık Bağlama*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, bilgi çıkarımı |
| **❓ Ne işe yarar?** | Metinde geçen bir varlık ifadesini (örneğin "Türkiye") bir bilgi tabanındaki (örneğin Wikipedia, Wikidata) **benzersiz bir varlığa bağlar**. |
| **💡 Basit örnek** | Metin: `"Ankara, Türkiye'nin başkentidir."` <br> • `"Türkiye"` → `wikidata.org/Q43` <br> • `"Ankara"` → `wikidata.org/Q3640` |
| **🧠 Nasıl çalışır?** | 1. **Varlık tespiti (NER):** Varlık ifadeleri bulunur <br> 2. **Aday oluşturma:** Bilgi tabanında aynı/isimli varlıklar listelenir <br> 3. **Bağlam tabanlı sıralama:** En uygun aday seçilir |
| **🎯 Entity Normalization farkı?** | **Normalization:** `Turkiye` → `Türkiye` (yazım düzeltme) <br> **Linking:** `Türkiye` → `wikidata.org/Q43` (bilgi tabanına bağlama) |
| **📚 Benzer terimler** | Entity Resolution, Entity Disambiguation, Record Linkage, Knowledge Base Population, Wikidata |

---

### 📌 Mention Detection
*Bahsetme Tespiti / Varlık Tespiti*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, bilgi çıkarımı, NER |
| **❓ Ne işe yarar?** | Metin içinde **bir varlığa işaret eden ifadeleri (mention)** bulur. NER'in bir alt aşaması veya alternatifidir. |
| **💡 Basit örnek** | Metin: `"Joe Biden, Kamala Harris ile Washington'da görüştü."` <br> **Mention Detection çıktısı:** <br> • `"Joe Biden"` <br> • `"Kamala Harris"` <br> • `"Washington"` |
| **🧠 NER ile farkı?** | • **NER:** Varlık mention'larını bulur + türünü (kişi, yer, kurum) de etiketler <br> • **MD:** Sadece varlık mention'larını bulur, tür belirtmek zorunda değildir |
| **📚 Benzer terimler** | Named Entity Recognition (NER), Entity Detection, Span Detection, Entity Mention |

---

### 📌 Entity Disambiguation
*Varlık Anlam Belirsizliği Giderme*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | Literatür taraması, bilgi çıkarımı, Entity Linking |
| **❓ Ne işe yarar?** | Aynı ada sahip farklı varlıklar arasında, bağlama bakarak **doğru olanı seçme** işlemidir. |
| **💡 Basit örnek** | Metin: `"Paris Hilton'da kaldım."` <br> • **Aday 1:** Paris (Fransa'nın başkenti) 🏛️ <br> • **Aday 2:** Paris Hilton (ünlü sosyetik) 👤 <br><br> **ED çıktısı:** Bağlamdaki `"Hilton"` kelimesi sayesinde doğru anlamın **Paris Hilton** olduğunu belirler. |
| **🧠 Nasıl çalışır?** | 1. Aday varlıklar belirlenir (örneğin "Paris" için şehir ve kişi) <br> 2. Varlığın geçtiği cümle ve çevresi incelenir <br> 3. Bağlama en uygun aday seçilir |
| **🎯 İlişkili terimlerle farkı** | • **Entity Linking:** Metindeki varlığı bilgi tabanına bağlar (ED'yi içerir) <br> • **Entity Disambiguation:** Sadece anlam belirsizliğini çözer <br> • **Word Sense Disambiguation:** Kelimelerin anlamlarını çözer (varlık değil) |
| **📚 Benzer terimler** | Entity Linking, Word Sense Disambiguation (WSD), Entity Resolution, Name Disambiguation |

---

## STEP 2 - VERİ TOPLAMA
*Wikipedia'dan veri çekme, API kullanımı, metin işleme ve veri saklama sürecinde öğrenilen terimler*

---

### 📌 Natural Language Toolkit (NLTK)
*Doğal Dil Araç Takımı*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, Metin İşleme |
| **❓ Ne işe yarar?** | Python için doğal dil işleme (NLP) kütüphanesi. Tokenization, stemming, tagging, parsing gibi işlemler için araçlar sağlar. |
| **💡 Basit örnek** | `sent_tokenize("Merhaba dünya. Nasılsın?")` → `["Merhaba dünya.", "Nasılsın?"]` |
| **🧠 Projede kullanımı** | Wikipedia'dan çekilen metinleri cümlelere ayırmak için `sent_tokenize` kullanıldı |
| **📚 Benzer terimler** | spaCy, Tokenization, sent_tokenize, word_tokenize, Corpus |

---

### 📌 Tokenization
*Tokenleştirme*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, Metin Önişleme |
| **❓ Ne işe yarar?** | Metni daha küçük parçalara (kelime, cümle, alt kelime) ayırma işlemi. |
| **💡 Basit örnek** | **Cümle tokenization:** `"NLTK harika. Çok kullanışlı."` → `["NLTK harika.", "Çok kullanışlı."]` <br> **Kelime tokenization:** `"NLTK harika"` → `["NLTK", "harika"]` |
| **🧠 Projede kullanımı** | Wikipedia makalelerini cümlelere ayırmak için `sent_tokenize()` kullanıldı |
| **📚 Benzer terimler** | NLTK, spaCy, sent_tokenize, word_tokenize, Subword tokenization (BPE) |

---

### 📌 BeautifulSoup

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, Web Scraping |
| **❓ Ne işe yarar?** | HTML ve XML dosyalarını ayrıştırmak (parse) için kullanılan Python kütüphanesi. Web'den çekilen sayfalardan veri çıkarmayı kolaylaştırır. |
| **💡 Basit örnek** | `soup.find_all('p')` → HTML sayfasındaki tüm paragraf (`<p>`) etiketlerini bulur |
| **🧠 Projede kullanımı** | Wikipedia sayfalarından ana metin içeriğini çıkarmak için kullanıldı. Uyarıları engellemek için `GuessedAtParserWarning` filtrelendi. |
| **📚 Benzer terimler** | HTML parsing, Web scraping, lxml, html.parser, requests |

---

### 📌 Rate Limiting
*Hız Sınırlama*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, API Kullanımı |
| **❓ Ne işe yarar?** | Bir API'ye (uygulama programlama arayüzü) belirli bir sürede yapılan istek sayısını sınırlayarak sunucunun aşırı yüklenmesini veya IP ban'lenmesini engeller. |
| **💡 Basit örnek** | `time.sleep(0.25)` → Her istekten sonra 0.25 saniye bekle <br> → Saniyede 4 istekten fazlası engellenir |
| **🧠 Projede kullanımı** | Wikipedia'ya hızlı istek atıp IP ban yememek için her sayfa çekiminden sonra `time.sleep(0.25)` eklendi |
| **📚 Benzer terimler** | API throttling, Request limiting, time.sleep, Cooldown |

---

### 📌 Metadata
*Üst Veri*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, Veri Saklama |
| **❓ Ne işe yarar?** | Veri hakkında veri. Bir veri setinin kaynağı, toplanma zamanı, boyutu gibi tanımlayıcı bilgileri ifade eder. |
| **💡 Basit örnek** | `{"text": "Türkiye", "source_page": "Turkey", "word_count": 1, "collected_at": "2026-02-18T..."}` |
| **🧠 Projede kullanımı** | Her cümle için kaynak sayfa, kelime sayısı, toplanma zamanı gibi bilgiler JSON dosyasında metadata olarak saklandı. |
| **📚 Benzer terimler** | Data dictionary, Schema, JSON, Data provenance |

---

### 📌 JSON
*JavaScript Object Notation*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 18.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, Veri Saklama |
| **❓ Ne işe yarar?** | Verileri metin tabanlı, insan tarafından okunabilir formatta saklamak ve taşımak için kullanılan hafif bir veri değişim formatı. |
| **💡 Basit örnek** | `{"isim": "Türkiye", "nufus": 85000000}` |
| **🧠 Projede kullanımı** | Toplanan cümleler ve metadata JSON formatında `dataset_3000_target.json` ve `dataset_latest.json` dosyalarına kaydedildi. |
| **📚 Benzer terimler** | XML, YAML, CSV, Data serialization |

---

## STEP 3 - GÜRÜLTÜ EKLEME
*Sentetik hata üretimi, veri bozma ve hata tespiti sürecinde öğrenilen terimler*

---

### 📌 Regular Expressions (Regex)
*Düzenli İfadeler*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 19.02.2026 |
| **📍 Nerede?** | STEP 2 - Veri Toplama, STEP 3 - Gürültü Ekleme |
| **❓ Ne işe yarar?** | Metin içinde desen eşleştirme, arama, değiştirme ve ayıklama işlemleri için kullanılan güçlü bir dil. |
| **💡 Basit örnekler** | **1. Referans temizleme:** <br> `re.sub(r'\[\d+\]', '', text)` <br> `"Türkiye[1]"` → `"Türkiye"` <br><br> **2. Fazla boşluk temizleme:** <br> `re.sub(r'\s+', ' ', text)` <br> `"Çok    boşluk   var"` → `"Çok boşluk var"` <br><br> **3. Kelime sınırı ile arama:** <br> `re.search(r'\bgovernment\b', text)` <br> Sadece tam kelime olarak "government" arar. <br><br> **4. E-posta doğrulama:** <br> `r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'` |
| **🧠 Projede kullanımı** | • Wikipedia'dan çekilen metinlerde **referansları temizleme** (`\[\d+\]`) <br> • **Fazla boşlukları** ve **satır sonlarını** temizleme (`\s+`, `\n+`) <br> • **Noktalama düzeltmeleri** (`\s+\.`, `\s+,`) <br> • Yaygın hata kalıplarını yakalama (örneğin `\bgovernment\b`) <br> • Gürültü ekleme sırasında kelime sınırlarını koruma |
| **🔧 Özel karakterler** | **`.`** → Herhangi bir karakter (newline hariç) <br> **`\d`** → Rakam (`[0-9]`) <br> **`\w`** → Harf, rakam, alt çizgi (`[a-zA-Z0-9_]`) <br> **`\s`** → Boşluk karakteri (space, tab, newline) <br> **`^`** → Satır başı <br> **`$`** → Satır sonu <br> **`*`** → 0 veya daha fazla tekrar <br> **`+`** → 1 veya daha fazla tekrar <br> **`?`** → 0 veya 1 tekrar <br> **`{n}`** → n kadar tekrar <br> **`[abc]`** → a, b veya c karakterlerinden biri <br> **`(abc)`** → Gruplama |
| **📚 Benzer terimler** | Pattern matching, String searching, Text processing, re module (Python), sed, grep, awk |

---

### 📌 Noise Quota
*Gürültü Kotası*

| | |
| :--- | :--- |
| **🗓️ Ne zaman?** | 19.02.2026 |
| **📍 Nerede?** | STEP 3 - Gürültü Ekleme, Veri Hazırlama |
| **❓ Ne işe yarar?** | Gürültü ekleme sürecinde her hata tipi için hedeflenen cümle sayısını ifade eder. Toplam gürültülü cümle sayısının, hata tiplerinin ağırlıklarına göre dağıtılmasını sağlar. |
| **💡 Basit örnek** | Toplam 1000 cümleye %35 gürültü eklenecek (350 cümle). <br> Hata tiplerinin ağırlıkları: <br> • deascii: %30 → quota = 105 cümle <br> • omission: %12 → quota = 42 cümle <br> • insertion: %8 → quota = 28 cümle <br> • transposition: %10 → quota = 35 cümle <br> • substitution: %15 → quota = 52 cümle <br> • space: %5 → quota = 17 cümle <br> • terminology: %8 → quota = 28 cümle <br> • common: %12 → quota = 42 cümle |
| **🧠 Neden gerekli?** | • Her hata tipinden yeterli sayıda örnek olmasını garanti eder. <br> • Rastgele seçimde bazı hata tipleri hiç temsil edilmeyebilir. <br> • Dengeli ve çeşitli bir veri seti oluşturmayı sağlar. |
| **📚 Benzer terimler** | Noise ratio, Error distribution, Sampling quota, Stratified sampling, Class balance |

---

## 📊 ÖZET TABLOSU

| Terim                                         | Kısaltma   | Öğrenme Tarihi |
|:----------------------------------------------|:-----------|:---------------|
| De-asciification                              | -          | 11.02.2026     |
| Out-of-Vocabulary                             | **OOV**    | 11.02.2026     |
| Entity Normalization                          | -          | 11.02.2026     |
| Named Entity Recognition                      | **NER**    | 11.02.2026     |
| Context-Aware Spelling Correction             | -          | 11.02.2026     |
| Noisy Text Normalization                      | -          | 11.02.2026     |
| BERT                                          | -          | 12.02.2026     |
| GECToR                                        | -          | 12.02.2026     |
| Transformer                                   | -          | 12.02.2026     |
| Fine-tuning                                   | -          | 12.02.2026     |
| OCR                                           | -          | 12.02.2026     |
| Multi-Head Attention                          | -          | 17.02.2026     |
| Positional Encoding                           | -          | 17.02.2026     |
| Masked Language Model                         | **MLM**    | 17.02.2026     |
| Next Sentence Prediction                      | **NSP**    | 17.02.2026     |
| Embeddings from Language Models               | **ELMo**   | 17.02.2026     |
| Dynamic Masking                               | -          | 17.02.2026     |
| Multi-Task Fine-Tuning                        | -          | 17.02.2026     |
| Damerau–Levenshtein Distance                  | **DLD**    | 17.02.2026     |
| String-to-String                              | **S2S**    | 17.02.2026     |
| Soft-Masked BERT                              | -          | 17.02.2026     |
| C2C (Character-to-Character)                  | **C2C**    | 17.02.2026     |
| Bidirectional and Auto-Regressive Transformer | **BART**   | 18.02.2026     |
| Automatic Speech Recognition                  | **ASR**    | 18.02.2026     |
| Word Error Rate                               | **WER**    | 18.02.2026     |
| Heavy Encoder                                 | -          | 18.02.2026     |
| CANINE                                        | **CANINE** | 18.02.2026     |
| Entity Linking                                | **EL**     | 18.02.2026     |
| Mention Detection                             | **MD**     | 18.02.2026     |
| Entity Disambiguation                         | **ED**     | 18.02.2026     |
| Natural Language Toolkit                      | **NLTK**   | 18.02.2026     |
| Tokenization                                  | -          | 18.02.2026     |
| BeautifulSoup                                 | **BS4**    | 18.02.2026     |
| Rate Limiting                                 | -          | 18.02.2026     |
| Metadata                                      | -          | 18.02.2026     |
| JSON                                          | **JSON**   | 18.02.2026     |
| Regular Expressions                           | **Regex**  | 19.02.2026     |
| Noise Quota                                   | -          | 19.02.2026     |

---

## 📌 DEĞİŞİKLİK KAYITLARI

| Tarih | Versiyon | Eklenen Terimler                                              | Açıklama                                                                    |
| :--- |:---------|:--------------------------------------------------------------|:----------------------------------------------------------------------------|
| 11.02.2026 | v1.0     | OOV, NER, Entity Norm, Spelling, Noisy Text, De-asciification | İlk oluşturma                                                               |
| 12.02.2026 | v1.1     | BERT, GECToR, Transformer, Fine-tuning, OCR                   | Literatür taraması eklendi                                                  |
| 17.02.2026 | v1.2     | Multi-Head Attention, Positional Encoding                     | Transformer detaylandırıldı                                                 |
| 17.02.2026 | v1.3     | MLM, NSP, Dynamic Masking                                     | BERT eğitim yöntemi eklendi                                                 |
| 17.02.2026 | v1.4     | ELMo                                                          | Bağlamsal embedding modeli eklendi                                          |
| 17.02.2026 | v1.5     | Multi-Task Fine-Tuning                                        | Çok görevli eğitim yöntemi eklendi                                          |
| 17.02.2026 | v1.6     | Damerau–Levenshtein Distance                                  | Edit distance metriği eklendi                                               |
| 17.02.2026 | v1.7     | String-to-String                                              | Metin dönüşüm terimi eklendi                                                |
| 17.02.2026 | v1.8     | Soft-Masked BERT                                              | Yazım düzeltme modeli eklendi                                               |
| 17.02.2026 | v1.9     | C2C (Character-to-Character)                                  | Karakter seviyesi işleme terimi eklendi                                     |
| 18.02.2026 | v2.0     | BART, ASR, WER                                                | Metin üretim modeli, konuşma tanıma ve hata metriği eklendi                 |
| 18.02.2026 | v2.1     | Heavy Encoder                                                 | Büyük ve karmaşık encoder modelleri için kullanılan terim eklendi           |
| 18.02.2026 | v2.2     | CANINE                                                        | Tokenization-free karakter seviyesi model eklendi                           |
| 18.02.2026 | v2.3     | Entity Linking                                                | Varlık bağlama terimi eklendi                                               |
| 18.02.2026 | v2.4     | Mention Detection (MD)                                        | Varlık tespiti terimi eklendi                                               |
| 18.02.2026 | v2.5     | Entity Disambiguation (ED)                                    | Varlık anlam belirsizliği giderme terimi eklendi                            |
| 18.02.2026 | v2.6     | NLTK, Tokenization, BS4, Rate Limiting, Metadata, JSON        | STEP 2 - Data Collection kapsamında kullanılan araçlar ve kavramlar eklendi |
| 19.02.2026 | v2.7     | Regular Expressions (Regex)                                   | STEP 2 ve STEP 3'te kullanılan düzenli ifadeler eklendi                     |
| 19.02.2026 | v2.8     | Noise Quota                                                   | Gürültü ekleme kotası terimi eklendi                                        |

---
*Bu belge proje ilerledikçe güncellenecektir.* 🔄
---
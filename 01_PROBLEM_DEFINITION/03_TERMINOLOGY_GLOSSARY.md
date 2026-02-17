# 📚 TERMINOLOGY GLOSSARY
## Entity Normalization & Correction

| **Son Güncelleme** | 12.02.2026 |
| :--- |:-----------|
| **Toplam Terim** | 16         |
| **Hazırlayan** | Büşra Kaya |

---

## 📋 İÇİNDEKİLER

| # | Bölüm | Durum |
| :--- | :--- | :--- |
| 1 | [STEP 1 - PROBLEM TANIMI](#step-1---problem-tanimi) | ✅ |

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

## 📊 ÖZET TABLOSU

| Terim | Kısaltma | Öğrenme Tarihi |
| :--- |:---------| :--- |
| De-asciification | -        | 11.02.2026 |
| Out-of-Vocabulary | **OOV**  | 11.02.2026 |
| Entity Normalization | -        | 11.02.2026 |
| Named Entity Recognition | **NER**  | 11.02.2026 |
| Context-Aware Spelling Correction | -        | 11.02.2026 |
| Noisy Text Normalization | -        | 11.02.2026 |
| BERT | -        | 12.02.2026 |
| GECToR | -        | 12.02.2026 |
| Transformer | -        | 12.02.2026 |
| Fine-tuning | -        | 12.02.2026 |
| OCR | -        | 12.02.2026 |
| Multi-Head Attention | -        | 17.02.2026 |
| Positional Encoding | -        | 17.02.2026 |
| Masked Language Model (MLM) | **MLM**  | 17.02.2026 |
| Next Sentence Prediction (NSP) | **NSP**  | 17.02.2026 |
| Embeddings from Language Models | **ELMo**     | 17.02.2026 |

---

## 📌 DEĞİŞİKLİK KAYITLARI

| Tarih | Versiyon | Eklenen Terimler                                              | Açıklama |
| :--- |:---------|:--------------------------------------------------------------| :--- |
| 11.02.2026 | v1.0     | OOV, NER, Entity Norm, Spelling, Noisy Text, De-asciification | İlk oluşturma |
| 12.02.2026 | v1.1     | BERT, GECToR, Transformer, Fine-tuning, OCR                   | Literatür taraması eklendi |
| 17.02.2026 | v1.2     | Multi-Head Attention, Positional Encoding                     | Transformer detaylandırıldı |
| 17.02.2026 | v1.3     | MLM, NSP                                                      | BERT eğitim yöntemi eklendi |
| 17.02.2026 | v1.4     | ELMo                                                          | Bağlamsal embedding modeli eklendi |
---

*Bu belge proje ilerledikçe güncellenecektir.* 🔄

---
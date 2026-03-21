# NarrativePulse - Scope Freeze (Adim 1)

Bu dokuman final proje kapsamimizi kilitler. Kodlamaya bu cercevenin disina cikmadan devam edilecektir.

## 1) Proje Amaci

`NarrativePulse`, bir veya iki metin dosyasini (`.txt`, `.md`) analiz eden bir Python CLI aracidir.
Arac, yazim stilini ozetleyen metrikler uretir ve iki metin arasinda stil benzerligi hesabi yapar.

## 2) Kesin Ozellikler (MVP)

MVP surumunde su analizler zorunludur:

1. `lexical_diversity`
   - Tanim: `unique_tokens / total_tokens`
2. `sentence_rhythm`
   - Tanim: Cumle uzunluklarinin (token bazinda) degiskenlik skoru.
   - Hesap: `std(sentence_lengths) / mean(sentence_lengths)` (coefficient of variation).
3. `dialogue_ratio`
   - Tanim: Diyalog olarak etiketlenen cumlelerin toplam cumlelere orani.
   - Diyalog kurali (MVP): Cift tirnak (`"..."`) iceren cumleler diyalog kabul edilir.
4. `repetition_hotspots`
   - Tanim: En sik tekrar eden 2-gram ve 3-gram ifadeler.
   - Stopword temizligi uygulanmaz; normalize edilmis tokenlar kullanilir.
5. `style_signature`
   - Tanim: Stil ozet vektoru.
   - Icerik (MVP): `[lexical_diversity, sentence_rhythm, dialogue_ratio, avg_sentence_length]`
6. `style_similarity`
   - Tanim: Iki metnin `style_signature` vektorleri arasinda cosine similarity (0-1 arasi).

## 3) CLI Kapsami

Desteklenecek komutlar:

1. Tek metin analizi:
   - `python -m narrativepulse analyze <file_path> [--top 10]`
2. Iki metin karsilastirma:
   - `python -m narrativepulse compare <file_a> <file_b> [--top 10]`

Davranis:

1. Cikti terminale okunur bir rapor olarak yazilacak.
2. `--top` argumani repetition listesinde gosterilecek satir sayisini belirleyecek.
3. Dosya okunamazsa net hata mesaji verilecek.

## 4) Girdi/Tokenizasyon Kurallari

1. Girdi dosya formati: UTF-8 `.txt` ve `.md`.
2. Tokenizasyon:
   - Kelime: harf/rakam apostrof icerebilen tokenlar.
   - Cumle: `.`, `!`, `?` ayraclari ile bolme.
3. Normalizasyon:
   - Kucuk harfe cevirme.
   - Basit noktalama temizligi.
4. Bos veya asiri kisa metinlerde metrikler icin guvenli fallback degerleri donulecek (0.0 gibi).

## 5) Kapsam Disi (Bu projede yok)

1. Derin NLP modelleri (BERT, embedding API, LLM).
2. Dil tespiti veya cok dilli gramer analizi.
3. Web arayuzu.
4. Veritabani ve kalici saklama katmani.
5. Agir optimizasyon veya buyuk veri pipeline'i.

## 6) Test Kriterleri

MVP kabul icin asgari testler:

1. Parser/tokenizer birim testleri.
2. Her metrik icin en az bir unit test.
3. `analyze` ve `compare` komutlari icin CLI smoke test.
4. Bos metin ve tek cumleli metin edge-case testleri.

## 7) Paketleme ve Teslim Kriterleri

1. Python `>=3.10`.
2. `pyproject.toml` ile install edilebilir paket.
3. `python -m narrativepulse ...` calisabilir olmali.
4. README icinde:
   - Kurulum
   - Kullanma ornekleri
   - Ornek cikti
   - Proje amaci

## 8) Git Commit Yol Haritasi

1. `Initial package scaffold for NarrativePulse`
2. `Add text parser and normalization layer`
3. `Implement core style metrics`
4. `Add document comparison and similarity scoring`
5. `Add CLI report formatting`
6. `Add tests and README examples`

Bu dokuman, `Adim 1`in resmi ciktisidir.

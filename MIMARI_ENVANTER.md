# Environment Kurulumu ve Mimari Tasarım Envanteri

## 1. Proje Tanımı

**Proje:** Rentèè Akıllı Satış Asistanı  
**Amaç:** Ziyaretçinin moda kiralama sorularını yanıtlamak, ilgili kullanıcının iletişim bilgisini toplamak ve işletme panelinde listelemek.  
**Teknolojiler:** Python 3.9+, Flask, SQLite, Groq API, HTML/CSS/JavaScript, Wix Velo, GitHub, Render.

## 2. Environment Envanteri

| Araç | Görevi | Kontrol komutu |
|---|---|---|
| Python 3.9+ | Backend kodunu çalıştırır | `python3 --version` |
| venv | Proje bağımlılıklarını izole eder | `python3 -m venv venv` |
| pip | Kütüphaneleri kurar | `pip install -r requirements.txt` |
| Git | Sürüm takibi yapar | `git --version` |
| VS Code | Kod düzenleme ortamıdır | Uygulamayı açma |
| GitHub | Kod deposunu barındırır | Repo bağlantısı |
| Render | Backend'i canlıya alır | `/health` kontrolü |
| Wix Velo | Web arayüzünü REST API'ye bağlar | Yayınlanan sayfada test |
| Groq | Yapay zekâ yanıtı üretir | `/api/sohbet` testi |

## 3. Python Bağımlılıkları

| Paket | Neden kullanılıyor? |
|---|---|
| Flask | Web sunucusu ve rotalar |
| Flask-Cors | Wix ile farklı alan adından güvenli bağlantı |
| requests | Groq API'ye HTTP isteği |
| python-dotenv | `.env` ayarlarını okuma |
| gunicorn | Render üretim sunucusu |

## 4. Katmanlar ve Sorumluluklar

| Dosya | Tek sorumluluk |
|---|---|
| `config.py` | Ayarlar ve ortam değişkenleri |
| `app/database.py` | SQLite sorguları ve lead işlemleri |
| `app/services/ai_service.py` | Groq bağlantısı ve AI yanıtı |
| `app/routes.py` | HTTP isteğini doğrulama ve doğru katmana yönlendirme |
| `app/__init__.py` | Uygulama fabrikası, CORS, veritabanı ve blueprint birleştirme |
| `run.py` | Sunucuyu başlatma |
| `templates/index.html` | B2C karşılama arayüzü |
| `templates/dashboard.html` | B2B yönetim arayüzü |

## 5. Veri Akışı

1. Ziyaretçi Wix'te mesajını yazar.
2. Wix Velo, `POST /api/sohbet` adresine JSON gönderir.
3. `routes.py` mesajı doğrular ve `ai_service.py` katmanını çağırır.
4. AI servisi Groq'tan yanıt alır ve JSON olarak arayüze döndürür.
5. Ziyaretçi formu doldurunca `POST /api/leads` çağrılır.
6. `routes.py`, `database.py` içindeki `lead_ekle()` fonksiyonunu çağırır.
7. Yönetim paneli `GET /api/leads` ile kayıtları listeler.

## 6. Güvenlik ve Hata Yönetimi

- API anahtarı kodda değil `.env` dosyasındadır.
- `.env`, `.gitignore` içinde olduğu için GitHub'a gönderilmez.
- SQL Injection'a karşı `?` parametreleri kullanılır.
- Groq ve SQLite işlemleri hata yakalama bloklarıyla korunur.
- Eksik veri `400`, yeni kayıt `201`, AI servis sorunu `503` durum kodu döndürür.
- Render'da CORS yalnızca Wix alan adına sınırlandırılır.

## 7. Doğrulama Kanıtları

- `GET /health` -> `200` ve `{"basari":true,"durum":"aktif"}`
- `POST /api/sohbet` -> `200` ve `cevap` alanı
- Eksik lead -> `400`
- Geçerli lead -> `201`
- `GET /api/leads` -> yeni kaydın listede görünmesi
- Otomatik testler: `python -m unittest discover -s tests -v`

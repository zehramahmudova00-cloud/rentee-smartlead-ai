# Rentèè Akıllı Satış Asistanı

Rentèè'nin ziyaretçilerine kiralık elbise, çanta ve aksesuar konusunda yardımcı olan; ilgilenen kullanıcıların iletişim bilgilerini güvenli biçimde kaydeden Flask tabanlı bir MVP'dir.

## Özellikler

- Groq API ile Türkçe satış asistanı
- API anahtarı yokken çalışan demo modu
- SQLite üzerinde isim, telefon, mesaj ve ilgi alanı kaydı
- Ziyaretçi karşılama sayfası ve yönetim paneli
- Wix Velo için hazır bağlantı kodları
- Modüler Separation of Concerns mimarisi
- CORS, `.env`, parametreli SQL ve kontrollü hata yanıtları

## Mimari

```text
rentee_smartlead/
├── run.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── render.yaml
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── routes.py
│   ├── services/ai_service.py
│   └── templates/
│       ├── index.html
│       └── dashboard.html
├── tests/test_app.py
└── wix_velo/
    ├── karsilama_sayfasi.js
    └── yonetim_paneli.js
```

## Bilgisayarda Çalıştırma

Mac Terminal'de proje klasöründe sırasıyla:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Tarayıcı adresleri:

- Karşılama: `http://localhost:5000`
- Yönetim paneli: `http://localhost:5000/dashboard`
- Sağlık kontrolü: `http://localhost:5000/health`

Canlı yapay zekâ için `.env` içindeki `GROQ_API_KEY` değerini kendi Groq anahtarınızla değiştirin. `.env` dosyasını GitHub'a yüklemeyin.

## Test

```bash
python -m unittest discover -s tests -v
```

## API Özeti

| Metot | Adres | Görev |
|---|---|---|
| GET | `/health` | Sunucunun açık olduğunu gösterir |
| POST | `/api/sohbet` | Kullanıcı mesajını asistana iletir |
| POST | `/api/leads` | Yeni lead kaydeder |
| GET | `/api/leads` | Lead listesini getirir |

Sohbet örneği:

```json
{"mesaj":"Mezuniyet için elbise arıyorum.","gecmis":[]}
```

Lead örneği:

```json
{"isim":"Zehra","telefon":"05550000000","mesaj":"Uzun elbise arıyorum.","ilgi_alani":"Abiye"}
```

## Render Yayını

1. Projeyi GitHub'da public bir depoya yükleyin; `.env` görünmediğini kontrol edin.
2. Render'da **New > Web Service** seçip depoyu bağlayın.
3. Build komutu: `pip install -r requirements.txt`
4. Start komutu: `gunicorn run:app`
5. Environment bölümüne `GROQ_API_KEY`, `SECRET_KEY` ve Wix adresinizi içeren `CORS_ORIGINS` ekleyin.
6. Canlı adreste `/health` açıp `aktif` yanıtını kontrol edin.
7. `wix_velo` dosyalarındaki `API` adresini Render adresinizle değiştirin.

## Güvenlik Notları

- Gizli anahtar `.env` içinde tutulur ve `.gitignore` ile Git dışında bırakılır.
- SQL sorgularında kullanıcı verisi `?` yer tutucularıyla gönderilir.
- CORS yalnızca izin verilen arayüz adreslerine göre ayarlanabilir.
- Kullanıcıya teknik hata ayrıntısı yerine güvenli ve anlaşılır mesaj gösterilir.

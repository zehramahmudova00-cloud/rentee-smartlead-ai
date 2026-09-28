# Rentèè Akıllı Satış Asistanı

Rentèè sitesindeki müşterilerle Türkçe sohbet eden ve ilgilenen kişilerin iletişim bilgilerini kaydeden Flask uygulaması. Groq anahtarı tanımlanmadığında örnek yanıtlarla demo modunda çalışır.

## Çalıştırma

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Canlı yapay zekâ için `.env` dosyasına kendi `GROQ_API_KEY` değerinizi ekleyin. `.env` dosyasını GitHub'a yüklemeyin. `python -m unittest discover -s tests -v` komutu testleri çalıştırır.

## Canlı bağlantılar

- Backend: https://rentee-smartlead-ai.onrender.com
- Sağlık: https://rentee-smartlead-ai.onrender.com/health
- Wix: https://renteestore.wixstudio.com/my-site-2

## Yapı

`app/routes.py` sohbet, lead ve sağlık API'lerini; `app/services/ai_service.py` yanıtları; `app/database.py` SQLite kayıtlarını yönetir. Wix için sayfa kodları, HTML bileşenleri ve yöneticiye özel web modülü `wix_velo/` klasöründedir. Render ayarları `render.yaml` içindedir: build `pip install -r requirements.txt`, start `gunicorn run:app`.

Yönetim listesinin `GET /api/leads` adresi `X-Admin-Token` ister. Render'daki `ADMIN_TOKEN` ile Wix Gizli Anahtar Yöneticisi'ndeki `RENTEE_ADMIN_TOKEN` aynı olmalıdır. Wix web modülü yalnızca site yöneticilerine izin verir. Render'ın ücretsiz örneğinde SQLite dosyası kalıcı disk üzerinde değildir; yeniden dağıtımda lead verileri silinebilir.

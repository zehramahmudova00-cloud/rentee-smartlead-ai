# 3 Dakikalık Demo ve Sunum Metni

Merhaba, projemin adı **Rentèè Akıllı Satış Asistanı**. Rentèè, abiye, çanta ve aksesuarların satın alınması yerine kiralanmasını destekleyen dijital moda platformu fikrimdir. Bu projede ziyaretçinin sorularını yapay zekâ ile yanıtlayan ve ilgilenen kişilerin iletişim bilgilerini kaydeden bir MVP geliştirdim.

Projeyi tek dosyada yazmak yerine sorumlulukların ayrılığı ilkesine göre katmanlara böldüm. `config.py` ayarları ve gizli anahtarları yönetiyor. Bütün SQL işlemleri yalnızca `database.py` içinde. Groq yapay zekâ bağlantısı yalnızca `ai_service.py` içinde. `routes.py` ise HTTP isteklerini kontrol edip doğru katmana yönlendiriyor. Böylece kod daha okunabilir, test edilebilir ve ileride geliştirilebilir oluyor.

Şimdi sağlık kontrolü adresini açıyorum. `aktif` yanıtı backend'in çalıştığını gösteriyor. Karşılama sayfasında kullanıcı moda kiralama hakkında soru sorabiliyor. Canlı anahtar varsa Groq yanıt veriyor; anahtar yoksa uygulama çökmeyip demo modunda çalışıyor. Ardından kullanıcı isim, telefon ve ilgi alanını bırakabiliyor. Bu bilgi SQLite veritabanına güvenli parametreli sorguyla kaydediliyor.

Yönetim panelini açtığımda en yeni lead kayıtlarını isim, telefon, ilgi alanı, mesaj ve tarih ile görebiliyorum. Aynı backend Wix Velo koduyla Rentèè web sitesine bağlanabiliyor. CORS ayarı yalnızca izin verilen arayüzlerin API'ye erişmesini sağlıyor.

Güvenlik için Groq anahtarını `.env` içinde sakladım ve `.gitignore` ile GitHub dışında bıraktım. Hata durumlarında kullanıcıya teknik ayrıntı vermeden anlaşılır JSON yanıtları dönüyorum. Projeyi otomatik testlerle sağlık kontrolü, sohbet, eksik form kontrolü ve lead ekleme-listeleme senaryolarında doğruladım.

Sonuç olarak bu proje, Rentèè'nin satış öncesi iletişimini otomatikleştiren, müşteri adaylarını toplayan ve modüler mimariyle büyümeye hazır çalışan bir prototiptir.

## Muhtemel Sorulara Kısa Cevaplar

**Neden tek bir `app.py` kullanmadın?**  
Her dosyanın tek görevi olsun, hata bulmak ve geliştirmek kolaylaşsın diye.

**Blueprint nedir?**  
Benzer rotaları gruplandıran Flask yapısıdır. Sayfalar ile `/api` rotalarını ayırdım.

**Neden `?` kullandın?**  
Kullanıcı verisini SQL komutundan ayırarak SQL Injection riskini azaltır.

**`.env` neden GitHub'a gitmiyor?**  
API anahtarı gizlidir; sızarsa başkaları kullanabilir. Bu yüzden `.gitignore` içindedir.

**201 ve 503 ne demek?**  
201 yeni kayıt başarıyla oluşturuldu; 503 dış yapay zekâ servisi geçici olarak kullanılamıyor demektir.

**Demo modu neden var?**  
API anahtarı eksik olduğunda uygulamanın tamamen çökmesini önler ve arayüz testine devam ettirir.

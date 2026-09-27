# Rentèè Projesini Sıfırdan Anlama Rehberi

Bu rehber, daha önce Python kullanmamış biri için hazırlanmıştır. Amaç kodu ezberlemek değil, her parçanın neden var olduğunu anlayabilmektir.

## 1. Proje Aslında Ne Yapıyor?

Projede üç temel işlem var:

1. Kullanıcı asistana bir mesaj gönderiyor.
2. Asistan Groq üzerinden yanıt üretiyor.
3. Kullanıcı isim ve telefon bırakınca bilgiler SQLite veritabanına kaydediliyor.

Wix gördüğümüz vitrindir. Flask arka taraftaki motordur. API ise vitrin ile motor arasında mesaj taşıyan köprüdür.

## 2. En Temel Python İşaretleri

```python
isim = "Zehra"
```

`=` sağdaki değeri soldaki isimle saklar. Buna değişken denir.

```python
def lead_ekle(isim, telefon):
    return "kaydedildi"
```

`def` bir fonksiyon tanımlar. Fonksiyon, belirli bir işi yapan tekrar kullanılabilir kod parçasıdır. Parantez içindeki `isim` ve `telefon` fonksiyonun dışarıdan aldığı bilgilerdir. `return` sonucu geri verir.

```python
if not isim:
    return "İsim zorunlu"
```

`if` bir koşulu kontrol eder. `not isim`, isim boşsa doğru kabul edilir. Alt satırın dört boşluk içeride olması o satırın koşula bağlı olduğunu gösterir.

```python
try:
    riskli_islem()
except Hata:
    guvenli_cevap()
```

`try-except`, bir işlem hata verdiğinde uygulamanın kontrolsüz biçimde çökmesini önler.

## 3. Dosyaları Bir Bina Gibi Düşün

### `config.py` - Ayar odası

API anahtarı, veritabanı adresi ve asistanın kişiliği burada tanımlanır. `os.environ.get()` bilgisayarın veya Render'ın ortam değişkenini okur. Değer yoksa ikinci parametredeki güvenli varsayılan kullanılır.

### `database.py` - Arşiv odası

Sadece veritabanı işlemlerini yapar. Başka hiçbir dosyada SQL yoktur. `?` işaretleri kullanıcı bilgisini SQL komutundan ayırır:

```python
db.execute("INSERT INTO leads (isim) VALUES (?)", (isim,))
```

Bu yaklaşım SQL Injection saldırılarına karşı koruma sağlar.

### `ai_service.py` - Yapay zekâ odası

Groq API adresi, model adı ve gönderilen mesajlar burada bulunur. Mesaj sırası şöyledir:

1. `system`: Asistanın kimliği ve kuralları
2. Eski `user` ve `assistant` mesajları
3. Kullanıcının yeni mesajı

API anahtarı yoksa uygulama hata vermek yerine demo metni döndürür.

### `routes.py` - Resepsiyon

İnternetten gelen isteği alır, eksik bilgi var mı diye bakar ve doğru odaya gönderir. Burada SQL sorgusu veya Groq isteği bulunmaz.

Örneğin:

```python
@api_bp.post("/leads")
```

Bu satır, `/api/leads` adresine POST isteği geldiğinde altındaki fonksiyonun çalışacağını belirtir. POST yeni bilgi göndermek, GET bilgi almak için kullanılır.

### `app/__init__.py` - Bina yöneticisi

`create_app()` bütün parçaları birleştirir: ayarları yükler, CORS'u açar, veritabanını hazırlar ve route gruplarını kaydeder. Buna uygulama fabrikası denir.

### `run.py` - Açma düğmesi

Uygulamayı oluşturur ve sunucuyu başlatır. Render da `gunicorn run:app` komutuyla buradaki `app` nesnesini çalıştırır.

## 4. JSON Nedir?

Frontend ve backend bilgileri JSON biçiminde gönderir:

```json
{
  "isim": "Zehra",
  "telefon": "05550000000"
}
```

Bu yapı Python'daki sözlüğe benzer: solda anahtar, sağda değer vardır. Frontend `isim` gönderirken backend de `isim` beklemelidir. Bir harf farkı bağlantıyı bozar.

## 5. Veritabanındaki Lead Tablosu

| Alan | Anlamı |
|---|---|
| `id` | Her kaydın benzersiz numarası |
| `isim` | Kullanıcının adı |
| `telefon` | İletişim telefonu |
| `mesaj` | Kullanıcının asistana yazdığı ihtiyaç |
| `ilgi_alani` | Elbise, çanta veya aksesuar gibi seçim |
| `tarih` | Kaydın oluşturulma zamanı |

## 6. Blueprint Neden Kullanıldı?

Blueprint, rotaları gruplandırır. Projede:

- `pages_bp`: `/` ve `/dashboard` gibi HTML sayfaları
- `api_bp`: `/api/sohbet` ve `/api/leads` gibi veri adresleri

Bu ayrım büyüyen bir projede düzen sağlar.

## 7. CORS Nedir?

Wix ve Render farklı internet adresleridir. Tarayıcı güvenlik nedeniyle her sitenin başka bir sunucuya istek göndermesine izin vermez. CORS, yalnızca belirlediğimiz Wix adresine bu izni verir. Geliştirme sırasında `*` kullanılabilir; canlı yayında Wix adresi yazılmalıdır.

## 8. Bilgisayarında İlk Çalıştırma

Terminal'i aç, proje klasörüne gir ve komutları sırayla çalıştır:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Komut satırının başında `(venv)` görünmesi sanal ortamın açık olduğunu gösterir. Kapatmak için `deactivate` yazabilirsin.

## 9. Groq Anahtarını Ekleme

1. Groq Console'da API Keys bölümünden yeni anahtar oluştur.
2. `.env` dosyasını aç.
3. `GROQ_API_KEY=` sonrasına `gsk_...` anahtarını yapıştır.
4. Anahtarı kimseye gönderme ve ekran görüntüsünde gösterme.
5. Sunucuyu kapatıp yeniden başlat.

## 10. Test Ne İşe Yarıyor?

```bash
python -m unittest discover -s tests -v
```

Bu komut dört senaryoyu otomatik dener: sağlık kontrolü, demo sohbeti, eksik formun reddedilmesi ve geçerli kaydın eklenip listelenmesi. `OK` görülürse hepsi geçmiştir.

## 11. Eğitmene Canlı Gösterme Sırası

1. GitHub'da klasörleri ve `.gitignore` dosyasını göster.
2. `.env` dosyasının repoda olmadığını göster.
3. Render adresinde `/health` aç.
4. Wix'te asistana bir soru sor.
5. Formdan kendi test kaydını oluştur.
6. Yönetim panelinde kaydın geldiğini göster.
7. `database.py` içinde `?` kullanılan sorguyu göster.
8. `routes.py` içinde SQL olmadığını anlat.

## 12. En Sık Hatalar

**`command not found: python`**  
Mac'te `python` yerine `python3` kullan.

**`ModuleNotFoundError`**  
Sanal ortamı açıp `pip install -r requirements.txt` komutunu tekrar çalıştır.

**Groq 401 hatası**  
API anahtarı yanlış, eksik veya başında/sonunda boşluk vardır.

**Wix bağlantı hatası**  
Velo dosyasındaki Render adresi değiştirilmemiş veya `CORS_ORIGINS` içinde Wix adresi yoktur.

**Render'da veriler yeniden başlatınca siliniyor**  
SQLite dosyası ücretsiz geçici dosya sisteminde kalıcı olmayabilir. Bu MVP ve ders teslimi için yeterlidir; gerçek üründe PostgreSQL kullanılmalıdır.

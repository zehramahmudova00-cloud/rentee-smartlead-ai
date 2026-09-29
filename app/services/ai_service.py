import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisindeki kontrollü hataları temsil eder."""


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.business_context = Config.BUSINESS_CONTEXT
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "openai/gpt-oss-20b"

    def _mesajlari_hazirla(self, mesaj, gecmis):
        hazir_mesajlar = [{"role": "system", "content": self.business_context}]
        for kayit in gecmis[-6:]:
            if not isinstance(kayit, dict):
                continue
            rol = kayit.get("role")
            icerik = str(kayit.get("content", "")).strip()
            if rol in {"user", "assistant"} and icerik:
                hazir_mesajlar.append({"role": rol, "content": icerik})
        hazir_mesajlar.append({"role": "user", "content": mesaj})
        return hazir_mesajlar

    def _groq_istegi(self, mesajlar):
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": mesajlar,
                    "temperature": 0.4,
                    "max_tokens": 350,
                },
                timeout=20,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except (requests.RequestException, KeyError, IndexError, TypeError) as error:
            raise AIServiceError("Groq yanıtı alınamadı.") from error

    def yanit_uret(self, mesaj, gecmis=None):
        """Groq kullanılamazsa soruya uygun güvenli demo yanıtı üretir."""
        if not self.api_key:
            return self._demo_yaniti(mesaj)
        mesajlar = self._mesajlari_hazirla(mesaj, gecmis or [])
        try:
            return self._groq_istegi(mesajlar)
        except AIServiceError:
            return self._demo_yaniti(mesaj)

    def _demo_yaniti(self, mesaj):
        metin = mesaj.lower()

        if any(kelime in metin for kelime in ("merhaba", "selam", "günaydın")):
            return (
                "Merhaba! Rentèè stil asistanıyım. Davet türünü, tercih ettiğin "
                "rengi ve bedenini yazarsan sana uygun bir kiralık parça önerebilirim."
            )
        if any(kelime in metin for kelime in ("teslimat", "kargo", "ne zaman")):
            return (
                "Teslimat süresi ürün ve kiralama tarihine göre değişir. Etkinlik "
                "tarihini yazarsan uygun kiralama aralığını birlikte planlayabiliriz."
            )
        if any(kelime in metin for kelime in ("iade", "değişim", "geri gönder")):
            return (
                "Kiraladığın ürünü kullanım süresi sonunda belirtilen iade yöntemiyle "
                "geri gönderebilirsin. Sipariş ve tarih bilgini yazarsan yardımcı olayım."
            )
        if any(kelime in metin for kelime in ("beden", "ölçü", "kaç beden")):
            return (
                "Doğru beden için göğüs, bel ve basen ölçülerini santimetre olarak yaz. "
                "Ürün ölçüleriyle karşılaştırarak en uygun bedeni önerebilirim."
            )
        if any(kelime in metin for kelime in ("mezuniyet", "düğün", "nişan", "davet")):
            return (
                "Etkinliğin için şık bir görünüm hazırlayabiliriz. Renk tercihini, "
                "bedenini ve uzun ya da kısa model istediğini yaz; sana kombin önereyim."
            )
        if any(kelime in metin for kelime in ("bordo", "elbise", "kombin", "saten")):
            return (
                "Bordo bir elbiseyi altın tonlu zarif aksesuarlar, nude ayakkabı ve "
                "sade bir çantayla tamamlayabilirsin. Bedenini yazarsan modeli netleştirelim."
            )
        if any(kelime in metin for kelime in ("fiyat", "ücret", "kiralama", "kirala")):
            return (
                "Rentèè’de fiyat ürün, marka ve kiralama süresine göre belirlenir. "
                "Aradığın ürünü ve kaç gün kiralamak istediğini yazarsan yardımcı olayım."
            )
        return (
            "Sana doğru öneriyi verebilmem için aradığın ürünü, etkinlik türünü, "
            "renk tercihini ve bedenini biraz daha anlatır mısın?"
        )

ai_service = AIService()

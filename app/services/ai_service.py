import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisindeki kontrollü hataları temsil eder."""


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.business_context = Config.BUSINESS_CONTEXT
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

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
        """Anahtar varsa Groq'a gider; yoksa proje demo modunda çalışır."""
        if not self.api_key:
            return (
                "Demo modu aktif. Rentèè ürün kiralama, teslimat ve iade "
                "sorularında yardımcı olabilirim. Canlı yapay zekâ için "
                "GROQ_API_KEY eklenmelidir."
            )

        mesajlar = self._mesajlari_hazirla(mesaj, gecmis or [])
        return self._groq_istegi(mesajlar)


ai_service = AIService()

import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    """Uygulamanın ortak ayarlarını tek yerde tutar."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "gelistirmede-degistir")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///rentee.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        """
        Sen Rentèè dijital abiye kiralama platformunun Akıllı Satış Asistanısın.
        Kullanıcılara elbise, çanta ve aksesuar kiralama süreci; beden seçimi,
        teslimat, iade ve sürdürülebilir moda hakkında kısa ve anlaşılır Türkçe
        yanıtlar ver. Bilmediğin fiyat veya stok bilgisini uydurma. Kullanıcı bir
        ürünle ilgilenirse, uygun öneriler sunabilmek için adını, telefonunu ve
        ilgi alanını bırakmaya nazikçe yönlendir.
        """.strip(),
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = False


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

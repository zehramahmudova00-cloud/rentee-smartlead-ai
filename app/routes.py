import re

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


pages_bp = Blueprint("pages", __name__)
api_bp = Blueprint("api", __name__)


@pages_bp.get("/")
def index():
    return render_template("index.html")


@pages_bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.post("/sohbet")
def sohbet():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "basari": False,
            "hata": "Gönderilen veri bir JSON nesnesi olmalıdır."
        }), 400

    mesaj = str(data.get("mesaj") or "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı zorunludur."
        }), 400

    if not isinstance(gecmis, list):
        return jsonify({
            "basari": False,
            "hata": "Geçmiş liste olmalıdır."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    except AIServiceError:
        return jsonify({
            "basari": False,
            "hata": (
                "Asistan şu anda yanıt veremiyor. "
                "Lütfen tekrar deneyin."
            )
        }), 503


@api_bp.post("/leads")
def lead_olustur():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "basari": False,
            "hata": "Gönderilen veri bir JSON nesnesi olmalıdır."
        }), 400

    isim = str(data.get("isim") or "").strip()
    eposta = str(data.get("eposta") or "").strip()
    telefon = str(data.get("telefon") or "").strip()
    mesaj = str(data.get("mesaj") or "").strip()
    ilgi_alani = str(data.get("ilgi_alani") or "").strip()

    if not isim or not eposta or not telefon:
        return jsonify({
            "basari": False,
            "hata": (
                "İsim, e-posta ve telefon alanları zorunludur."
            )
        }), 400

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", eposta):
        return jsonify({
            "basari": False,
            "hata": "Geçerli bir e-posta adresi girin."
        }), 400

    try:
        lead_id = lead_ekle(
            isim=isim,
            telefon=telefon,
            mesaj=mesaj,
            ilgi_alani=ilgi_alani,
            eposta=eposta,
        )

        return jsonify({
            "basari": True,
            "mesaj": "Bilgileriniz kaydedildi.",
            "id": lead_id
        }), 201

    except RuntimeError:
        return jsonify({
            "basari": False,
            "hata": "Kayıt sırasında bir sorun oluştu."
        }), 500


@api_bp.get("/leads")
def leadleri_listele():
    try:
        yanit = jsonify({
            "basari": True,
            "leadler": tum_leadler()
        })

        yanit.headers["Cache-Control"] = "no-store"
        return yanit

    except RuntimeError:
        return jsonify({
            "basari": False,
            "hata": "Kayıtlar şu anda getirilemiyor."
        }), 500

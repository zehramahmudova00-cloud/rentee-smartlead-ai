from hmac import compare_digest

from flask import Blueprint, current_app, jsonify, render_template, request

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
    data = request.get_json(silent=True) or {}
    mesaj = str(data.get("mesaj", "")).strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alanı zorunludur."}), 400
    if not isinstance(gecmis, list):
        return jsonify({"basari": False, "hata": "Geçmiş liste olmalıdır."}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": cevap})
    except AIServiceError:
        return jsonify(
            {
                "basari": False,
                "hata": "Asistan şu anda yanıt veremiyor. Lütfen tekrar deneyin.",
            }
        ), 503


@api_bp.post("/leads")
def lead_olustur():
    data = request.get_json(silent=True) or {}
    isim = str(data.get("isim", "")).strip()
    telefon = str(data.get("telefon", "")).strip()
    mesaj = str(data.get("mesaj", "")).strip()
    ilgi_alani = str(data.get("ilgi_alani", "")).strip()

    if not isim or not telefon:
        return jsonify(
            {"basari": False, "hata": "İsim ve telefon alanları zorunludur."}
        ), 400

    try:
        lead_id = lead_ekle(isim, telefon, mesaj, ilgi_alani)
        return jsonify(
            {"basari": True, "mesaj": "Bilgileriniz kaydedildi.", "id": lead_id}
        ), 201
    except RuntimeError:
        return jsonify(
            {"basari": False, "hata": "Kayıt sırasında bir sorun oluştu."}
        ), 500


@api_bp.get("/leads")
def leadleri_listele():
    token = current_app.config.get("ADMIN_TOKEN", "")
    supplied = request.headers.get("X-Admin-Token", "")
    if not token or not supplied or not compare_digest(token, supplied):
        return jsonify({"basari": False, "hata": "Erişim reddedildi."}), 403
    try:
        return jsonify({"basari": True, "leadler": tum_leadler()})
    except RuntimeError:
        return jsonify(
            {"basari": False, "hata": "Kayıtlar şu anda getirilemiyor."}
        ), 500

from flask import Flask, jsonify
from flask_cors import CORS

from config import CONFIGS
from app.database import init_db
from app.routes import api_bp, pages_bp


def create_app(config_name="development", test_config=None):
    """Ayarları ve katmanları birleştiren uygulama fabrikası."""
    app = Flask(__name__)
    app.config.from_object(CONFIGS.get(config_name, CONFIGS["development"]))

    if test_config:
        app.config.update(test_config)

    origins = [
        origin.strip()
        for origin in app.config["CORS_ORIGINS"].split(",")
        if origin.strip()
    ]
    CORS(app, resources={r"/api/*": {"origins": origins}})

    with app.app_context():
        init_db(app)

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify({"basari": True, "durum": "aktif"})

    return app

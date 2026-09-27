import sqlite3
from pathlib import Path

from flask import current_app, g


def _database_path():
    """sqlite:/// ile başlayan ayarı gerçek dosya yoluna dönüştürür."""
    database_url = current_app.config["DATABASE_URL"]
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Bu MVP yalnızca sqlite:/// biçimini destekler.")

    raw_path = database_url[len(prefix) :]
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path(current_app.instance_path) / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def get_db():
    """Her istek için bir SQLite bağlantısı açar ve tekrar kullanır."""
    if "db" not in g:
        g.db = sqlite3.connect(_database_path())
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Lead tablosunu yoksa oluşturur ve bağlantı kapanışını kaydeder."""
    app.teardown_appcontext(close_db)
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            ilgi_alani TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


def lead_ekle(isim, telefon, mesaj="", ilgi_alani=""):
    """Kullanıcı verisini güvenli yer tutucularla kaydeder."""
    try:
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO leads (isim, telefon, mesaj, ilgi_alani)
            VALUES (?, ?, ?, ?)
            """,
            (isim, telefon, mesaj, ilgi_alani),
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as error:
        raise RuntimeError("Lead kaydedilemedi.") from error


def tum_leadler():
    """Kayıtları en yeniden en eskiye sözlük listesi olarak döndürür."""
    try:
        rows = get_db().execute(
            """
            SELECT id, isim, telefon, mesaj, ilgi_alani, tarih
            FROM leads
            ORDER BY tarih DESC, id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as error:
        raise RuntimeError("Lead listesi alınamadı.") from error

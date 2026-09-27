import tempfile
import unittest
from pathlib import Path

from app import create_app


class RenteeAppTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "test.db"
        self.app = create_app(
            "testing",
            {
                "DATABASE_URL": f"sqlite:///{db_path}",
                "CORS_ORIGINS": "http://localhost",
            },
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["basari"])

    def test_lead_ekleme_ve_listeleme(self):
        response = self.client.post(
            "/api/leads",
            json={
                "isim": "Zehra",
                "telefon": "05550000000",
                "mesaj": "Mezuniyet elbisesi arıyorum.",
                "ilgi_alani": "Abiye",
            },
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/leads")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["leadler"]), 1)
        self.assertEqual(data["leadler"][0]["isim"], "Zehra")

    def test_eksik_lead_reddedilir(self):
        response = self.client.post("/api/leads", json={"isim": "Zehra"})
        self.assertEqual(response.status_code, 400)

    def test_demo_sohbet(self):
        response = self.client.post("/api/sohbet", json={"mesaj": "Nasıl kiralarım?"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["basari"])


if __name__ == "__main__":
    unittest.main()

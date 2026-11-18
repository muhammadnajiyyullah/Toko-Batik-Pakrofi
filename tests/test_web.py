"""Smoke test untuk website Flask Toko Batik Rofi."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import app as web
except ImportError:  # Flask belum terpasang
    web = None


@unittest.skipUnless(web is not None, "Flask belum terpasang")
class TestWebsite(unittest.TestCase):
    def setUp(self):
        web.toko.reset()
        self.client = web.app.test_client()

    def test_halaman_utama(self):
        respons = self.client.get("/")
        self.assertEqual(respons.status_code, 200)
        self.assertIn(b"Toko Batik Rofi", respons.data)

    def test_api_produk_dan_pelanggan(self):
        respons = self.client.get("/api/produk")
        self.assertEqual(respons.status_code, 200)
        data = respons.get_json()["data"]
        self.assertEqual(len(data), 6)

        respons = self.client.get("/api/pelanggan")
        self.assertEqual(respons.status_code, 200)
        self.assertEqual(len(respons.get_json()["data"]), 3)

    def test_api_tambah_produk(self):
        respons = self.client.post(
            "/api/produk",
            json={
                "jenis": "cap",
                "kode": "BC03",
                "nama": "Batik Cap Sekar",
                "harga_dasar": 150000,
                "stok": 6,
            },
        )
        self.assertEqual(respons.status_code, 201)
        data = respons.get_json()["data"]
        self.assertEqual(data["kode"], "BC03")
        self.assertEqual(data["harga_jual"], 180000)

    def test_api_transaksi(self):
        respons = self.client.post(
            "/api/transaksi",
            json={
                "id_pelanggan": "C001",
                "items": [{"kode": "BT01", "jumlah": 2}],
            },
        )
        self.assertEqual(respons.status_code, 201)
        data = respons.get_json()["data"]
        self.assertEqual(data["transaksi"]["id_transaksi"], "TRX001")
        self.assertIn("TOKO BATIK ROFI", data["struk"])

    def test_api_error_validasi(self):
        respons = self.client.post(
            "/api/produk",
            json={
                "jenis": "tulis",
                "kode": "BT99",
                "nama": "Produk Salah",
                "harga_dasar": 0,
                "stok": 1,
            },
        )
        self.assertEqual(respons.status_code, 400)
        self.assertFalse(respons.get_json()["ok"])

    def test_api_konsol(self):
        respons = self.client.post("/api/console", json={"command": "help"})
        self.assertEqual(respons.status_code, 200)
        baris = respons.get_json()["data"]["lines"]
        self.assertTrue(any("tambah-produk" in item for item in baris))

    def test_api_reset(self):
        self.client.post(
            "/api/transaksi",
            json={
                "id_pelanggan": "C001",
                "items": [{"kode": "BT01", "jumlah": 1}],
            },
        )
        respons = self.client.post("/api/reset", json={})
        self.assertEqual(respons.status_code, 200)
        self.assertEqual(respons.get_json()["data"]["jumlah_transaksi"], 0)


if __name__ == "__main__":
    unittest.main()

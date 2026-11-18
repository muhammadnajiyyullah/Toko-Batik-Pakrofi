"""Unit test untuk class ProdukBatik dan turunannya."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exceptions import (  # noqa: E402
    DataProdukTidakValidError,
    JumlahTidakValidError,
    StokHabisError,
)
from produk_batik import (  # noqa: E402
    BatikCap,
    BatikPrint,
    BatikTulis,
    ProdukBatik,
)


class TestProdukBatik(unittest.TestCase):
    def test_objek_valid_terbentuk(self):
        batik = BatikTulis("BT01", "Parang", 100000, 5)
        self.assertEqual(batik.kode, "BT01")
        self.assertEqual(batik.nama, "Parang")
        self.assertEqual(batik.harga_dasar, 100000)
        self.assertEqual(batik.stok, 5)
        self.assertEqual(batik.jenis, "tulis")

    def test_harga_nol_ditolak(self):
        with self.assertRaises(DataProdukTidakValidError):
            BatikTulis("BT02", "Kawung", 0, 5)

    def test_harga_negatif_ditolak(self):
        with self.assertRaises(DataProdukTidakValidError):
            BatikTulis("BT02", "Kawung", -1000, 5)

    def test_stok_negatif_ditolak(self):
        with self.assertRaises(DataProdukTidakValidError):
            BatikTulis("BT02", "Kawung", 100000, -1)

    def test_kode_kosong_ditolak(self):
        with self.assertRaises(DataProdukTidakValidError):
            BatikTulis("   ", "Kawung", 100000, 5)

    def test_nama_kosong_ditolak(self):
        with self.assertRaises(DataProdukTidakValidError):
            BatikTulis("BT03", "", 100000, 5)

    def test_harga_jual_polymorphism(self):
        tulis = BatikTulis("BT01", "Parang", 100000, 5)
        cap = BatikCap("BC01", "Mega Mendung", 100000, 5)
        cetak = BatikPrint("BP01", "Sogan", 100000, 5)
        dasar = ProdukBatik("PD01", "Dasar", 100000, 5)

        self.assertEqual(tulis.harga_jual(), 150000)
        self.assertEqual(cap.harga_jual(), 120000)
        self.assertEqual(cetak.harga_jual(), 100000)
        self.assertEqual(dasar.harga_jual(), 100000)

    def test_kurangi_stok(self):
        batik = BatikTulis("BT01", "Parang", 100000, 5)
        sisa = batik.kurangi_stok(2)
        self.assertEqual(sisa, 3)
        self.assertEqual(batik.stok, 3)

    def test_stok_tidak_cukup(self):
        batik = BatikTulis("BT01", "Parang", 100000, 2)
        with self.assertRaises(StokHabisError):
            batik.kurangi_stok(3)
        self.assertEqual(batik.stok, 2)

    def test_jumlah_tidak_valid(self):
        batik = BatikTulis("BT01", "Parang", 100000, 5)
        for jumlah in (0, -1, 1.5, True):
            with self.subTest(jumlah=jumlah):
                with self.assertRaises(JumlahTidakValidError):
                    batik.kurangi_stok(jumlah)

    def test_tambah_stok(self):
        batik = BatikTulis("BT01", "Parang", 100000, 5)
        self.assertEqual(batik.tambah_stok(3), 8)

    def test_setter_harga_dan_stok_tervalidasi(self):
        batik = BatikTulis("BT01", "Parang", 100000, 5)
        batik.harga_dasar = 200000
        batik.stok = 10
        self.assertEqual(batik.harga_jual(), 300000)
        self.assertEqual(batik.stok, 10)

        with self.assertRaises(DataProdukTidakValidError):
            batik.harga_dasar = 0
        with self.assertRaises(DataProdukTidakValidError):
            batik.stok = -5


if __name__ == "__main__":
    unittest.main()

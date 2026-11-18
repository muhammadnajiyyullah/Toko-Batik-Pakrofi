"""Unit test untuk class Transaksi."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exceptions import (  # noqa: E402
    JumlahTidakValidError,
    StokHabisError,
    TransaksiTidakValidError,
)
from pelanggan import PelangganMember, PelangganReguler  # noqa: E402
from produk_batik import BatikCap, BatikTulis  # noqa: E402
from transaksi import Transaksi  # noqa: E402


class TestTransaksi(unittest.TestCase):
    def setUp(self):
        self.parang = BatikTulis("BT01", "Parang", 100000, 10)
        self.mega = BatikCap("BC01", "Mega Mendung", 100000, 4)
        self.reguler = PelangganReguler("C001", "Rofi", "081234567890")
        self.member = PelangganMember("C002", "Siti", "081298765432")

    def test_total_tanpa_diskon(self):
        transaksi = Transaksi("TRX001", self.reguler)
        transaksi.tambah_item(self.parang, 2)

        self.assertEqual(transaksi.hitung_subtotal(), 300000)
        self.assertEqual(transaksi.hitung_diskon(), 0)
        self.assertEqual(transaksi.hitung_total(), 300000)

    def test_total_dengan_diskon_member(self):
        transaksi = Transaksi("TRX002", self.member)
        transaksi.tambah_item(self.parang, 2)
        transaksi.tambah_item(self.mega, 1)

        self.assertEqual(transaksi.hitung_subtotal(), 420000)
        self.assertAlmostEqual(transaksi.hitung_diskon(), 42000)
        self.assertAlmostEqual(transaksi.hitung_total(), 378000)

    def test_stok_habis_saat_proses(self):
        transaksi = Transaksi("TRX003", self.reguler)
        transaksi.tambah_item(self.mega, 5)

        with self.assertRaises(StokHabisError):
            transaksi.proses()

        self.assertEqual(self.mega.stok, 4)
        self.assertFalse(transaksi.diproses)

    def test_stok_tidak_berubah_bila_salah_satu_item_gagal(self):
        transaksi = Transaksi("TRX004", self.reguler)
        transaksi.tambah_item(self.parang, 2)
        transaksi.tambah_item(self.mega, 5)

        with self.assertRaises(StokHabisError):
            transaksi.proses()

        self.assertEqual(self.parang.stok, 10)
        self.assertEqual(self.mega.stok, 4)

    def test_duplikat_produk_dijumlahkan_saat_cek_stok(self):
        transaksi = Transaksi("TRX005", self.reguler)
        transaksi.tambah_item(self.mega, 3)
        transaksi.tambah_item(self.mega, 2)

        with self.assertRaises(StokHabisError):
            transaksi.proses()

        self.assertEqual(self.mega.stok, 4)

    def test_duplikat_produk_valid_mengurangi_stok_sekali(self):
        transaksi = Transaksi("TRX006", self.reguler)
        transaksi.tambah_item(self.mega, 2)
        transaksi.tambah_item(self.mega, 1)

        total = transaksi.proses()

        self.assertEqual(total, 360000)
        self.assertEqual(self.mega.stok, 1)
        self.assertTrue(transaksi.diproses)

    def test_jumlah_tidak_valid(self):
        transaksi = Transaksi("TRX007", self.reguler)
        for jumlah in (0, -1, 1.5, True):
            with self.subTest(jumlah=jumlah):
                with self.assertRaises(JumlahTidakValidError):
                    transaksi.tambah_item(self.parang, jumlah)

    def test_transaksi_kosong_tidak_bisa_diproses(self):
        transaksi = Transaksi("TRX008", self.reguler)
        with self.assertRaises(TransaksiTidakValidError):
            transaksi.proses()

    def test_transaksi_tidak_bisa_diproses_dua_kali(self):
        transaksi = Transaksi("TRX009", self.reguler)
        transaksi.tambah_item(self.parang, 1)
        transaksi.proses()

        with self.assertRaises(TransaksiTidakValidError):
            transaksi.proses()
        with self.assertRaises(TransaksiTidakValidError):
            transaksi.tambah_item(self.parang, 1)

    def test_to_dict_berisi_rincian(self):
        transaksi = Transaksi("TRX010", self.member)
        transaksi.tambah_item(self.parang, 2)
        transaksi.proses()

        data = transaksi.to_dict()
        self.assertEqual(data["id_transaksi"], "TRX010")
        self.assertEqual(data["pelanggan"]["jenis"], "member")
        self.assertEqual(data["total_item"], 2)
        self.assertAlmostEqual(data["subtotal"], 300000)
        self.assertAlmostEqual(data["diskon"], 30000)
        self.assertAlmostEqual(data["total"], 270000)
        self.assertEqual(data["item"][0]["kode"], "BT01")


if __name__ == "__main__":
    unittest.main()

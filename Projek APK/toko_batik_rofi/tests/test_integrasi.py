"""Unit test integrasi service TokoBatik dan konsol."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from console import KonsolToko  # noqa: E402
from exceptions import (  # noqa: E402
    DataPelangganTidakValidError,
    DataProdukTidakValidError,
    StokHabisError,
)
from toko import TokoBatik  # noqa: E402


class TestIntegrasiToko(unittest.TestCase):
    def setUp(self):
        self.toko = TokoBatik()
        self.konsol = KonsolToko(self.toko)

    def test_data_demo_awal(self):
        self.assertEqual(len(self.toko.produk_data()), 6)
        self.assertEqual(len(self.toko.pelanggan_data()), 3)
        self.assertEqual(self.toko.dashboard_data()["jumlah_transaksi"], 0)

    def test_tambah_produk_dan_pelanggan(self):
        produk = self.toko.tambah_produk(
            "tulis", "bt03", "Batik Tulis Sido Mukti", 200000, 4
        )
        self.assertEqual(produk.kode, "BT03")
        self.assertEqual(produk.harga_jual(), 300000)

        pelanggan = self.toko.tambah_pelanggan(
            "c004", "Dewi", "081211112222", "member"
        )
        self.assertEqual(pelanggan.id, "C004")
        self.assertEqual(self.toko.cari_pelanggan("C004").nama, "Dewi")

    def test_duplikat_produk_dan_pelanggan_ditolak(self):
        with self.assertRaises(DataProdukTidakValidError):
            self.toko.tambah_produk("cap", "BT01", "Duplikat", 100000, 1)
        with self.assertRaises(DataPelangganTidakValidError):
            self.toko.tambah_pelanggan(
                "C001", "Duplikat", "081234567890", "reguler"
            )

    def test_alur_transaksi_lengkap(self):
        stok_awal = self.toko.cari_produk("BT01").stok
        transaksi = self.toko.buat_transaksi(
            "C001", [("BT01", 2)]
        )

        self.assertEqual(transaksi.id_transaksi, "TRX001")
        self.assertAlmostEqual(transaksi.hitung_total(), 675000)
        self.assertEqual(self.toko.cari_produk("BT01").stok, stok_awal - 2)

        pelanggan, riwayat = self.toko.riwayat_pelanggan("C001")
        self.assertEqual(len(riwayat), 1)
        self.assertEqual(riwayat[0].id_transaksi, "TRX001")

        dashboard = self.toko.dashboard_data()
        self.assertEqual(dashboard["jumlah_transaksi"], 1)
        self.assertAlmostEqual(dashboard["total_pendapatan"], 675000)
        self.assertEqual(dashboard["produk_terlaris"]["kode"], "BT01")

        laporan = self.toko.laporan_data()
        self.assertFalse(laporan["kosong"])
        self.assertIn("TRX001", self.toko.cetak_struk("TRX001"))
        self.assertIn("LAPORAN PENJUALAN", laporan["teks"])

    def test_transaksi_gagal_tidak_mengubah_data(self):
        stok_awal = self.toko.cari_produk("BT02").stok
        with self.assertRaises(StokHabisError):
            self.toko.buat_transaksi("C002", [("BT02", stok_awal + 1)])

        self.assertEqual(self.toko.cari_produk("BT02").stok, stok_awal)
        self.assertEqual(self.toko.dashboard_data()["jumlah_transaksi"], 0)

    def test_reset_mengembalikan_data_demo(self):
        self.toko.buat_transaksi("C001", [("BT01", 1)])
        self.toko.reset()

        self.assertEqual(self.toko.dashboard_data()["jumlah_transaksi"], 0)
        self.assertEqual(self.toko.cari_produk("BT01").stok, 8)
        self.assertEqual(len(self.toko.riwayat_pelanggan("C001")[1]), 0)

    def test_perintah_konsol(self):
        output = self.konsol.jalankan("help")
        self.assertTrue(any("tambah-produk" in baris for baris in output))

        output = self.konsol.jalankan("produk")
        self.assertTrue(any("BT01" in baris for baris in output))

        output = self.konsol.jalankan("beli C002 BP01 2")
        self.assertTrue(any("berhasil diproses" in baris for baris in output))
        self.assertTrue(any("TOKO BATIK ROFI" in baris for baris in output))

        output = self.konsol.jalankan("riwayat C002")
        self.assertTrue(any("TRX001" in baris for baris in output))

        output = self.konsol.jalankan("perintah-tidak-ada")
        self.assertTrue(any("tidak dikenal" in baris for baris in output))

    def test_konsol_menangani_error(self):
        output = self.konsol.jalankan("beli C001 BT01 999")
        self.assertTrue(output[0].startswith("Error:"))


if __name__ == "__main__":
    unittest.main()

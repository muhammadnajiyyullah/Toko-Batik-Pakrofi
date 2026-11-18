"""
=====================================================================
 UNIT TEST — Class Laporan (CLASS UTAMA ANGGOTA D)
 Menjalankan :  python -m unittest test_laporan -v
=====================================================================
 Cakupan pengujian:
   POSITIVE : catat transaksi, rekap produk, total pendapatan,
              produk terlaris, cetak struk & laporan penjualan.
   NEGATIVE : mencatat transaksi belum selesai, laporan kosong,
              nama toko kosong.
=====================================================================
"""

import unittest
from datetime import datetime

from pelanggan import Pelanggan
from produk import ProdukBatik
from transaksi import Transaksi
from laporan import Laporan, LaporanKosongException


class TestLaporanPositive(unittest.TestCase):
    """POSITIVE TEST CASE — kondisi normal / input benar."""

    def setUp(self):
        """Dijalankan sebelum tiap test: pelanggan, produk, laporan."""
        self.pelanggan_1 = Pelanggan("Budi Santoso", "081234567890")
        self.pelanggan_2 = Pelanggan("Siti Aminah", "081298765432")
        self.produk_a = ProdukBatik("Kain Batik Parang", "Parang",
                                     "Kain Batik", "2 meter", 100_000, 20)
        self.produk_b = ProdukBatik("Scarf Batik Sutra", "Kawung",
                                     "Aksesori", "All size", 50_000, 30)
        self.laporan = Laporan("Toko Batik Nusantara")

    def _transaksi_selesai(self, pembeli, daftar_item):
        """Helper: membuat transaksi SELESAI lalu mencatatnya ke laporan."""
        transaksi = Transaksi(
            pembeli,
            tanggal=datetime(2026, 11, 11, 10, 0),  # tanggal tetap utk test
        )
        for produk, jumlah in daftar_item:
            transaksi.tambah_item(produk, jumlah)
        transaksi.proses_transaksi()
        self.laporan.catat_transaksi(transaksi)
        return transaksi

    def test_01_catat_satu_transaksi(self):
        """Transaksi tercatat menambah jumlah_transaksi."""
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 2)])
        self.assertEqual(self.laporan.jumlah_transaksi, 1)

    def test_02_catat_dua_transaksi(self):
        """Beberapa transaksi tercatat berurutan (List riwayat)."""
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 2)])
        self._transaksi_selesai(self.pelanggan_2, [(self.produk_a, 1),
                                                   (self.produk_b, 2)])
        self.assertEqual(self.laporan.jumlah_transaksi, 2)

    def test_03_rekap_produk_terjual(self):
        """Rekap Dict mengagregasi qty per produk lintas transaksi."""
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 2)])
        self._transaksi_selesai(self.pelanggan_2, [(self.produk_a, 1),
                                                   (self.produk_b, 2)])
        rekap = self.laporan.rekap_produk
        self.assertEqual(rekap["Kain Batik Parang"], 3)   # 2 + 1
        self.assertEqual(rekap["Scarf Batik Sutra"], 2)

    def test_04_total_pendapatan(self):
        """total_pendapatan menjumlahkan seluruh transaksi."""
        # Trx 1: 2 x 100.000 ; Trx 2: 1 x 100.000 + 2 x 50.000
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 2)])
        self._transaksi_selesai(self.pelanggan_2, [(self.produk_a, 1),
                                                   (self.produk_b, 2)])
        self.assertEqual(self.laporan.total_pendapatan(), 400_000)

    def test_05_produk_terlaris(self):
        """produk_terlaris mengembalikan (nama, qty) yang paling laku."""
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 2)])
        self._transaksi_selesai(self.pelanggan_2, [(self.produk_b, 1)])
        self.assertEqual(self.laporan.produk_terlaris(),
                         ("Kain Batik Parang", 2))

    def test_06_cetak_struk_memuat_data(self):
        """Struk memuat nama toko, ID, pelanggan, item, dan total."""
        transaksi = self._transaksi_selesai(self.pelanggan_1,
                                            [(self.produk_a, 2)])
        struk = self.laporan.cetak_struk(transaksi)

        self.assertIn("Toko Batik Nusantara", struk)
        self.assertIn(transaksi.id_transaksi, struk)
        self.assertIn("Budi Santoso", struk)
        self.assertIn("Kain Batik Parang", struk)
        self.assertIn("Rp200,000", struk)
        self.assertIn("TOTAL", struk)

    def test_07_cetak_laporan_memuat_data(self):
        """Laporan penjualan memuat rekap & total pendapatan."""
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 2)])
        self._transaksi_selesai(self.pelanggan_2, [(self.produk_b, 3)])
        laporan_teks = self.laporan.cetak_laporan_penjualan()

        self.assertIn("LAPORAN PENJUALAN", laporan_teks)
        self.assertIn("Jumlah transaksi : 2", laporan_teks)
        self.assertIn("Rp350,000", laporan_teks)                 # 200rb + 150rb
        self.assertIn("Kain Batik Parang", laporan_teks)
        self.assertIn("Scarf Batik Sutra", laporan_teks)

    def test_08_rekap_mengembalikan_salinan(self):
        """Dict rekap yang dikembalikan adalah salinan (encapsulation)."""
        self._transaksi_selesai(self.pelanggan_1, [(self.produk_a, 1)])
        salinan = self.laporan.rekap_produk
        salinan["PRODUK SABOTASE"] = 999   # coba ubah salinan
        self.assertNotIn("PRODUK SABOTASE", self.laporan.rekap_produk)


class TestLaporanNegative(unittest.TestCase):
    """NEGATIVE TEST CASE — input salah / memicu Custom Exception."""

    def setUp(self):
        """Dijalankan sebelum tiap test: pelanggan, produk, laporan."""
        self.pelanggan = Pelanggan("Rizky Pratama", "087811223344")
        self.produk = ProdukBatik("Dress Batik Wanita", "Floral",
                                  "Pakaian Jadi", "M", 390_000, 6)
        self.laporan = Laporan("Toko Batik Nusantara")

    def test_09_catat_transaksi_belum_selesai(self):
        """Transaksi berstatus 'BERJALAN' tidak boleh dicatat."""
        transaksi = Transaksi(self.pelanggan)
        transaksi.tambah_item(self.produk, 1)   # status masih BERJALAN
        with self.assertRaises(ValueError):
            self.laporan.catat_transaksi(transaksi)

    def test_10_produk_terlaris_kosong_memicu_exception(self):
        """Belum ada penjualan memicu LaporanKosongException."""
        with self.assertRaises(LaporanKosongException):
            self.laporan.produk_terlaris()

    def test_11_cetak_laporan_kosong_memicu_exception(self):
        """Laporan tanpa transaksi memicu LaporanKosongException."""
        with self.assertRaises(LaporanKosongException):
            self.laporan.cetak_laporan_penjualan()

    def test_12_cetak_struk_transaksi_belum_selesai(self):
        """Struk transaksi 'BERJALAN' memicu ValueError."""
        transaksi = Transaksi(self.pelanggan)
        with self.assertRaises(ValueError):
            self.laporan.cetak_struk(transaksi)

    def test_13_nama_toko_kosong_memicu_valueerror(self):
        """Nama toko kosong memicu ValueError saat membuat laporan."""
        with self.assertRaises(ValueError):
            Laporan("   ")


if __name__ == "__main__":
    unittest.main()

"""
=====================================================================
 UNIT TEST — Class ProdukBatik (CLASS UTAMA ANGGOTA A)
 Menjalankan :  python -m unittest test_produk -v
=====================================================================
 Cakupan pengujian:
   POSITIVE : pembuatan objek valid, getter, setter valid,
              tambah/kurangi stok, tampilkan info.
   NEGATIVE : harga <= 0 / bukan angka, stok < 0, stok kurang,
              jumlah tidak valid, nama kosong, jenis tidak valid.
=====================================================================
"""

import unittest

from produk import (HargaTidakValidException, ProdukBatik,
                    StokTidakValidException)


class TestProdukPositive(unittest.TestCase):
    """POSITIVE TEST CASE — kondisi normal / input benar."""

    def setUp(self):
        """Dijalankan sebelum tiap test: menyiapkan produk valid."""
        self.produk = ProdukBatik(
            nama="Kain Batik Parang", motif="Parang",
            jenis="Kain Batik", ukuran="2 meter",
            harga=350_000, stok=10,
        )

    def test_01_id_produk_berformat_benar(self):
        """ID dibuat otomatis oleh sistem dan berawalan 'BT-'."""
        self.assertTrue(self.produk.id_produk.startswith("BT-"))

    def test_02_getter_nilai_awal_benar(self):
        """Semua nilai awal tersimpan dengan benar melalui getter."""
        self.assertEqual(self.produk.nama, "Kain Batik Parang")
        self.assertEqual(self.produk.motif, "Parang")
        self.assertEqual(self.produk.jenis, "Kain Batik")
        self.assertEqual(self.produk.ukuran, "2 meter")
        self.assertEqual(self.produk.harga, 350_000)
        self.assertEqual(self.produk.stok, 10)

    def test_03_setter_nama_valid(self):
        """Nama produk dapat diganti dengan nilai valid."""
        self.produk.nama = "Kain Batik Mega Mendung"
        self.assertEqual(self.produk.nama, "Kain Batik Mega Mendung")

    def test_04_setter_harga_valid(self):
        """Harga dapat diganti dengan nilai valid dan > 0."""
        self.produk.harga = 500_000
        self.assertEqual(self.produk.harga, 500_000)

    def test_05_setter_stok_valid(self):
        """Stok dapat diganti dengan nilai valid dan >= 0."""
        self.produk.stok = 25
        self.assertEqual(self.produk.stok, 25)

    def test_06_tambah_stok_berhasil(self):
        """tambah_stok menambah stok sesuai jumlah."""
        self.produk.tambah_stok(5)
        self.assertEqual(self.produk.stok, 15)

    def test_07_kurangi_stok_berhasil(self):
        """kurangi_stok mengurangi stok sesuai jumlah."""
        self.produk.kurangi_stok(3)
        self.assertEqual(self.produk.stok, 7)

    def test_08_tampilkan_info_memuat_field_penting(self):
        """tampilkan_info memuat nama, motif, harga, dan stok."""
        info = self.produk.tampilkan_info()
        self.assertIn("Kain Batik Parang", info)
        self.assertIn("Parang", info)
        self.assertIn("Rp350,000", info)
        self.assertIn("Stok: 10", info)

    def test_09_str_mengembalikan_info(self):
        """__str__ mengembalikan ringkasan info produk."""
        self.assertEqual(str(self.produk), self.produk.tampilkan_info())


class TestProdukNegative(unittest.TestCase):
    """NEGATIVE TEST CASE — input salah / memicu Custom Exception."""

    def setUp(self):
        """Dijalankan sebelum tiap test: menyiapkan produk valid."""
        self.produk = ProdukBatik(
            nama="Kemeja Batik Pria", motif="Sogan",
            jenis="Pakaian Jadi", ukuran="L",
            harga=275_000, stok=10,
        )

    def test_10_harga_nol_memicu_exception(self):
        """Harga 0 harus memicu HargaTidakValidException."""
        with self.assertRaises(HargaTidakValidException):
            self.produk.harga = 0

    def test_11_harga_negatif_memicu_exception(self):
        """Harga negatif harus memicu HargaTidakValidException."""
        with self.assertRaises(HargaTidakValidException):
            self.produk.harga = -50_000

    def test_12_harga_bukan_angka_memicu_exception(self):
        """Harga berupa teks harus memicu HargaTidakValidException."""
        with self.assertRaises(HargaTidakValidException):
            self.produk.harga = "mahal"

    def test_13_konstruktor_harga_tidak_valid(self):
        """Konstruktor juga memvalidasi harga melalui setter."""
        with self.assertRaises(HargaTidakValidException):
            ProdukBatik("X", "Parang", "Kain Batik", "2 meter", 0, 5)

    def test_14_stok_negatif_memicu_exception(self):
        """Stok negatif harus memicu StokTidakValidException."""
        with self.assertRaises(StokTidakValidException):
            self.produk.stok = -1

    def test_15_tambah_stok_nol_memicu_exception(self):
        """tambah_stok dengan jumlah 0 harus memicu exception."""
        with self.assertRaises(StokTidakValidException):
            self.produk.tambah_stok(0)

    def test_16_kurangi_stok_melebihi_sisa(self):
        """kurangi_stok melebihi stok tersisa harus memicu exception."""
        with self.assertRaises(StokTidakValidException):
            self.produk.kurangi_stok(99)
        # Pastikan stok TIDAK berubah saat operasi gagal.
        self.assertEqual(self.produk.stok, 10)

    def test_17_kurangi_stok_pesan_menyebut_produk(self):
        """Pesan exception memuat nama produk agar informatif."""
        with self.assertRaises(StokTidakValidException) as konteks:
            self.produk.kurangi_stok(99)
        self.assertIn("Kemeja Batik Pria", str(konteks.exception))

    def test_18_nama_kosong_memicu_valueerror(self):
        """Nama kosong / spasi harus memicu ValueError."""
        with self.assertRaises(ValueError):
            self.produk.nama = "   "

    def test_19_jenis_tidak_dikenal_memicu_valueerror(self):
        """Jenis di luar JENIS_VALID harus memicu ValueError."""
        with self.assertRaises(ValueError):
            self.produk.jenis = "Elektronik"


if __name__ == "__main__":
    unittest.main()

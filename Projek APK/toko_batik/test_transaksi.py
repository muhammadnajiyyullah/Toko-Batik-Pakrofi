"""
=====================================================================
 UNIT TEST — Class Transaksi (CLASS UTAMA ANGGOTA C)
 Menjalankan :  python -m unittest test_transaksi -v
=====================================================================
 Cakupan pengujian:
   POSITIVE : tambah item, penggabungan item sama, hitung total,
              proses transaksi, integrasi dengan class Produk.
   NEGATIVE : stok habis, jumlah item tidak valid, transaksi
              kosong, pelanggan/produk bukan objek valid.
=====================================================================
"""

import unittest
from datetime import datetime

from pelanggan import Pelanggan
from produk import ProdukBatik
from transaksi import (JumlahItemTidakValidException, StokHabisException,
                       Transaksi, TransaksiKosongException)


class TestTransaksiPositive(unittest.TestCase):
    """POSITIVE TEST CASE — kondisi normal / input benar."""

    def setUp(self):
        """Dijalankan sebelum tiap test: pelanggan, produk, transaksi."""
        self.pelanggan = Pelanggan("Budi Santoso", "081234567890")
        self.produk = ProdukBatik("Kain Batik Parang", "Parang",
                                  "Kain Batik", "2 meter", 100_000, 10)
        self.transaksi = Transaksi(
            self.pelanggan,
            tanggal=datetime(2026, 11, 11, 10, 0),  # tanggal tetap utk test
        )

    def test_01_id_transaksi_berformat_benar(self):
        """ID dibuat otomatis dan berawalan 'TRX-'."""
        self.assertTrue(self.transaksi.id_transaksi.startswith("TRX-"))

    def test_02_status_awal_berjalan(self):
        """Transaksi baru berstatus 'BERJALAN'."""
        self.assertEqual(self.transaksi.status, "BERJALAN")

    def test_03_tambah_item_satu_produk(self):
        """tambah_item mengisi keranjang & mengurangi stok produk."""
        self.transaksi.tambah_item(self.produk, 2)

        item = self.transaksi.daftar_item[0]
        self.assertEqual(item["jumlah"], 2)
        self.assertEqual(item["subtotal"], 200_000)
        self.assertEqual(self.transaksi.total_harga, 200_000)
        self.assertEqual(self.produk.stok, 8)   # 10 - 2 (integrasi class Produk)

    def test_04_tambah_item_produk_sama_digabung(self):
        """Produk yang sama ditambah 2x digabung menjadi 1 baris item."""
        self.transaksi.tambah_item(self.produk, 2)
        self.transaksi.tambah_item(self.produk, 3)

        self.assertEqual(len(self.transaksi.daftar_item), 1)      # tetap 1 baris
        self.assertEqual(self.transaksi.daftar_item[0]["jumlah"], 5)
        self.assertEqual(self.transaksi.total_harga, 500_000)
        self.assertEqual(self.produk.stok, 5)                     # 10 - 2 - 3

    def test_05_hitung_total_multi_produk(self):
        """Total menjumlahkan subtotal seluruh jenis produk."""
        produk_lain = ProdukBatik("Scarf Batik", "Kawung",
                                  "Aksesori", "All size", 50_000, 30)
        self.transaksi.tambah_item(self.produk, 2)         # 200_000
        self.transaksi.tambah_item(produk_lain, 3)         # 150_000

        self.assertEqual(self.transaksi.hitung_total(), 350_000)

    def test_06_proses_transaksi_mengembalikan_ringkasan(self):
        """proses_transaksi mengubah status & mengembalikan Dict lengkap."""
        self.transaksi.tambah_item(self.produk, 2)
        ringkasan = self.transaksi.proses_transaksi()

        self.assertEqual(self.transaksi.status, "SELESAI")
        self.assertEqual(ringkasan["id_transaksi"], self.transaksi.id_transaksi)
        self.assertEqual(ringkasan["pelanggan"], "Budi Santoso")
        self.assertEqual(ringkasan["total"], 200_000)
        self.assertEqual(len(ringkasan["item"]), 1)
        self.assertEqual(ringkasan["item"][0]["nama"], "Kain Batik Parang")

    def test_07_str_memuat_info_penting(self):
        """__str__ memuat ID transaksi dan nama pelanggan."""
        teks = str(self.transaksi)
        self.assertIn(self.transaksi.id_transaksi, teks)
        self.assertIn("Budi Santoso", teks)


class TestTransaksiNegative(unittest.TestCase):
    """NEGATIVE TEST CASE — input salah / memicu Custom Exception."""

    def setUp(self):
        """Dijalankan sebelum tiap test: pelanggan, produk, transaksi."""
        self.pelanggan = Pelanggan("Siti Aminah", "081298765432")
        self.produk = ProdukBatik("Kemeja Batik Pria", "Sogan",
                                  "Pakaian Jadi", "L", 275_000, 10)
        self.transaksi = Transaksi(self.pelanggan)

    def test_08_jumlah_nol_memicu_exception(self):
        """Jumlah 0 memicu JumlahItemTidakValidException."""
        with self.assertRaises(JumlahItemTidakValidException):
            self.transaksi.tambah_item(self.produk, 0)

    def test_09_jumlah_negatif_memicu_exception(self):
        """Jumlah negatif memicu JumlahItemTidakValidException."""
        with self.assertRaises(JumlahItemTidakValidException):
            self.transaksi.tambah_item(self.produk, -2)

    def test_10_stok_habis_memicu_exception(self):
        """Permintaan melebihi stok memicu StokHabisException."""
        with self.assertRaises(StokHabisException):
            self.transaksi.tambah_item(self.produk, 11)   # stok hanya 10

    def test_11_stok_habis_tidak_mengurangi_stok(self):
        """Saat gagal, stok produk tidak boleh berubah."""
        try:
            self.transaksi.tambah_item(self.produk, 11)
        except StokHabisException:
            pass
        self.assertEqual(self.produk.stok, 10)
        self.assertEqual(len(self.transaksi.daftar_item), 0)

    def test_12_pesan_stok_habis_informatif(self):
        """Pesan StokHabisException memuat nama produk & angka stok."""
        with self.assertRaises(StokHabisException) as konteks:
            self.transaksi.tambah_item(self.produk, 11)
        pesan = str(konteks.exception)
        self.assertIn("Kemeja Batik Pria", pesan)
        self.assertIn("10", pesan)
        self.assertIn("11", pesan)

    def test_13_atribut_exception_terisi(self):
        """Objek exception menyimpan data pelengkap untuk penelusuran."""
        with self.assertRaises(StokHabisException) as konteks:
            self.transaksi.tambah_item(self.produk, 11)
        self.assertEqual(konteks.exception.nama_produk, "Kemeja Batik Pria")
        self.assertEqual(konteks.exception.stok_tersisa, 10)
        self.assertEqual(konteks.exception.jumlah_diminta, 11)

    def test_14_proses_transaksi_kosong_memicu_exception(self):
        """Finalisasi tanpa item memicu TransaksiKosongException."""
        with self.assertRaises(TransaksiKosongException):
            self.transaksi.proses_transaksi()

    def test_15_konstruktor_pelanggan_tidak_valid(self):
        """Pelanggan bukan objek Pelanggan memicu ValueError."""
        with self.assertRaises(ValueError):
            Transaksi("bukan objek pelanggan")

    def test_16_tambah_item_bukan_objek_produk(self):
        """Item bukan objek ProdukBatik memicu ValueError."""
        with self.assertRaises(ValueError):
            self.transaksi.tambah_item("kain palsu", 2)


if __name__ == "__main__":
    unittest.main()

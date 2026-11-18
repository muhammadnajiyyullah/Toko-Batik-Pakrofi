"""
=====================================================================
 UNIT TEST — Class Pelanggan (CLASS UTAMA ANGGOTA B)
 Menjalankan :  python -m unittest test_pelanggan -v
=====================================================================
 Cakupan pengujian:
   POSITIVE : pembuatan objek valid, getter/setter, tambah
              riwayat belanja, total belanja, cari pelanggan.
   NEGATIVE : no. telepon salah format, pelanggan tidak
              terdaftar, nama kosong, email salah, ringkasan
              transaksi tidak valid.
=====================================================================
"""

import unittest

from pelanggan import (NomorTeleponTidakValidException, Pelanggan,
                       PelangganTidakTerdaftarException)


class TestPelangganPositive(unittest.TestCase):
    """POSITIVE TEST CASE — kondisi normal / input benar."""

    def setUp(self):
        """Dijalankan sebelum tiap test: menyiapkan pelanggan valid."""
        self.pelanggan = Pelanggan("Budi Santoso", "081234567890",
                                   "budi@email.com")
        self.daftar = {"PLG-001": self.pelanggan}
        self.ringkasan = {
            "id_transaksi": "TRX-001",
            "tanggal": "11-11-2026 10:00",
            "total": 500_000,
            "item": [{"nama": "Kain Batik Parang", "jumlah": 1,
                      "subtotal": 500_000}],
        }

    def test_01_id_pelanggan_berformat_benar(self):
        """ID dibuat otomatis dan berawalan 'PLG-'."""
        self.assertTrue(self.pelanggan.id_pelanggan.startswith("PLG-"))

    def test_02_getter_nilai_awal_benar(self):
        """Semua nilai awal tersimpan dengan benar."""
        self.assertEqual(self.pelanggan.nama, "Budi Santoso")
        self.assertEqual(self.pelanggan.no_telepon, "081234567890")
        self.assertEqual(self.pelanggan.email, "budi@email.com")

    def test_03_setter_nama_valid(self):
        """Nama pelanggan dapat diganti dengan nilai valid."""
        self.pelanggan.nama = "Siti Aminah"
        self.assertEqual(self.pelanggan.nama, "Siti Aminah")

    def test_04_setter_telepon_valid(self):
        """No. telepon valid (10-13 digit) dapat diganti."""
        self.pelanggan.no_telepon = "0812987654321"   # 13 digit
        self.assertEqual(self.pelanggan.no_telepon, "0812987654321")

    def test_05_email_opsional_default(self):
        """Email kosong otomatis menjadi '-'."""
        pelanggan = Pelanggan("Rizky", "087811223344")
        self.assertEqual(pelanggan.email, "-")

    def test_06_tambah_riwayat_belanja(self):
        """Riwayat belanja bertambah setelah transaksi dicatat."""
        self.pelanggan.tambah_riwayat(self.ringkasan)
        self.assertEqual(len(self.pelanggan.riwayat_belanja), 1)

    def test_07_total_belanja_dijumlahkan(self):
        """total_belanja menjumlahkan seluruh riwayat."""
        self.pelanggan.tambah_riwayat(self.ringkasan)
        self.pelanggan.tambah_riwayat({"id_transaksi": "TRX-002",
                                       "total": 250_000, "item": []})
        self.assertEqual(self.pelanggan.total_belanja(), 750_000)

    def test_08_tampilkan_riwayat_memuat_id_transaksi(self):
        """String riwayat memuat ID transaksi yang pernah terjadi."""
        self.pelanggan.tambah_riwayat(self.ringkasan)
        self.assertIn("TRX-001", self.pelanggan.tampilkan_riwayat())

    def test_09_tampilkan_riwayat_kosong(self):
        """Pelanggan tanpa transaksi mendapat pesan riwayat kosong."""
        self.assertIn("belum memiliki riwayat",
                      self.pelanggan.tampilkan_riwayat())

    def test_10_cari_pelanggan_ditemukan(self):
        """cari_pelanggan mengembalikan objek yang benar."""
        hasil = Pelanggan.cari_pelanggan(self.daftar, "PLG-001")
        self.assertIs(hasil, self.pelanggan)

    def test_11_cari_pelanggan_huruf_kecil(self):
        """Pencarian tidak sensitif huruf besar/kecil."""
        hasil = Pelanggan.cari_pelanggan(self.daftar, "plg-001")
        self.assertIs(hasil, self.pelanggan)


class TestPelangganNegative(unittest.TestCase):
    """NEGATIVE TEST CASE — input salah / memicu Custom Exception."""

    def setUp(self):
        """Dijalankan sebelum tiap test: menyiapkan pelanggan valid."""
        self.pelanggan = Pelanggan("Budi Santoso", "081234567890")
        self.daftar = {"PLG-001": self.pelanggan}

    def test_12_telepon_terlalu_pendek_memicu_exception(self):
        """No. telepon < 10 digit memicu NomorTeleponTidakValidException."""
        with self.assertRaises(NomorTeleponTidakValidException):
            self.pelanggan.no_telepon = "12345"

    def test_13_telepon_mengandung_huruf_memicu_exception(self):
        """No. telepon non-digit memicu NomorTeleponTidakValidException."""
        with self.assertRaises(NomorTeleponTidakValidException):
            self.pelanggan.no_telepon = "08-abcd-6789"

    def test_14_konstruktor_telepon_tidak_valid(self):
        """Konstruktor juga memvalidasi no. telepon melalui setter."""
        with self.assertRaises(NomorTeleponTidakValidException):
            Pelanggan("Salah Telepon", "08")

    def test_15_nama_kosong_memicu_valueerror(self):
        """Nama kosong / spasi memicu ValueError."""
        with self.assertRaises(ValueError):
            self.pelanggan.nama = "   "

    def test_16_email_tanpa_at_memicu_valueerror(self):
        """Email tanpa '@' memicu ValueError."""
        with self.assertRaises(ValueError):
            self.pelanggan.email = "budi.email.com"

    def test_17_riwayat_bukan_dict_memicu_valueerror(self):
        """Ringkasan transaksi harus berupa dictionary."""
        with self.assertRaises(ValueError):
            self.pelanggan.tambah_riwayat("TRX-001")

    def test_18_riwayat_tanpa_key_wajib_memicu_valueerror(self):
        """Ringkasan tanpa 'id_transaksi'/'total' memicu ValueError."""
        with self.assertRaises(ValueError):
            self.pelanggan.tambah_riwayat({"total": 100_000})

    def test_19_riwayat_total_negatif_memicu_valueerror(self):
        """Total belanja negatif memicu ValueError."""
        with self.assertRaises(ValueError):
            self.pelanggan.tambah_riwayat({"id_transaksi": "TRX-009",
                                           "total": -5_000})

    def test_20_cari_pelanggan_tidak_terdaftar(self):
        """ID tak dikenal memicu PelangganTidakTerdaftarException."""
        with self.assertRaises(PelangganTidakTerdaftarException):
            Pelanggan.cari_pelanggan(self.daftar, "PLG-999")

    def test_21_cari_pelanggan_pesan_memuat_id(self):
        """Pesan exception memuat ID yang dicari (informatif)."""
        with self.assertRaises(PelangganTidakTerdaftarException) as konteks:
            Pelanggan.cari_pelanggan(self.daftar, "PLG-999")
        self.assertIn("PLG-999", str(konteks.exception))


if __name__ == "__main__":
    unittest.main()

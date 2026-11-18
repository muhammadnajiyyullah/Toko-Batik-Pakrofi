"""Unit test untuk class Pelanggan dan turunannya."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exceptions import (  # noqa: E402
    DataPelangganTidakValidError,
    PelangganTidakTerdaftarError,
)
from pelanggan import (  # noqa: E402
    DaftarPelanggan,
    PelangganMember,
    PelangganReguler,
    cari_pelanggan,
)


class DummyTransaksi:
    def __init__(self, id_transaksi):
        self.id_transaksi = id_transaksi


class TestPelanggan(unittest.TestCase):
    def test_diskon_reguler_nol(self):
        pelanggan = PelangganReguler("C001", "Rofi", "081234567890")
        self.assertEqual(pelanggan.diskon(), 0.0)
        self.assertEqual(pelanggan.jenis, "reguler")

    def test_diskon_member_sepuluh_persen(self):
        pelanggan = PelangganMember("C002", "Siti", "081298765432")
        self.assertEqual(pelanggan.diskon(), 0.1)
        self.assertEqual(pelanggan.jenis, "member")

    def test_riwayat_tidak_bisa_diubah_dari_luar(self):
        pelanggan = PelangganMember("C001", "Rofi", "081234567890")
        pelanggan.tambah_riwayat(DummyTransaksi("TRX001"))

        riwayat = pelanggan.riwayat_belanja
        riwayat.append(DummyTransaksi("TRX002"))

        self.assertEqual(len(pelanggan.riwayat_belanja), 1)
        self.assertEqual(pelanggan.lihat_riwayat()[0].id_transaksi, "TRX001")

    def test_tambah_riwayat_invalid(self):
        pelanggan = PelangganReguler("C001", "Rofi", "081234567890")
        with self.assertRaises(DataPelangganTidakValidError):
            pelanggan.tambah_riwayat("bukan transaksi")

    def test_data_pelanggan_tidak_valid(self):
        with self.assertRaises(DataPelangganTidakValidError):
            PelangganReguler("", "Rofi", "081234567890")
        with self.assertRaises(DataPelangganTidakValidError):
            PelangganReguler("C001", "", "081234567890")
        with self.assertRaises(DataPelangganTidakValidError):
            PelangganReguler("C001", "Rofi", "0812")
        with self.assertRaises(DataPelangganTidakValidError):
            PelangganReguler("C001", "Rofi", "08abc4567890")

    def test_daftar_pelanggan_dan_pencarian(self):
        daftar = DaftarPelanggan()
        daftar.tambah(PelangganReguler("c001", "Rofi", "081234567890"))

        pelanggan = daftar.cari_pelanggan("C001")
        self.assertEqual(pelanggan.nama, "Rofi")
        self.assertIn("C001", daftar)
        self.assertEqual(len(daftar), 1)

    def test_id_duplikat_ditolak(self):
        daftar = DaftarPelanggan()
        daftar.tambah(PelangganReguler("C001", "Rofi", "081234567890"))
        with self.assertRaises(DataPelangganTidakValidError):
            daftar.tambah(PelangganMember("C001", "Siti", "081298765432"))

    def test_pelanggan_tidak_terdaftar(self):
        daftar = DaftarPelanggan()
        with self.assertRaises(PelangganTidakTerdaftarError):
            daftar.cari_pelanggan("C999")

    def test_fungsi_cari_pelanggan_dengan_dict(self):
        data = {"C001": PelangganReguler("C001", "Rofi", "081234567890")}
        self.assertEqual(cari_pelanggan(data, "C001").nama, "Rofi")
        with self.assertRaises(PelangganTidakTerdaftarError):
            cari_pelanggan(data, "C999")


if __name__ == "__main__":
    unittest.main()

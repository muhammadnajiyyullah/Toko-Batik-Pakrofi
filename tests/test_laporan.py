"""Unit test untuk class Laporan."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exceptions import (  # noqa: E402
    LaporanKosongError,
    TransaksiTidakValidError,
)
from laporan import Laporan  # noqa: E402
from pelanggan import PelangganMember, PelangganReguler  # noqa: E402
from produk_batik import BatikCap, BatikTulis  # noqa: E402
from transaksi import Transaksi  # noqa: E402


class TestLaporan(unittest.TestCase):
    def setUp(self):
        self.parang = BatikTulis("BT01", "Parang", 100000, 10)
        self.mega = BatikCap("BC01", "Mega Mendung", 100000, 10)
        self.reguler = PelangganReguler("C001", "Rofi", "081234567890")
        self.member = PelangganMember("C002", "Siti", "081298765432")
        self.laporan = Laporan()

    def buat_transaksi(self, id_transaksi, pelanggan, items):
        transaksi = Transaksi(id_transaksi, pelanggan)
        for produk, jumlah in items:
            transaksi.tambah_item(produk, jumlah)
        transaksi.proses()
        return transaksi

    def test_laporan_kosong(self):
        self.assertEqual(self.laporan.total_pendapatan(), 0)
        with self.assertRaises(LaporanKosongError):
            self.laporan.produk_terlaris()
        with self.assertRaises(LaporanKosongError):
            self.laporan.cetak_ringkasan()

    def test_total_pendapatan_dan_rekap(self):
        trx1 = self.buat_transaksi(
            "TRX001", self.reguler, [(self.parang, 2), (self.mega, 1)]
        )
        trx2 = self.buat_transaksi(
            "TRX002", self.member, [(self.parang, 1)]
        )
        self.laporan.tambah_transaksi(trx1)
        self.laporan.tambah_transaksi(trx2)

        self.assertEqual(len(self.laporan.daftar_transaksi), 2)
        self.assertAlmostEqual(self.laporan.total_pendapatan(), 555000)
        self.assertEqual(self.laporan.rekap_produk["BT01"], 3)
        self.assertEqual(self.laporan.rekap_produk["BC01"], 1)

    def test_produk_terlaris(self):
        trx1 = self.buat_transaksi(
            "TRX001", self.reguler, [(self.parang, 2), (self.mega, 1)]
        )
        trx2 = self.buat_transaksi(
            "TRX002", self.member, [(self.parang, 1)]
        )
        self.laporan.tambah_transaksi(trx1)
        self.laporan.tambah_transaksi(trx2)

        terlaris = self.laporan.produk_terlaris()
        self.assertEqual(terlaris["kode"], "BT01")
        self.assertEqual(terlaris["nama"], "Parang")
        self.assertEqual(terlaris["jumlah"], 3)

    def test_rekap_per_pelanggan(self):
        trx1 = self.buat_transaksi(
            "TRX001", self.reguler, [(self.parang, 1)]
        )
        trx2 = self.buat_transaksi(
            "TRX002", self.member, [(self.mega, 1)]
        )
        self.laporan.tambah_transaksi(trx1)
        self.laporan.tambah_transaksi(trx2)

        rekap = self.laporan.rekap_per_pelanggan()
        self.assertEqual(rekap["C001"]["jumlah_transaksi"], 1)
        self.assertAlmostEqual(rekap["C001"]["total_belanja"], 150000)
        self.assertEqual(rekap["C002"]["nama"], "Siti")
        self.assertAlmostEqual(rekap["C002"]["total_belanja"], 108000)

    def test_transaksi_belum_diproses_ditolak(self):
        transaksi = Transaksi("TRX001", self.reguler)
        transaksi.tambah_item(self.parang, 1)
        with self.assertRaises(TransaksiTidakValidError):
            self.laporan.tambah_transaksi(transaksi)

    def test_transaksi_duplikat_ditolak(self):
        transaksi = self.buat_transaksi(
            "TRX001", self.reguler, [(self.parang, 1)]
        )
        self.laporan.tambah_transaksi(transaksi)
        with self.assertRaises(TransaksiTidakValidError):
            self.laporan.tambah_transaksi(transaksi)

    def test_cetak_struk_dan_ringkasan(self):
        transaksi = self.buat_transaksi(
            "TRX001", self.member, [(self.parang, 2)]
        )
        self.laporan.tambah_transaksi(transaksi)

        struk = self.laporan.cetak_struk(transaksi)
        self.assertIn("TOKO BATIK ROFI", struk)
        self.assertIn("TRX001", struk)
        self.assertIn("Parang", struk)
        self.assertIn("Rp300.000", struk)
        self.assertIn("Rp270.000", struk)

        ringkasan = self.laporan.cetak_ringkasan()
        self.assertIn("LAPORAN PENJUALAN", ringkasan)
        self.assertIn("BT01", ringkasan)
        self.assertIn("Siti", ringkasan)


if __name__ == "__main__":
    unittest.main()

"""Kumpulan custom exception untuk aplikasi Toko Batik Rofi.

Semua exception mewarisi TokoBatikError sehingga main.py cukup menangkap
satu tipe exception untuk menangani seluruh kesalahan yang berasal dari
logika toko.
"""


class TokoBatikError(Exception):
    """Induk (base class) semua error di aplikasi Toko Batik Rofi."""


class DataProdukTidakValidError(TokoBatikError):
    """Dilempar ketika data produk tidak memenuhi aturan validasi."""


class DataPelangganTidakValidError(TokoBatikError):
    """Dilempar ketika data pelanggan tidak memenuhi aturan validasi."""


class PelangganTidakTerdaftarError(TokoBatikError):
    """Dilempar ketika pelanggan dengan ID tertentu tidak ditemukan."""


class StokHabisError(TokoBatikError):
    """Dilempar ketika jumlah yang diminta melebihi stok yang tersedia."""


class JumlahTidakValidError(TokoBatikError):
    """Dilempar ketika jumlah item bukan bilangan bulat positif."""


class TransaksiTidakValidError(TokoBatikError):
    """Dilempar ketika transaksi berada pada kondisi yang tidak valid."""


class LaporanKosongError(TokoBatikError):
    """Dilempar ketika laporan diminta tetapi belum ada transaksi."""

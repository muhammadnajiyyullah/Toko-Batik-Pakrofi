"""Class produk batik beserta turunannya (Anggota A).

Menerapkan:
- Encapsulation : atribut private + @property dan setter tervalidasi.
- Inheritance   : BatikTulis, BatikCap, BatikPrint mewarisi ProdukBatik.
- Polymorphism  : harga_jual() di-override oleh setiap subclass.
"""

from exceptions import (
    DataProdukTidakValidError,
    JumlahTidakValidError,
    StokHabisError,
)
from utils import format_rupiah


class ProdukBatik:
    """Produk batik dasar yang menyimpan kode, nama, harga dasar, dan stok."""

    def __init__(self, kode, nama, harga_dasar, stok):
        self.__kode = ""
        self.__nama = ""
        self.__harga_dasar = 0
        self.__stok = 0

        self.__validasi_teks(kode, "Kode produk")
        self.__validasi_teks(nama, "Nama produk")
        self.__kode = kode.strip()
        self.__nama = nama.strip()

        # Setter dipakai agar validasi harga dan stok hanya ditulis sekali.
        self.harga_dasar = harga_dasar
        self.stok = stok

    # ------------------------------------------------------------------
    # Helper validasi internal
    # ------------------------------------------------------------------
    @staticmethod
    def __validasi_teks(nilai, label):
        if not isinstance(nilai, str) or not nilai.strip():
            raise DataProdukTidakValidError(f"{label} tidak boleh kosong.")

    @staticmethod
    def __validasi_angka(nilai, label, minimal, inklusif=True):
        if isinstance(nilai, bool) or not isinstance(nilai, (int, float)):
            raise DataProdukTidakValidError(f"{label} harus berupa angka.")
        if inklusif and nilai < minimal:
            raise DataProdukTidakValidError(
                f"{label} tidak boleh kurang dari {minimal}."
            )
        if not inklusif and nilai <= minimal:
            raise DataProdukTidakValidError(f"{label} harus lebih dari {minimal}.")

    @staticmethod
    def __validasi_jumlah(jumlah):
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise JumlahTidakValidError("Jumlah harus bilangan bulat positif.")

    # ------------------------------------------------------------------
    # Property (read-only)
    # ------------------------------------------------------------------
    @property
    def kode(self):
        return self.__kode

    @property
    def nama(self):
        return self.__nama

    @property
    def jenis(self):
        """Jenis batik berdasarkan nama class, contoh: tulis, cap, print."""
        jenis = type(self).__name__.replace("Batik", "").lower()
        return jenis or "dasar"

    # ------------------------------------------------------------------
    # Property dengan setter tervalidasi
    # ------------------------------------------------------------------
    @property
    def harga_dasar(self):
        return self.__harga_dasar

    @harga_dasar.setter
    def harga_dasar(self, nilai):
        self.__validasi_angka(nilai, "Harga dasar", 0, inklusif=False)
        self.__harga_dasar = nilai

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        self.__validasi_angka(nilai, "Stok", 0)
        self.__stok = int(nilai)

    # ------------------------------------------------------------------
    # Method utama
    # ------------------------------------------------------------------
    def harga_jual(self):
        """Harga jual dasar; subclass meng-override method ini."""
        return self.__harga_dasar

    def kurangi_stok(self, jumlah):
        """Mengurangi stok setelah memastikan jumlahnya mencukupi."""
        self.__validasi_jumlah(jumlah)
        if jumlah > self.__stok:
            raise StokHabisError(
                f"Stok {self.__nama} tidak cukup. "
                f"Diminta {jumlah}, tersedia {self.__stok}."
            )
        self.__stok -= jumlah
        return self.__stok

    def tambah_stok(self, jumlah):
        """Menambah stok produk."""
        self.__validasi_jumlah(jumlah)
        self.__stok += jumlah
        return self.__stok

    def info(self):
        """Mengembalikan ringkasan produk dalam satu baris."""
        return (
            f"[{self.__kode}] {self.__nama} ({type(self).__name__}) | "
            f"Harga jual: {format_rupiah(self.harga_jual())} | "
            f"Stok: {self.__stok}"
        )


class BatikTulis(ProdukBatik):
    """Batik tulis memiliki harga jual 1,5 kali harga dasar."""

    def harga_jual(self):
        return self.harga_dasar * 1.5


class BatikCap(ProdukBatik):
    """Batik cap memiliki harga jual 1,2 kali harga dasar."""

    def harga_jual(self):
        return self.harga_dasar * 1.2


class BatikPrint(ProdukBatik):
    """Batik print dijual sebesar harga dasar (faktor 1,0)."""

    def harga_jual(self):
        return self.harga_dasar * 1.0

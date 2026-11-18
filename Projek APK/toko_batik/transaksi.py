"""
=====================================================================
 TUGAS BESAR PBO  |  SISTEM KASIR TOKO BATIK
 Modul : transaksi.py
 Class : Transaksi  ->  CLASS UTAMA ANGGOTA C
=====================================================================
 Mengelola proses pembelian (peran "kasir"): keranjang belanja,
 perhitungan total, dan finalisasi transaksi.

 Custom Exception (didefinisikan di modul ini):
   1. StokHabisException         -> stok produk habis/tidak
      mencukupi untuk jumlah yang diminta (sesuai ketentuan
      dokumen Tugas Besar).
   2. JumlahItemTidakValidException -> jumlah item <= 0 /
      bukan bilangan bulat.
   3. TransaksiKosongException   -> transaksi difinalisasi tanpa
      memiliki item.

 Collection yang digunakan:
   - List : __daftar_item, keranjang belanja.
            Tiap elemen berupa Dict {produk, jumlah, subtotal}.
   - Dict : struktur tiap item keranjang & ringkasan transaksi.

 Catatan integrasi:
   - MEMANGGIL class Produk (Anggota A): produk.kurangi_stok()
     dan membaca property produk.stok / produk.harga.
   - Menyimpan objek Pelanggan (Anggota B) milik pembeli.
   - Hasil proses_transaksi() diteruskan ke Laporan (Anggota D)
     dan Pelanggan.tambah_riwayat() melalui main.py.
=====================================================================
"""

from datetime import datetime
from typing import Dict, List, Optional

from pelanggan import Pelanggan
from produk import ProdukBatik


class StokHabisException(Exception):
    """Custom Exception: stok produk habis / tidak mencukupi."""

    def __init__(self, nama_produk: str, stok_tersisa: int,
                 jumlah_diminta: int) -> None:
        pesan = (
            f"Stok '{nama_produk}' tidak mencukupi/habis "
            f"(tersisa {stok_tersisa}, diminta {jumlah_diminta})."
        )
        super().__init__(pesan)
        # Data pelengkap disimpan agar mudah ditelusuri saat error.
        self.nama_produk = nama_produk
        self.stok_tersisa = stok_tersisa
        self.jumlah_diminta = jumlah_diminta


class JumlahItemTidakValidException(Exception):
    """Custom Exception: jumlah item tidak valid (<= 0 / bukan angka)."""

    def __init__(self, jumlah) -> None:
        super().__init__(
            f"Jumlah item tidak valid: '{jumlah}'. Harus bilangan bulat > 0."
        )


class TransaksiKosongException(Exception):
    """Custom Exception: transaksi difinalisasi tanpa item."""

    def __init__(self, id_transaksi: str) -> None:
        super().__init__(f"Transaksi {id_transaksi} kosong, tidak memiliki item.")


class Transaksi:
    """
    Class Transaksi — CLASS UTAMA ANGGOTA C.

    Penerapan ENCAPSULATION:
      - Atribut private: id_transaksi, pelanggan, tanggal,
        daftar_item, total_harga, dan status.
      - Getter menyediakan data read-only; daftar_item
        mengembalikan SALINAN list agar isi keranjang tidak bisa
        dimanipulasi dari luar tanpa lewat tambah_item().
      - total_harga hanya dapat berubah melalui method internal
        (tambah_item), tidak melalui setter langsung.

    Penerapan INTEGRASI (memanggil class lain):
      - tambah_item() membaca produk.stok lalu memanggil
        produk.kurangi_stok() milik class ProdukBatik (Anggota A).
    """

    # Atribut class: penghitung transaksi -> ID otomatis TRX-001, ...
    _jumlah_transaksi = 0

    def __init__(self, pelanggan: Pelanggan,
                 tanggal: Optional[datetime] = None) -> None:
        """
        Konstruktor Transaksi.

        Parameter tanggal opsional (dipakai unit test agar hasilnya
        deterministik); jika kosong digunakan waktu saat ini.
        """
        if not isinstance(pelanggan, Pelanggan):
            raise ValueError("Transaksi harus memiliki objek Pelanggan yang valid.")
        Transaksi._jumlah_transaksi += 1

        self.__id_transaksi = f"TRX-{Transaksi._jumlah_transaksi:03d}"
        self.__pelanggan = pelanggan
        self.__tanggal = tanggal if isinstance(tanggal, datetime) else datetime.now()
        # Collection: keranjang belanja berupa List of Dict.
        self.__daftar_item: List[Dict] = []
        self.__total_harga = 0
        self.__status = "BERJALAN"

    # ------------------- GETTER -------------------

    @property
    def id_transaksi(self) -> str:
        """Getter ID transaksi (read-only, otomatis TRX-001, ...)."""
        return self.__id_transaksi

    @property
    def pelanggan(self) -> Pelanggan:
        """Getter objek pelanggan pembeli."""
        return self.__pelanggan

    @property
    def tanggal(self) -> datetime:
        """Getter waktu transaksi dibuat."""
        return self.__tanggal

    @property
    def daftar_item(self) -> List[Dict]:
        """Getter SALINAN keranjang belanja (encapsulation)."""
        return list(self.__daftar_item)

    @property
    def total_harga(self) -> int:
        """Getter total harga seluruh item di keranjang."""
        return self.__total_harga

    @property
    def status(self) -> str:
        """Getter status transaksi ('BERJALAN' atau 'SELESAI')."""
        return self.__status

    # ------------------- METHOD -------------------

    def tambah_item(self, produk: ProdukBatik, jumlah: int) -> None:
        """
        Menambahkan produk ke keranjang belanja.

        Alur:
          1. Validasi objek produk dan jumlah item.
          2. Cek ketersediaan stok -> StokHabisException jika kurang.
          3. Jika produk sudah ada di keranjang, jumlah digabung.
          4. Panggil produk.kurangi_stok() (class Produk, Anggota A).
          5. Perbarui total harga keranjang.
        """
        if not isinstance(produk, ProdukBatik):
            raise ValueError("Item harus berupa objek ProdukBatik.")
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise JumlahItemTidakValidException(jumlah)
        if produk.stok < jumlah:
            raise StokHabisException(produk.nama, produk.stok, jumlah)

        # Cek apakah produk sudah pernah masuk keranjang -> digabung.
        for item in self.__daftar_item:
            if item["produk"].id_produk == produk.id_produk:
                item["jumlah"] += jumlah
                item["subtotal"] = item["jumlah"] * produk.harga
                break
        else:
            # Produk belum ada -> tambah sebagai item baru.
            self.__daftar_item.append({
                "produk": produk,
                "jumlah": jumlah,
                "subtotal": jumlah * produk.harga,
            })

        produk.kurangi_stok(jumlah)                # panggil class Produk (A)
        self.__total_harga = self.hitung_total()   # sinkronkan total

    def hitung_total(self) -> int:
        """Menjumlahkan subtotal seluruh item di keranjang."""
        return sum(item["subtotal"] for item in self.__daftar_item)

    def proses_transaksi(self) -> Dict:
        """
        Memfinalisasi transaksi (pembayaran dianggap berhasil).

        - Mengubah status menjadi 'SELESAI' (transaksi tidak bisa
          diubah lagi).
        - Mengembalikan Dict ringkasan yang dipakai oleh:
          * Laporan.catat_transaksi()   (Anggota D)
          * Pelanggan.tambah_riwayat() (Anggota B)
        """
        if not self.__daftar_item:
            raise TransaksiKosongException(self.__id_transaksi)

        self.__status = "SELESAI"
        return {
            "id_transaksi": self.__id_transaksi,
            "tanggal": self.__tanggal.strftime("%d-%m-%Y %H:%M"),
            "pelanggan": self.__pelanggan.nama,
            "id_pelanggan": self.__pelanggan.id_pelanggan,
            "item": [
                {
                    "nama": i["produk"].nama,
                    "jumlah": i["jumlah"],
                    "subtotal": i["subtotal"],
                }
                for i in self.__daftar_item
            ],
            "total": self.__total_harga,
        }

    def __str__(self) -> str:
        """Representasi ringkas transaksi saat diprint."""
        return (
            f"{self.__id_transaksi} | {self.__pelanggan.nama} | "
            f"{len(self.__daftar_item)} jenis item | "
            f"Rp{self.__total_harga:,} | {self.__status}"
        )

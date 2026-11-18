"""Class transaksi penjualan Toko Batik Rofi (Anggota C).

Menerapkan:
- Komposisi      : Transaksi memiliki objek Pelanggan dan daftar ProdukBatik.
- Custom Exception: StokHabisError, JumlahTidakValidError, TransaksiTidakValidError.
- Collection     : item transaksi disimpan dalam list berisi (produk, jumlah).

Method proses() memeriksa seluruh stok terlebih dahulu, baru kemudian
mengurangi stok. Dengan begitu transaksi yang gagal tidak mengubah data.
"""

from datetime import datetime

from exceptions import (
    JumlahTidakValidError,
    StokHabisError,
    TransaksiTidakValidError,
)
from pelanggan import Pelanggan
from produk_batik import ProdukBatik
from utils import format_rupiah


class Transaksi:
    """Satu transaksi pembelian yang dilakukan seorang pelanggan."""

    def __init__(self, id_transaksi, pelanggan, tanggal=None):
        if not isinstance(id_transaksi, str) or not id_transaksi.strip():
            raise TransaksiTidakValidError("ID transaksi tidak boleh kosong.")
        if not isinstance(pelanggan, Pelanggan):
            raise TransaksiTidakValidError("Pelanggan transaksi tidak valid.")
        if tanggal is not None and not isinstance(tanggal, datetime):
            raise TransaksiTidakValidError("Tanggal transaksi tidak valid.")

        self.__id_transaksi = id_transaksi.strip().upper()
        self.__pelanggan = pelanggan
        self.__item = []
        self.__tanggal = tanggal or datetime.now()
        self.__diproses = False

    # ------------------------------------------------------------------
    # Property read-only
    # ------------------------------------------------------------------
    @property
    def id_transaksi(self):
        return self.__id_transaksi

    @property
    def pelanggan(self):
        return self.__pelanggan

    @property
    def item(self):
        """Salinan daftar item agar tidak bisa diubah dari luar."""
        return list(self.__item)

    @property
    def tanggal(self):
        return self.__tanggal

    @property
    def diproses(self):
        return self.__diproses

    # ------------------------------------------------------------------
    # Method utama
    # ------------------------------------------------------------------
    def tambah_item(self, produk, jumlah):
        """Menambahkan satu produk beserta jumlahnya ke transaksi."""
        if self.__diproses:
            raise TransaksiTidakValidError(
                "Transaksi yang sudah diproses tidak bisa diubah."
            )
        if not isinstance(produk, ProdukBatik):
            raise TransaksiTidakValidError("Produk transaksi tidak valid.")
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise JumlahTidakValidError(
                "Jumlah harus bilangan bulat positif."
            )

        self.__item.append((produk, jumlah))
        return self

    def hitung_subtotal(self):
        """Subtotal = jumlah dari harga_jual() x jumlah tiap item."""
        return sum(produk.harga_jual() * jumlah for produk, jumlah in self.__item)

    def hitung_diskon(self):
        """Diskon dihitung dari persentase milik pelanggan."""
        return self.__pelanggan.diskon() * self.hitung_subtotal()

    def hitung_total(self):
        """Total yang harus dibayar setelah diskon."""
        return self.hitung_subtotal() - self.hitung_diskon()

    def proses(self):
        """Memvalidasi stok seluruh item, lalu mengurangi stok dan mengunci transaksi."""
        if self.__diproses:
            raise TransaksiTidakValidError(
                f"Transaksi {self.__id_transaksi} sudah diproses."
            )
        if not self.__item:
            raise TransaksiTidakValidError(
                "Transaksi belum memiliki item."
            )

        # Gabungkan kebutuhan per kode produk. Ini penting jika produk yang
        # sama ditambahkan lebih dari sekali dalam satu transaksi.
        kebutuhan = {}
        produk_per_kode = {}
        for produk, jumlah in self.__item:
            kebutuhan[produk.kode] = kebutuhan.get(produk.kode, 0) + jumlah
            produk_per_kode[produk.kode] = produk

        # Tahap 1: pastikan semua stok cukup sebelum ada data yang diubah.
        for kode, jumlah in kebutuhan.items():
            produk = produk_per_kode[kode]
            if jumlah > produk.stok:
                raise StokHabisError(
                    f"Stok {produk.nama} tidak cukup. "
                    f"Diminta {jumlah}, tersedia {produk.stok}."
                )

        # Tahap 2: kurangi stok setelah seluruh item dinyatakan aman.
        for kode, jumlah in kebutuhan.items():
            produk_per_kode[kode].kurangi_stok(jumlah)

        self.__diproses = True
        return self.hitung_total()

    def to_dict(self):
        """Representasi transaksi untuk web/API dan laporan."""
        daftar_item = []
        for produk, jumlah in self.__item:
            harga_satuan = produk.harga_jual()
            daftar_item.append(
                {
                    "kode": produk.kode,
                    "nama": produk.nama,
                    "jenis": produk.jenis,
                    "jumlah": jumlah,
                    "harga_satuan": harga_satuan,
                    "subtotal": harga_satuan * jumlah,
                }
            )

        return {
            "id_transaksi": self.__id_transaksi,
            "tanggal": self.__tanggal.strftime("%d-%m-%Y %H:%M"),
            "tanggal_iso": self.__tanggal.isoformat(timespec="minutes"),
            "pelanggan": {
                "id": self.__pelanggan.id,
                "nama": self.__pelanggan.nama,
                "jenis": self.__pelanggan.jenis,
                "diskon": self.__pelanggan.diskon(),
            },
            "item": daftar_item,
            "total_item": sum(jumlah for _, jumlah in self.__item),
            "subtotal": self.hitung_subtotal(),
            "diskon": self.hitung_diskon(),
            "total": self.hitung_total(),
            "diproses": self.__diproses,
        }

    def info(self):
        """Ringkasan transaksi dalam satu baris."""
        return (
            f"[{self.__id_transaksi}] "
            f"{self.__tanggal.strftime('%d-%m-%Y %H:%M')} | "
            f"{self.__pelanggan.id} {self.__pelanggan.nama} | "
            f"{sum(jumlah for _, jumlah in self.__item)} item | "
            f"{format_rupiah(self.hitung_total())}"
        )

"""Lapisan integrasi seluruh class Toko Batik Rofi.

Class TokoBatik menyatukan ProdukBatik, Pelanggan, Transaksi, dan Laporan.
Lapisan ini dipakai oleh main.py (konsol) maupun app.py (website Flask).
"""

from exceptions import (
    DataPelangganTidakValidError,
    DataProdukTidakValidError,
    JumlahTidakValidError,
    LaporanKosongError,
    TokoBatikError,
)
from laporan import Laporan
from pelanggan import (
    DaftarPelanggan,
    PelangganMember,
    PelangganReguler,
)
from produk_batik import BatikCap, BatikPrint, BatikTulis
from transaksi import Transaksi


class TokoBatik:
    """Service utama yang mengoordinasikan seluruh class toko."""

    def __init__(self):
        self.reset()

    # ------------------------------------------------------------------
    # Inisialisasi dan data demo
    # ------------------------------------------------------------------
    def reset(self):
        """Mengembalikan seluruh data ke kondisi data demo awal."""
        self.__produk = {}
        self.__pelanggan = DaftarPelanggan()
        self.__laporan = Laporan()
        self.__counter_transaksi = 0
        self.__isi_data_demo()

    def __isi_data_demo(self):
        produk_demo = [
            ("tulis", "BT01", "Batik Tulis Parang", 250000, 8),
            ("tulis", "BT02", "Batik Tulis Kawung", 300000, 5),
            ("cap", "BC01", "Batik Cap Mega Mendung", 180000, 12),
            ("cap", "BC02", "Batik Cap Truntum", 160000, 10),
            ("print", "BP01", "Batik Print Sogan", 120000, 20),
            ("print", "BP02", "Batik Print Modern", 100000, 25),
        ]
        for jenis, kode, nama, harga, stok in produk_demo:
            self.tambah_produk(jenis, kode, nama, harga, stok)

        pelanggan_demo = [
            ("C001", "Rofi Pratama", "081234567890", "member"),
            ("C002", "Siti Aminah", "081298765432", "reguler"),
            ("C003", "Budi Santoso", "085712345678", "member"),
        ]
        for id_pelanggan, nama, no_hp, tipe in pelanggan_demo:
            self.tambah_pelanggan(id_pelanggan, nama, no_hp, tipe)

    # ------------------------------------------------------------------
    # Property read-only
    # ------------------------------------------------------------------
    @property
    def laporan(self):
        return self.__laporan

    # ------------------------------------------------------------------
    # Produk
    # ------------------------------------------------------------------
    def tambah_produk(self, jenis, kode, nama, harga_dasar, stok):
        peta_jenis = {
            "tulis": BatikTulis,
            "cap": BatikCap,
            "print": BatikPrint,
        }
        jenis_normal = str(jenis).strip().lower()
        if jenis_normal not in peta_jenis:
            raise DataProdukTidakValidError(
                "Jenis produk harus tulis, cap, atau print."
            )

        kode_normal = str(kode).strip().upper()
        if not kode_normal:
            raise DataProdukTidakValidError("Kode produk tidak boleh kosong.")
        if kode_normal in self.__produk:
            raise DataProdukTidakValidError(
                f"Produk dengan kode '{kode_normal}' sudah ada."
            )

        produk = peta_jenis[jenis_normal](kode_normal, nama, harga_dasar, stok)
        self.__produk[kode_normal] = produk
        return produk

    def cari_produk(self, kode):
        kunci = str(kode).strip().upper()
        if kunci not in self.__produk:
            raise DataProdukTidakValidError(
                f"Produk dengan kode '{kode}' tidak ditemukan."
            )
        return self.__produk[kunci]

    def tambah_stok(self, kode, jumlah):
        produk = self.cari_produk(kode)
        produk.tambah_stok(jumlah)
        return produk

    def produk_data(self):
        return [
            self.produk_ke_dict(produk)
            for produk in sorted(self.__produk.values(), key=lambda item: item.kode)
        ]

    @staticmethod
    def produk_ke_dict(produk):
        return {
            "kode": produk.kode,
            "nama": produk.nama,
            "jenis": produk.jenis,
            "harga_dasar": produk.harga_dasar,
            "harga_jual": produk.harga_jual(),
            "stok": produk.stok,
            "stok_menipis": produk.stok <= 5,
        }

    # ------------------------------------------------------------------
    # Pelanggan
    # ------------------------------------------------------------------
    def tambah_pelanggan(self, id_pelanggan, nama, no_hp, tipe="reguler"):
        peta_tipe = {
            "reguler": PelangganReguler,
            "member": PelangganMember,
        }
        tipe_normal = str(tipe).strip().lower()
        if tipe_normal not in peta_tipe:
            raise DataPelangganTidakValidError(
                "Tipe pelanggan harus reguler atau member."
            )

        id_normal = str(id_pelanggan).strip().upper()
        pelanggan = peta_tipe[tipe_normal](id_normal, nama, no_hp)
        self.__pelanggan.tambah(pelanggan)
        return pelanggan

    def cari_pelanggan(self, id_pelanggan):
        return self.__pelanggan.cari_pelanggan(id_pelanggan)

    def pelanggan_data(self):
        rekap = self.__laporan.rekap_per_pelanggan()
        return [
            self.pelanggan_ke_dict(pelanggan, rekap.get(pelanggan.id, {}))
            for pelanggan in sorted(
                self.__pelanggan.semua(), key=lambda item: item.id
            )
        ]

    @staticmethod
    def pelanggan_ke_dict(pelanggan, rekap=None):
        rekap = rekap or {}
        return {
            "id": pelanggan.id,
            "nama": pelanggan.nama,
            "no_hp": pelanggan.no_hp,
            "jenis": pelanggan.jenis,
            "diskon": pelanggan.diskon(),
            "diskon_persen": pelanggan.diskon() * 100,
            "jumlah_transaksi": rekap.get("jumlah_transaksi", 0),
            "total_belanja": rekap.get("total_belanja", 0),
        }

    # ------------------------------------------------------------------
    # Transaksi
    # ------------------------------------------------------------------
    def buat_transaksi(self, id_pelanggan, items):
        """Membuat, memproses, dan mencatat transaksi baru.

        items berupa list/tuple berisi pasangan (kode_produk, jumlah).
        """
        if not isinstance(items, (list, tuple)) or not items:
            raise JumlahTidakValidError(
                "Transaksi minimal memiliki satu item."
            )

        pelanggan = self.cari_pelanggan(id_pelanggan)

        self.__counter_transaksi += 1
        transaksi = Transaksi(
            f"TRX{self.__counter_transaksi:03d}", pelanggan
        )

        for kode, jumlah in items:
            transaksi.tambah_item(self.cari_produk(kode), jumlah)

        transaksi.proses()
        self.__laporan.tambah_transaksi(transaksi)
        pelanggan.tambah_riwayat(transaksi)
        return transaksi

    def cari_transaksi(self, id_transaksi):
        kunci = str(id_transaksi).strip().upper()
        for transaksi in self.__laporan.daftar_transaksi:
            if transaksi.id_transaksi == kunci:
                return transaksi
        raise TokoBatikError(
            f"Transaksi dengan ID '{id_transaksi}' tidak ditemukan."
        )

    def transaksi_data(self):
        return [
            transaksi.to_dict()
            for transaksi in reversed(self.__laporan.daftar_transaksi)
        ]

    def riwayat_pelanggan(self, id_pelanggan):
        pelanggan = self.cari_pelanggan(id_pelanggan)
        return pelanggan, pelanggan.lihat_riwayat()

    def cetak_struk(self, id_transaksi):
        return self.__laporan.cetak_struk(self.cari_transaksi(id_transaksi))

    def cetak_laporan(self):
        return self.__laporan.cetak_ringkasan()

    # ------------------------------------------------------------------
    # Ringkasan untuk dashboard dan website
    # ------------------------------------------------------------------
    def dashboard_data(self):
        transaksi = self.__laporan.daftar_transaksi
        try:
            terlaris = self.__laporan.produk_terlaris()
        except LaporanKosongError:
            terlaris = None

        stok_menipis = [
            data for data in self.produk_data() if data["stok_menipis"]
        ]
        stok_menipis.sort(key=lambda item: (item["stok"], item["kode"]))

        return {
            "jumlah_produk": len(self.__produk),
            "jumlah_pelanggan": len(self.__pelanggan),
            "jumlah_transaksi": len(transaksi),
            "total_pendapatan": self.__laporan.total_pendapatan(),
            "total_item_terjual": sum(
                self.__laporan.rekap_produk.values()
            ),
            "produk_terlaris": terlaris,
            "stok_menipis": stok_menipis[:5],
            "transaksi_terbaru": [
                transaksi.to_dict() for transaksi in transaksi[-5:][::-1]
            ],
        }

    def laporan_data(self):
        transaksi = self.__laporan.daftar_transaksi
        if not transaksi:
            return {
                "kosong": True,
                "jumlah_transaksi": 0,
                "total_pendapatan": 0,
                "total_item": 0,
                "produk_terlaris": None,
                "rekap_produk": [],
                "rekap_pelanggan": [],
                "teks": "Belum ada transaksi. Laporan akan tersedia setelah transaksi pertama diproses.",
            }

        rekap_produk = []
        for kode, jumlah in sorted(
            self.__laporan.rekap_produk.items(),
            key=lambda item: (-item[1], item[0]),
        ):
            produk = self.__produk.get(kode)
            rekap_produk.append(
                {
                    "kode": kode,
                    "nama": produk.nama if produk else kode,
                    "jumlah": jumlah,
                }
            )

        rekap_pelanggan = [
            {"id": id_pelanggan, **data}
            for id_pelanggan, data in sorted(
                self.__laporan.rekap_per_pelanggan().items(),
                key=lambda item: (-item[1]["total_belanja"], item[0]),
            )
        ]

        return {
            "kosong": False,
            "jumlah_transaksi": len(transaksi),
            "total_pendapatan": self.__laporan.total_pendapatan(),
            "total_item": sum(self.__laporan.rekap_produk.values()),
            "produk_terlaris": self.__laporan.produk_terlaris(),
            "rekap_produk": rekap_produk,
            "rekap_pelanggan": rekap_pelanggan,
            "teks": self.__laporan.cetak_ringkasan(),
        }

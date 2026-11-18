"""Class laporan penjualan Toko Batik Rofi (Anggota D).

Menerapkan:
- Collection : list untuk riwayat transaksi, dict untuk rekap produk dan pelanggan.
- Custom Exception: LaporanKosongError saat laporan diminta tanpa data.
"""

from exceptions import (
    LaporanKosongError,
    TransaksiTidakValidError,
)
from transaksi import Transaksi
from utils import format_rupiah


class Laporan:
    """Menyimpan seluruh transaksi dan menyusun rekap penjualan."""

    def __init__(self):
        self.__daftar_transaksi = []
        self.__rekap_produk = {}
        self.__nama_produk = {}
        self.__rekap_pelanggan = {}

    # ------------------------------------------------------------------
    # Property read-only
    # ------------------------------------------------------------------
    @property
    def daftar_transaksi(self):
        return list(self.__daftar_transaksi)

    @property
    def rekap_produk(self):
        return dict(self.__rekap_produk)

    # ------------------------------------------------------------------
    # Method utama
    # ------------------------------------------------------------------
    def tambah_transaksi(self, transaksi):
        """Menambahkan transaksi yang sudah diproses ke laporan."""
        if not isinstance(transaksi, Transaksi):
            raise TransaksiTidakValidError("Objek laporan bukan Transaksi.")
        if not transaksi.diproses:
            raise TransaksiTidakValidError(
                "Transaksi harus diproses sebelum masuk ke laporan."
            )
        if any(
            item.id_transaksi == transaksi.id_transaksi
            for item in self.__daftar_transaksi
        ):
            raise TransaksiTidakValidError(
                f"Transaksi {transaksi.id_transaksi} sudah ada di laporan."
            )

        self.__daftar_transaksi.append(transaksi)

        for item in transaksi.to_dict()["item"]:
            kode = item["kode"]
            self.__rekap_produk[kode] = (
                self.__rekap_produk.get(kode, 0) + item["jumlah"]
            )
            self.__nama_produk[kode] = item["nama"]

        pelanggan = transaksi.pelanggan
        rekap = self.__rekap_pelanggan.setdefault(
            pelanggan.id,
            {
                "nama": pelanggan.nama,
                "jenis": pelanggan.jenis,
                "jumlah_transaksi": 0,
                "total_belanja": 0,
            },
        )
        rekap["jumlah_transaksi"] += 1
        rekap["total_belanja"] += transaksi.hitung_total()

        return transaksi

    def total_pendapatan(self):
        return sum(transaksi.hitung_total() for transaksi in self.__daftar_transaksi)

    def produk_terlaris(self):
        """Mengembalikan produk dengan jumlah terjual paling banyak."""
        if not self.__rekap_produk:
            raise LaporanKosongError(
                "Belum ada transaksi, produk terlaris belum tersedia."
            )

        kode = max(
            self.__rekap_produk,
            key=lambda item: (self.__rekap_produk[item], item),
        )
        return {
            "kode": kode,
            "nama": self.__nama_produk.get(kode, kode),
            "jumlah": self.__rekap_produk[kode],
        }

    def rekap_per_pelanggan(self):
        """Mengembalikan dict rekap belanja per pelanggan."""
        return {
            id_pelanggan: dict(data)
            for id_pelanggan, data in self.__rekap_pelanggan.items()
        }

    def cetak_struk(self, transaksi):
        """Menyusun struk transaksi dalam bentuk teks."""
        if not isinstance(transaksi, Transaksi):
            raise TransaksiTidakValidError("Objek struk bukan Transaksi.")
        if not transaksi.diproses:
            raise TransaksiTidakValidError(
                "Struk hanya bisa dicetak untuk transaksi yang sudah diproses."
            )

        data = transaksi.to_dict()
        lebar = 48
        garis = "=" * lebar
        tipis = "-" * lebar

        baris = [
            garis,
            "TOKO BATIK ROFI".center(lebar),
            "Jl. Batik Indah No. 17, Pekalongan".center(lebar),
            garis,
            f"No. Transaksi : {data['id_transaksi']}",
            f"Tanggal       : {data['tanggal']}",
            f"Pelanggan     : {data['pelanggan']['id']} - "
            f"{data['pelanggan']['nama']} ({data['pelanggan']['jenis']})",
            tipis,
            "ITEM:",
        ]

        for nomor, item in enumerate(data["item"], start=1):
            baris.append(f"{nomor}. {item['nama']} ({item['jenis']})")
            baris.append(
                f"   {item['jumlah']} x {format_rupiah(item['harga_satuan'])}"
                f" = {format_rupiah(item['subtotal'])}"
            )

        persen_diskon = data["pelanggan"]["diskon"] * 100
        baris.extend(
            [
                tipis,
                f"Subtotal      : {format_rupiah(data['subtotal'])}",
                f"Diskon ({persen_diskon:.0f}%)  : -{format_rupiah(data['diskon'])}",
                f"TOTAL         : {format_rupiah(data['total'])}",
                garis,
                "Terima kasih telah berbelanja di Toko Batik Rofi.",
                "Simpan struk ini sebagai bukti pembelian.",
                garis,
            ]
        )
        return "\n".join(baris)

    def cetak_ringkasan(self):
        """Menyusun laporan penjualan keseluruhan dalam bentuk teks."""
        if not self.__daftar_transaksi:
            raise LaporanKosongError(
                "Laporan belum bisa dicetak karena belum ada transaksi."
            )

        lebar = 56
        garis = "=" * lebar
        tipis = "-" * lebar
        terlaris = self.produk_terlaris()
        total_item = sum(self.__rekap_produk.values())

        baris = [
            garis,
            "LAPORAN PENJUALAN".center(lebar),
            "TOKO BATIK ROFI".center(lebar),
            garis,
            f"Jumlah transaksi  : {len(self.__daftar_transaksi)}",
            f"Total item terjual: {total_item}",
            f"Total pendapatan  : {format_rupiah(self.total_pendapatan())}",
            f"Produk terlaris   : {terlaris['kode']} - {terlaris['nama']} "
            f"({terlaris['jumlah']} pcs)",
            tipis,
            "REKAP PER PRODUK",
        ]

        for kode, jumlah in sorted(
            self.__rekap_produk.items(),
            key=lambda item: (-item[1], item[0]),
        ):
            nama = self.__nama_produk.get(kode, kode)
            baris.append(f"{kode:<6} {nama:<28} {jumlah:>4} pcs")

        baris.extend([tipis, "REKAP PER PELANGGAN"])

        for id_pelanggan, data in sorted(
            self.__rekap_pelanggan.items(),
            key=lambda item: (-item[1]["total_belanja"], item[0]),
        ):
            baris.append(
                f"{id_pelanggan:<6} {data['nama']:<22} "
                f"{data['jumlah_transaksi']:>2} trx | "
                f"{format_rupiah(data['total_belanja'])}"
            )

        baris.extend([garis, "Laporan dibuat otomatis oleh sistem.", garis])
        return "\n".join(baris)

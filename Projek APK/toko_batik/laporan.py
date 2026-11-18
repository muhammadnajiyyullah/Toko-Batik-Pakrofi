"""
=====================================================================
 TUGAS BESAR PBO  |  SISTEM KASIR TOKO BATIK
 Modul : laporan.py
 Class : Laporan  ->  CLASS UTAMA ANGGOTA D
=====================================================================
 Mengelola riwayat penjualan toko: pencatatan transaksi, rekap
 produk terjual, pencetakan struk, dan laporan penjualan.

 Custom Exception (didefinisikan di modul ini):
   - LaporanKosongException -> laporan/struk diminta saat data
     masih kosong.

 Collection yang digunakan (sesuai ketentuan dokumen Tugas
 Besar: gunakan List/Dict untuk menyimpan riwayat):
   - List : __riwayat_transaksi -> kumpulan objek Transaksi.
   - Dict : __rekap_produk -> {nama_produk: total_qty_terjual}.

 Catatan integrasi:
   - Menerima objek Transaksi (Anggota C) lewat catat_transaksi().
   - Membaca detail item dari Transaksi.daftar_item (yang berisi
     objek ProdukBatik milik Anggota A).
=====================================================================
"""

from typing import Dict, List, Tuple

from transaksi import Transaksi


class LaporanKosongException(Exception):
    """Custom Exception: operasi laporan dilakukan saat data kosong."""

    def __init__(self, pesan: str) -> None:
        super().__init__(pesan)


class Laporan:
    """
    Class Laporan — CLASS UTAMA ANGGOTA D.

    Penerapan ENCAPSULATION:
      - Atribut private: nama_toko, riwayat_transaksi, rekap_produk.
      - Getter mengembalikan data read-only; rekap_produk
        mengembalikan SALINAN dictionary agar data internal aman.
      - Pengisian data hanya melalui catat_transaksi() yang
        memvalidasi status transaksi terlebih dahulu.

    Penerapan COLLECTION:
      - List  : penyimpanan objek transaksi terurut (riwayat).
      - Dict  : agregasi jumlah produk terjual per nama produk.
    """

    def __init__(self, nama_toko: str = "Toko Batik Nusantara") -> None:
        """Konstruktor Laporan: menyiapkan wadah data penjualan."""
        if not isinstance(nama_toko, str) or not nama_toko.strip():
            raise ValueError("Nama toko tidak boleh kosong.")
        self.__nama_toko = nama_toko.strip()
        # Collection: List untuk riwayat + Dict untuk rekap produk.
        self.__riwayat_transaksi: List[Transaksi] = []
        self.__rekap_produk: Dict[str, int] = {}

    # ------------------- GETTER -------------------

    @property
    def nama_toko(self) -> str:
        """Getter nama toko."""
        return self.__nama_toko

    @property
    def jumlah_transaksi(self) -> int:
        """Getter jumlah transaksi yang sudah tercatat."""
        return len(self.__riwayat_transaksi)

    @property
    def rekap_produk(self) -> Dict[str, int]:
        """Getter SALINAN rekap produk terjual (encapsulation)."""
        return dict(self.__rekap_produk)

    # ------------------- METHOD -------------------

    def catat_transaksi(self, transaksi: Transaksi) -> None:
        """
        Mencatat transaksi yang sudah selesai ke dalam laporan.

        Validasi: hanya transaksi berstatus 'SELESAI' yang boleh
        dicatat. Setelah dicatat, rekap produk terjual diperbarui.
        """
        if getattr(transaksi, "status", None) != "SELESAI":
            raise ValueError(
                "Hanya transaksi berstatus 'SELESAI' yang dapat dicatat ke laporan."
            )
        self.__riwayat_transaksi.append(transaksi)

        # Agregasi jumlah produk terjual ke dalam Dict rekap.
        for item in transaksi.daftar_item:
            nama = item["produk"].nama
            self.__rekap_produk[nama] = self.__rekap_produk.get(nama, 0) + item["jumlah"]

    def total_pendapatan(self) -> int:
        """Menjumlahkan total harga seluruh transaksi tercatat."""
        return sum(t.total_harga for t in self.__riwayat_transaksi)

    def produk_terlaris(self) -> Tuple[str, int]:
        """
        Mengembalikan (nama_produk, total_terjual) terlaris.

        Melempar LaporanKosongException jika belum ada penjualan.
        """
        if not self.__rekap_produk:
            raise LaporanKosongException(
                "Belum ada produk terjual sehingga produk terlaris tidak dapat ditentukan."
            )
        nama_terlaris = max(self.__rekap_produk, key=self.__rekap_produk.get)
        return nama_terlaris, self.__rekap_produk[nama_terlaris]

    def cetak_struk(self, transaksi: Transaksi) -> str:
        """
        Menyusun struk pembelian (teks) dari sebuah transaksi.

        Struk memuat nama toko, nomor struk, pelanggan, daftar item,
        dan total pembayaran. Melempar ValueError jika transaksi
        belum berstatus 'SELESAI'.
        """
        if getattr(transaksi, "status", None) != "SELESAI":
            raise ValueError("Struk hanya bisa dicetak untuk transaksi berstatus 'SELESAI'.")

        garis = "=" * 44
        baris = [
            self.__nama_toko.center(44),
            garis,
            f"No. Struk  : {transaksi.id_transaksi}",
            f"Pelanggan  : {transaksi.pelanggan.nama}",
            f"Tanggal    : {transaksi.tanggal.strftime('%d-%m-%Y %H:%M')}",
            garis,
        ]
        for item in transaksi.daftar_item:
            produk = item["produk"]
            baris.append(f"{produk.nama[:24]:<24} {item['jumlah']:>3} x Rp{produk.harga:,}")
            baris.append(f"{'':>34}Rp{item['subtotal']:,}")
        baris += [
            garis,
            f"{'TOTAL':<34}Rp{transaksi.total_harga:,}",
            garis,
            "Terima kasih atas kunjungan Anda!".center(44),
        ]
        return "\n".join(baris)

    def cetak_laporan_penjualan(self) -> str:
        """
        Menyusun laporan penjualan seluruh transaksi tercatat.

        Melempar LaporanKosongException jika belum ada transaksi.
        """
        if not self.__riwayat_transaksi:
            raise LaporanKosongException(
                "Laporan penjualan kosong: belum ada transaksi tercatat."
            )

        garis = "-" * 46
        baris = [
            f"{'LAPORAN PENJUALAN':^46}",
            self.__nama_toko.center(46),
            garis,
            f"Jumlah transaksi : {self.jumlah_transaksi}",
            f"Total pendapatan : Rp{self.total_pendapatan():,}",
            garis,
            "Rekap produk terjual:",
        ]
        # Urutkan dari qty terbesar (produk terlaris di atas).
        urutan = sorted(self.__rekap_produk.items(),
                        key=lambda x: x[1], reverse=True)
        for nama, qty in urutan:
            baris.append(f"  - {nama:<34} {qty:>3} pcs")
        return "\n".join(baris)

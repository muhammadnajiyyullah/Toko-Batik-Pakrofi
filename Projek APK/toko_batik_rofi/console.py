"""Perintah konsol berbasis teks untuk website Toko Batik Rofi.

KonsolToko menerjemahkan satu baris perintah menjadi pemanggilan method
pada service TokoBatik, lalu mengembalikan output berupa list baris teks.
"""

from exceptions import TokoBatikError
from utils import format_rupiah

BANTUAN = """Perintah yang tersedia:
  produk                                      Tampilkan daftar produk
  pelanggan                                   Tampilkan daftar pelanggan
  transaksi                                   Tampilkan riwayat transaksi
  laporan                                     Cetak ringkasan laporan
  terlaris                                    Tampilkan produk terlaris
  riwayat <id_pelanggan>                      Riwayat belanja pelanggan
  struk <id_transaksi>                        Cetak struk transaksi
  tambah-produk <tulis|cap|print> <kode> <harga> <stok> <nama...>
  tambah-pelanggan <id> <reguler|member> <no_hp> <nama...>
  beli <id_pelanggan> <kode> <jumlah> [<kode> <jumlah> ...]
  tambah-stok <kode> <jumlah>
  reset                                       Kembalikan data demo
  clear                                       Bersihkan layar
  help                                        Tampilkan bantuan ini"""


class KonsolToko:
    def __init__(self, toko):
        self.toko = toko

    def jalankan(self, baris):
        """Menjalankan satu perintah dan mengembalikan list baris output."""
        try:
            return self.__jalankan(baris)
        except TokoBatikError as error:
            return [f"Error: {error}"]
        except (ValueError, TypeError) as error:
            return [f"Error: input tidak valid ({error})."]

    def __jalankan(self, baris):
        token = str(baris).strip().split()
        if not token:
            return []

        perintah = token[0].lower()

        if perintah in ("help", "bantuan", "?"):
            return BANTUAN.splitlines()

        if perintah == "clear":
            return ["__CLEAR__"]

        if perintah == "produk":
            return self.__daftar_produk()

        if perintah == "pelanggan":
            return self.__daftar_pelanggan()

        if perintah == "transaksi":
            return self.__daftar_transaksi()

        if perintah == "laporan":
            return self.toko.cetak_laporan().splitlines()

        if perintah == "terlaris":
            terlaris = self.toko.laporan.produk_terlaris()
            return [
                "Produk terlaris:",
                f"  {terlaris['kode']} - {terlaris['nama']} "
                f"({terlaris['jumlah']} pcs terjual)",
            ]

        if perintah == "riwayat":
            return self.__riwayat(token)

        if perintah == "struk":
            return self.__struk(token)

        if perintah == "tambah-produk":
            return self.__tambah_produk(token)

        if perintah == "tambah-pelanggan":
            return self.__tambah_pelanggan(token)

        if perintah == "tambah-stok":
            return self.__tambah_stok(token)

        if perintah == "beli":
            return self.__beli(token)

        if perintah == "reset":
            self.toko.reset()
            return ["Data demo berhasil dikembalikan ke kondisi awal."]

        return [
            f"Perintah '{token[0]}' tidak dikenal.",
            "Ketik 'help' untuk melihat daftar perintah.",
        ]

    # ------------------------------------------------------------------
    # Perintah daftar
    # ------------------------------------------------------------------
    def __daftar_produk(self):
        produk = self.toko.produk_data()
        if not produk:
            return ["Belum ada produk."]

        baris = [
            f"{'KODE':<6} {'NAMA':<28} {'JENIS':<7} {'HARGA JUAL':>13} {'STOK':>5}",
            "-" * 64,
        ]
        for item in produk:
            baris.append(
                f"{item['kode']:<6} {self.__potong(item['nama'], 28):<28} "
                f"{item['jenis']:<7} "
                f"{format_rupiah(item['harga_jual']):>13} "
                f"{item['stok']:>5}"
            )
        return baris

    def __daftar_pelanggan(self):
        pelanggan = self.toko.pelanggan_data()
        if not pelanggan:
            return ["Belum ada pelanggan."]

        baris = [
            f"{'ID':<6} {'NAMA':<24} {'TIPE':<8} {'DISKON':>7} {'TRANSAKSI':>10}",
            "-" * 62,
        ]
        for item in pelanggan:
            baris.append(
                f"{item['id']:<6} {self.__potong(item['nama'], 24):<24} "
                f"{item['jenis']:<8} "
                f"{item['diskon_persen']:>6.0f}% "
                f"{item['jumlah_transaksi']:>10}"
            )
        return baris

    def __daftar_transaksi(self):
        transaksi = self.toko.transaksi_data()
        if not transaksi:
            return ["Belum ada transaksi."]

        baris = [
            f"{'ID':<8} {'TANGGAL':<17} {'PELANGGAN':<22} {'TOTAL':>14}",
            "-" * 66,
        ]
        for item in transaksi:
            pelanggan = f"{item['pelanggan']['id']} {item['pelanggan']['nama']}"
            baris.append(
                f"{item['id_transaksi']:<8} {item['tanggal']:<17} "
                f"{self.__potong(pelanggan, 22):<22} "
                f"{format_rupiah(item['total']):>14}"
            )
        return baris

    # ------------------------------------------------------------------
    # Perintah detail
    # ------------------------------------------------------------------
    def __riwayat(self, token):
        if len(token) != 2:
            return ["Format: riwayat <id_pelanggan>"]

        pelanggan, riwayat = self.toko.riwayat_pelanggan(token[1])
        if not riwayat:
            return [f"{pelanggan.id} - {pelanggan.nama} belum memiliki riwayat belanja."]

        baris = [f"Riwayat belanja {pelanggan.id} - {pelanggan.nama}:"]
        for transaksi in riwayat:
            baris.append(f"  {transaksi.info()}")
        return baris

    def __struk(self, token):
        if len(token) != 2:
            return ["Format: struk <id_transaksi>"]
        return self.toko.cetak_struk(token[1]).splitlines()

    def __tambah_produk(self, token):
        if len(token) < 6:
            return [
                "Format: tambah-produk <tulis|cap|print> <kode> <harga> <stok> <nama...>"
            ]

        jenis = token[1]
        kode = token[2]
        harga = int(token[3])
        stok = int(token[4])
        nama = " ".join(token[5:])

        produk = self.toko.tambah_produk(jenis, kode, nama, harga, stok)
        return [f"Produk berhasil ditambahkan: {produk.info()}"]

    def __tambah_pelanggan(self, token):
        if len(token) < 5:
            return [
                "Format: tambah-pelanggan <id> <reguler|member> <no_hp> <nama...>"
            ]

        id_pelanggan = token[1]
        tipe = token[2]
        no_hp = token[3]
        nama = " ".join(token[4:])

        pelanggan = self.toko.tambah_pelanggan(
            id_pelanggan, nama, no_hp, tipe
        )
        return [f"Pelanggan berhasil didaftarkan: {pelanggan.info()}"]

    def __tambah_stok(self, token):
        if len(token) != 3:
            return ["Format: tambah-stok <kode> <jumlah>"]

        produk = self.toko.tambah_stok(token[1], int(token[2]))
        return [
            f"Stok {produk.nama} ditambah. Stok sekarang: {produk.stok}."
        ]

    def __beli(self, token):
        if len(token) < 4 or (len(token) - 2) % 2 != 0:
            return [
                "Format: beli <id_pelanggan> <kode> <jumlah> [<kode> <jumlah> ...]"
            ]

        id_pelanggan = token[1]
        items = []
        for index in range(2, len(token), 2):
            items.append((token[index], int(token[index + 1])))

        transaksi = self.toko.buat_transaksi(id_pelanggan, items)
        output = [
            f"Transaksi {transaksi.id_transaksi} berhasil diproses.",
            "",
        ]
        output.extend(self.toko.cetak_struk(transaksi.id_transaksi).splitlines())
        return output

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    @staticmethod
    def __potong(teks, lebar):
        teks = str(teks)
        if len(teks) <= lebar:
            return teks
        return teks[: max(0, lebar - 3)] + "..."

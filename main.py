"""Program utama Toko Batik Rofi versi konsol.

Jalankan dari folder toko_batik_rofi:
    python main.py

Seluruh kesalahan logika toko ditangkap sebagai TokoBatikError sehingga
program tidak berhenti saat pengguna salah memasukkan data.
"""

from exceptions import TokoBatikError
from toko import TokoBatik
from utils import format_rupiah

LEBAR = 72


def garis(karakter="-"):
    print(karakter * LEBAR)


def judul(teks):
    garis("=")
    print(teks.center(LEBAR))
    garis("=")


def baca_teks(prompt):
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("  [!] Input tidak boleh kosong.")


def baca_angka(prompt, minimal=None):
    while True:
        nilai = input(prompt).strip()
        try:
            angka = int(nilai)
        except ValueError:
            print("  [!] Masukkan bilangan bulat.")
            continue
        if minimal is not None and angka < minimal:
            print(f"  [!] Nilai minimal {minimal}.")
            continue
        return angka


def baca_opsi(prompt, opsi):
    while True:
        nilai = input(prompt).strip().lower()
        if nilai in opsi:
            return nilai
        print(f"  [!] Pilihan harus salah satu dari: {', '.join(opsi)}.")


def tampil_produk(toko):
    data = toko.produk_data()
    judul("DAFTAR PRODUK BATIK")
    print(
        f"{'KODE':<6} {'NAMA':<28} {'JENIS':<7} "
        f"{'HARGA JUAL':>13} {'STOK':>5}"
    )
    garis()
    for item in data:
        print(
            f"{item['kode']:<6} {item['nama'][:28]:<28} {item['jenis']:<7} "
            f"{format_rupiah(item['harga_jual']):>13} {item['stok']:>5}"
        )
    garis()
    print(f"Total {len(data)} produk.")


def tambah_produk(toko):
    judul("TAMBAH PRODUK")
    jenis = baca_opsi(
        "Jenis (tulis/cap/print): ", ["tulis", "cap", "print"]
    )
    kode = baca_teks("Kode produk: ")
    nama = baca_teks("Nama produk: ")
    harga = baca_angka("Harga dasar (Rp): ", 1)
    stok = baca_angka("Stok awal: ", 0)
    produk = toko.tambah_produk(jenis, kode, nama, harga, stok)
    print(f"\n[OK] Produk ditambahkan: {produk.info()}")


def tampil_pelanggan(toko):
    data = toko.pelanggan_data()
    judul("DAFTAR PELANGGAN")
    print(
        f"{'ID':<6} {'NAMA':<24} {'TIPE':<8} {'DISKON':>7} "
        f"{'TRANSAKSI':>10} {'TOTAL BELANJA':>16}"
    )
    garis()
    for item in data:
        print(
            f"{item['id']:<6} {item['nama'][:24]:<24} {item['jenis']:<8} "
            f"{item['diskon_persen']:>6.0f}% {item['jumlah_transaksi']:>10} "
            f"{format_rupiah(item['total_belanja']):>16}"
        )
    garis()
    print(f"Total {len(data)} pelanggan.")


def daftarkan_pelanggan(toko):
    judul("DAFTARKAN PELANGGAN")
    id_pelanggan = baca_teks("ID pelanggan: ")
    nama = baca_teks("Nama pelanggan: ")
    no_hp = baca_teks("Nomor HP: ")
    tipe = baca_opsi("Tipe (reguler/member): ", ["reguler", "member"])
    pelanggan = toko.tambah_pelanggan(id_pelanggan, nama, no_hp, tipe)
    print(f"\n[OK] Pelanggan terdaftar: {pelanggan.info()}")


def buat_transaksi(toko):
    judul("BUAT TRANSAKSI")
    id_pelanggan = baca_teks("ID pelanggan: ")
    pelanggan = toko.cari_pelanggan(id_pelanggan)
    print(
        f"Pelanggan: {pelanggan.nama} "
        f"(diskon {pelanggan.diskon() * 100:.0f}%)"
    )

    items = []
    while True:
        kode = input("Kode produk (kosong = selesai): ").strip()
        if not kode:
            break

        produk = toko.cari_produk(kode)
        print(
            f"  {produk.nama} | harga jual {format_rupiah(produk.harga_jual())} "
            f"| stok {produk.stok}"
        )
        jumlah = baca_angka("  Jumlah: ", 1)
        items.append((produk.kode, jumlah))
        print(f"  Ditambahkan: {jumlah} x {produk.nama}")

    if not items:
        print("\n[!] Tidak ada item. Transaksi dibatalkan.")
        return

    transaksi = toko.buat_transaksi(pelanggan.id, items)
    print("\n[OK] Transaksi berhasil diproses.\n")
    print(toko.cetak_struk(transaksi.id_transaksi))


def lihat_riwayat(toko):
    judul("RIWAYAT PELANGGAN")
    id_pelanggan = baca_teks("ID pelanggan: ")
    pelanggan, riwayat = toko.riwayat_pelanggan(id_pelanggan)
    print(f"\n{pelanggan.info()}\n")

    if not riwayat:
        print("Belum ada riwayat belanja.")
        return

    for transaksi in riwayat:
        print(transaksi.info())


def cetak_laporan(toko):
    print()
    print(toko.cetak_laporan())


def tampilkan_menu():
    print()
    garis("=")
    print("TOKO BATIK ROFI - SISTEM PENJUALAN BATIK".center(LEBAR))
    garis("=")
    print("  1. Lihat daftar produk")
    print("  2. Tambah produk")
    print("  3. Daftarkan pelanggan")
    print("  4. Lihat daftar pelanggan")
    print("  5. Buat transaksi")
    print("  6. Lihat riwayat pelanggan")
    print("  7. Cetak laporan penjualan")
    print("  8. Keluar")
    garis()


def main():
    toko = TokoBatik()

    print()
    print("=" * LEBAR)
    print("SELAMAT DATANG DI TOKO BATIK ROFI".center(LEBAR))
    print("Sistem Penjualan Batik Berbasis Konsol".center(LEBAR))
    print("=" * LEBAR)
    print("Data demo telah dimuat. Pilih menu 1 untuk melihat produk.")

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu [1-8]: ").strip()

        try:
            if pilihan == "1":
                tampil_produk(toko)
            elif pilihan == "2":
                tambah_produk(toko)
            elif pilihan == "3":
                daftarkan_pelanggan(toko)
            elif pilihan == "4":
                tampil_pelanggan(toko)
            elif pilihan == "5":
                buat_transaksi(toko)
            elif pilihan == "6":
                lihat_riwayat(toko)
            elif pilihan == "7":
                cetak_laporan(toko)
            elif pilihan == "8":
                print("\nTerima kasih telah menggunakan Toko Batik Rofi.")
                break
            else:
                print("\n[!] Pilihan menu tidak valid. Masukkan angka 1-8.")
        except TokoBatikError as error:
            print(f"\n[!] {error}")
        except (ValueError, TypeError) as error:
            print(f"\n[!] Input tidak valid: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan. Terima kasih.")


"""
=====================================================================
 TUGAS BESAR PBO  |  SISTEM KASIR TOKO BATIK
 Modul : main.py  ->  INTEGRASI (dikerjakan BERSAMA seluruh anggota)
=====================================================================
 Menyatukan 4 class utama:
   Anggota A : ProdukBatik (produk.py)     -> data produk & stok
   Anggota B : Pelanggan   (pelanggan.py)  -> data pelanggan & riwayat
   Anggota C : Transaksi   (transaksi.py)  -> proses pembelian (kasir)
   Anggota D : Laporan     (laporan.py)    -> struk & laporan penjualan

 Cara menjalankan :  python main.py
=====================================================================
"""

from laporan import Laporan, LaporanKosongException
from pelanggan import (NomorTeleponTidakValidException, Pelanggan,
                       PelangganTidakTerdaftarException)
from produk import ProdukBatik
from transaksi import (JumlahItemTidakValidException, StokHabisException,
                       Transaksi, TransaksiKosongException)

GARIS = "=" * 46


def muat_data_awal():
    """Menyiapkan data awal toko: daftar produk & pelanggan terdaftar."""
    daftar_produk = {p.id_produk: p for p in [
        ProdukBatik("Kain Batik Parang", "Parang",
                    "Kain Batik", "2 meter", 350_000, 10),
        ProdukBatik("Kain Batik Mega Mendung", "Mega Mendung",
                    "Kain Batik", "2 meter", 420_000, 8),
        ProdukBatik("Kemeja Batik Pria", "Sogan",
                    "Pakaian Jadi", "L", 275_000, 15),
        ProdukBatik("Dress Batik Wanita", "Floral",
                    "Pakaian Jadi", "M", 390_000, 6),
        ProdukBatik("Scarf Batik Sutra", "Kawung",
                    "Aksesori", "All size", 150_000, 20),
    ]}

    daftar_pelanggan = {p.id_pelanggan: p for p in [
        Pelanggan("Budi Santoso", "081234567890", "budi@email.com"),
        Pelanggan("Siti Aminah", "081298765432", "siti@email.com"),
        Pelanggan("Rizky Pratama", "087811223344"),
    ]}
    return daftar_produk, daftar_pelanggan


def tampilkan_daftar_produk(daftar_produk):
    """Menu 1: menampilkan seluruh produk beserta stok terkini."""
    print(f"\n{'DAFTAR PRODUK':^46}")
    print("-" * 46)
    for produk in daftar_produk.values():
        print(produk.tampilkan_info())   # panggil method class Produk (A)


def buat_transaksi(daftar_produk, daftar_pelanggan, laporan):
    """Menu 2: alur kasir — inti integrasi keempat class."""
    id_pelanggan = input("\nID pelanggan (mis. PLG-001): ").strip().upper()

    # --- Integrasi class Pelanggan (B) + exception handling ---
    try:
        pelanggan = Pelanggan.cari_pelanggan(daftar_pelanggan, id_pelanggan)
    except PelangganTidakTerdaftarException as e:
        print(f"[GAGAL] {e}")
        return None

    # --- Integrasi class Transaksi (C) ---
    transaksi = Transaksi(pelanggan)
    print(f"\nTransaksi {transaksi.id_transaksi} dimulai untuk {pelanggan.nama}.")
    print("Masukkan ID produk dan jumlahnya. Ketik 'SELESAI' untuk mengakhiri.")

    while True:
        tampilkan_daftar_produk(daftar_produk)
        masukan = input("ID produk / SELESAI > ").strip().upper()
        if masukan == "SELESAI":
            break
        if masukan not in daftar_produk:
            print("[GAGAL] ID produk tidak ditemukan.\n")
            continue

        produk = daftar_produk[masukan]
        try:
            jumlah = int(input(f"Jumlah '{produk.nama}' (stok {produk.stok}): "))
        except ValueError:
            print("[GAGAL] Jumlah harus berupa angka.\n")
            continue

        # --- Integrasi class Produk (A) + exception Transaksi (C) ---
        try:
            transaksi.tambah_item(produk, jumlah)
            print(f"[OK] {jumlah}x {produk.nama} masuk keranjang | "
                  f"Total sementara: Rp{transaksi.total_harga:,}\n")
        except (StokHabisException, JumlahItemTidakValidException) as e:
            print(f"[GAGAL] {e}\n")

    if len(transaksi.daftar_item) == 0:
        print("[BATAL] Transaksi dibatalkan (tidak ada item).")
        return None

    try:
        ringkasan = transaksi.proses_transaksi()   # status -> SELESAI
    except TransaksiKosongException as e:
        print(f"[GAGAL] {e}")
        return None

    # --- Integrasi class Laporan (D) & riwayat Pelanggan (B) ---
    laporan.catat_transaksi(transaksi)
    pelanggan.tambah_riwayat(ringkasan)

    print("\n" + laporan.cetak_struk(transaksi))
    return transaksi


def tampilkan_daftar_pelanggan(daftar_pelanggan):
    """Menu 3: menampilkan seluruh pelanggan terdaftar."""
    print(f"\n{'DAFTAR PELANGGAN':^46}")
    print("-" * 46)
    for pelanggan in daftar_pelanggan.values():
        print(pelanggan)


def tambah_pelanggan_baru(daftar_pelanggan):
    """Menu 4: registrasi pelanggan (demonstrasi validasi & exception)."""
    nama = input("Nama pelanggan   : ").strip()
    telp = input("No. telepon      : ").strip()
    email = input("Email (opsional) : ").strip() or "-"
    try:
        pelanggan = Pelanggan(nama, telp, email)
    except (ValueError, NomorTeleponTidakValidException) as e:
        print(f"[GAGAL] {e}")
        return
    daftar_pelanggan[pelanggan.id_pelanggan] = pelanggan
    print(f"[OK] Pelanggan baru terdaftar dengan ID {pelanggan.id_pelanggan}.")


def main():
    """Fungsi utama: menjalankan menu interaktif kasir toko batik."""
    daftar_produk, daftar_pelanggan = muat_data_awal()
    laporan = Laporan("Toko Batik Nusantara")
    transaksi_terakhir = None

    print(GARIS)
    print(f"{'SISTEM KASIR TOKO BATIK':^46}")
    print(f"{'Toko Batik Nusantara':^46}")
    print(GARIS)

    while True:
        print(f"""
{GARIS}
 MENU:
   1. Lihat daftar produk
   2. Buat transaksi baru (kasir)
   3. Lihat daftar pelanggan
   4. Tambah pelanggan baru
   5. Cetak struk transaksi terakhir
   6. Lihat laporan penjualan
   0. Keluar
{GARIS}""")
        pilihan = input("Pilih menu > ").strip()

        if pilihan == "1":
            tampilkan_daftar_produk(daftar_produk)
        elif pilihan == "2":
            hasil = buat_transaksi(daftar_produk, daftar_pelanggan, laporan)
            if hasil is not None:
                transaksi_terakhir = hasil
        elif pilihan == "3":
            tampilkan_daftar_pelanggan(daftar_pelanggan)
        elif pilihan == "4":
            tambah_pelanggan_baru(daftar_pelanggan)
        elif pilihan == "5":
            if transaksi_terakhir is None:
                print("[INFO] Belum ada transaksi pada sesi ini.")
            else:
                print("\n" + laporan.cetak_struk(transaksi_terakhir))
        elif pilihan == "6":
            try:
                print("\n" + laporan.cetak_laporan_penjualan())
            except LaporanKosongException as e:
                print(f"[INFO] {e}")
        elif pilihan == "0":
            print("\nTerima kasih! Sampai jumpa.")
            break
        else:
            print("[GAGAL] Pilihan tidak dikenal.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan. Terima kasih!")

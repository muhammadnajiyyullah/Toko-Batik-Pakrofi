# Tugas Besar PBO — Sistem Kasir Toko Batik 🏪🧵

Mata Kuliah : Pemrograman Berorientasi Objek (INF2516) — Semester 3
Prodi       : Informatika

## 📌 Aturan Proyek
**1 Anggota = 1 Class Utama.** Setiap anggota bertindak sebagai Developer, Tester,
dan Dokumentator penuh untuk class miliknya (desain atribut, method, custom
exception, unit test, dokumentasi, logbook).

## 👥 Pembagian Class (4 Anggota)

| Anggota | Class Utama | File | Tanggung Jawab | Custom Exception | Collection |
|---|---|---|---|---|---|
| A | `ProdukBatik` | `produk.py` | Atribut private, getter/setter, validasi harga & stok, `kurangi_stok()` | `HargaTidakValidException`, `StokTidakValidException` | — |
| B | `Pelanggan` | `pelanggan.py` | Data pelanggan, riwayat belanja, pencarian pelanggan | `PelangganTidakTerdaftarException`, `NomorTeleponTidakValidException` | `List` riwayat belanja |
| C | `Transaksi` | `transaksi.py` | Keranjang, hitung total, **memanggil class Produk**, finalisasi | `StokHabisException`, `JumlahItemTidakValidException`, `TransaksiKosongException` | `List of Dict` keranjang |
| D | `Laporan` | `laporan.py` | Riwayat penjualan, rekap produk, **cetak struk** & laporan | `LaporanKosongException` | `List` riwayat + `Dict` rekap |
| Bersama | — | `main.py` | Integrasi seluruh class menjadi aplikasi kasir utuh | — | — |

## 📂 Struktur Proyek

```
toko_batik/
├── produk.py          # Class utama Anggota A
├── pelanggan.py       # Class utama Anggota B
├── transaksi.py       # Class utama Anggota C
├── laporan.py         # Class utama Anggota D
├── main.py            # Integrasi (dikerjakan bersama)
├── test_produk.py     # Unit test Anggota A (19 test)
├── test_pelanggan.py  # Unit test Anggota B (21 test)
├── test_transaksi.py  # Unit test Anggota C (16 test)
├── test_laporan.py    # Unit test Anggota D (13 test)
└── dokumentasi/
    ├── dokumentasi_anggota_a_produk.md
    ├── dokumentasi_anggota_b_pelanggan.md
    ├── dokumentasi_anggota_c_transaksi.md
    └── dokumentasi_anggota_d_laporan.md
```

## ▶️ Cara Menjalankan Aplikasi

```bash
cd toko_batik
python main.py
```

Menu tersedia: lihat produk, transaksi kasir, daftar/tambah pelanggan,
cetak struk, dan laporan penjualan.

## ✅ Cara Menjalankan Unit Test

Seluruh test (69 test case):

```bash
python -m unittest -v
```

Per class saja:

```bash
python -m unittest test_produk -v      # Anggota A
python -m unittest test_pelanggan -v    # Anggota B
python -m unittest test_transaksi -v    # Anggota C
python -m unittest test_laporan -v      # Anggota D
```

> Hasil terakhir: `Ran 69 tests ... OK` — **semua test lulus (green)**.
> Screenshot hasil test untuk Laporan Pertemuan 14.

## 🔗 Alur Integrasi (main.py)

1. `Pelanggan.cari_pelanggan()` → validasi pelanggan terdaftar (Exception B).
2. `Transaksi(pelanggan)` → keranjang dibuat.
3. `transaksi.tambah_item(produk, jumlah)` → cek stok, panggil
   `produk.kurangi_stok()` (Class A), lempar `StokHabisException` bila kurang.
4. `transaksi.proses_transaksi()` → status `SELESAI` + ringkasan Dict.
5. `laporan.catat_transaksi()` (Class D) & `pelanggan.tambah_riwayat()`.
6. `laporan.cetak_struk()` → struk tercetak; laporan penjualan selalu ter-update.

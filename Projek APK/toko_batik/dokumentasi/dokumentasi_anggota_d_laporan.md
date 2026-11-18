# Dokumentasi Class `Laporan` — Anggota D

| | |
|---|---|
| Mata Kuliah | Pemrograman Berorientasi Objek (INF2516) — Semester 3 |
| Proyek | Tugas Besar — Sistem Kasir Toko Batik |
| Class Utama | `Laporan` (`laporan.py`) |
| Peran Saya | Developer, Tester, dan Dokumentator class ini |

---

## 1. Deskripsi dan Fungsi Utama

Class `Laporan` mengelola **seluruh data penjualan toko**: mencatat transaksi yang telah selesai, mengagregasi produk terjual, mencetak **struk** pembelian, dan menyusun **laporan penjualan**. Sesuai ketentuan dokumen Tugas Besar, class ini menggunakan **Collection (List/Dict) untuk menyimpan riwayat**: List untuk objek transaksi terurut dan Dict untuk rekap jumlah produk terjual.

Class ini menerima objek `Transaksi` (Anggota C) melalui `catat_transaksi()` dan membaca detail item di dalamnya (yang memuat objek `ProdukBatik` milik Anggota A).

## 2. Rancangan Atribut (Encapsulation)

| Atribut | Tipe | Akses | Deskripsi |
|---|---|---|---|
| `__nama_toko` | `str` | private | Nama toko yang tercetak pada struk/laporan |
| `__riwayat_transaksi` | `List[Transaksi]` | private | **Collection (List)** objek transaksi tercatat |
| `__rekap_produk` | `Dict[str, int]` | private | **Collection (Dict)** `{nama_produk: total_qty_terjual}` |

## 3. Rancangan Method

| Method | Deskripsi | Exception |
|---|---|---|
| `__init__(nama_toko)` | Konstruktor; nama toko tidak boleh kosong | `ValueError` |
| property `nama_toko`, `jumlah_transaksi` | Getter dasar | — |
| property `rekap_produk` | Getter **salinan** Dict rekap (encapsulation) | — |
| `catat_transaksi(transaksi)` | Menyimpan transaksi berstatus `"SELESAI"` ke List & memperbarui Dict rekap | `ValueError` |
| `total_pendapatan()` | Menjumlahkan total harga seluruh transaksi | — |
| `produk_terlaris()` | Mengembalikan `(nama, qty)` produk paling banyak terjual | `LaporanKosongException` |
| `cetak_struk(transaksi)` | Menyusun teks struk: nama toko, no. struk, pelanggan, item, TOTAL | `ValueError` |
| `cetak_laporan_penjualan()` | Menyusun teks laporan: jumlah transaksi, total pendapatan, rekap produk terurut | `LaporanKosongException` |

## 4. Custom Exception

| Exception | Dipicu Ketika |
|---|---|
| `LaporanKosongException` | `produk_terlaris()` / `cetak_laporan_penjualan()` dipanggil saat belum ada transaksi tercatat |

## 5. Penerapan Encapsulation

1. Atribut private; pengisian data **hanya** melalui `catat_transaksi()` yang memvalidasi status transaksi.
2. Getter `rekap_produk` mengembalikan **salinan Dict** — perubahan dari luar tidak memengaruhi data internal (dibuktikan pada unit test `test_08`).
3. Objek di dalam List riwayat hanya dibaca (read-only usage), tidak dimodifikasi.

## 6. Collection yang Digunakan (sesuai ketentuan Tugas Besar)

- **List** — `__riwayat_transaksi`: menyimpan objek `Transaksi` secara terurut.
- **Dict** — `__rekap_produk`: agregasi `{nama_produk: total_qty}` dengan pola `get(nama, 0) + jumlah`.

## 7. Unit Test

File `test_laporan.py` — 13 test case (8 positive, 5 negative), semua **lulus (green)**:
- Positive: catat 1 & 2 transaksi, rekap produk lintas transaksi (2+1 = 3), total pendapatan (Rp400.000), produk terlaris, isi struk (nama toko/ID/pelanggan/item/total), isi laporan penjualan, rekap mengembalikan salinan.
- Negative: mencatat transaksi `"BERJALAN"`, produk terlaris & laporan kosong, struk transaksi belum selesai, nama toko kosong.

## 8. Contoh Penggunaan

```python
from laporan import Laporan, LaporanKosongException
from transaksi import Transaksi
from pelanggan import Pelanggan
from produk import ProdukBatik

laporan = Laporan("Toko Batik Nusantara")
trx = Transaksi(Pelanggan("Budi Santoso", "081234567890"))
trx.tambah_item(ProdukBatik("Kain Batik Parang", "Parang", "Kain Batik",
                            "2 meter", 350_000, 10), 2)
trx.proses_transaksi()

laporan.catat_transaksi(trx)
print(laporan.cetak_struk(trx))
print(laporan.total_pendapatan())      # 700000
try:
    Laporan().cetak_laporan_penjualan()
except LaporanKosongException as e:
    print(e)
```

## 9. Logbook Individu

| Pertemuan | Aktivitas (coding, testing, bug fixing) | Output | Paraf Ketua |
|---|---|---|---|
| Pert. 11 | Desain UML class `Laporan`: menentukan Collection List (riwayat) & Dict (rekap produk), rancangan cetak struk | File gambar UML draft | (ttd) |
| Pert. 12 | Coding skeleton class `Laporan` (atribut private, kerangka List & Dict kosong) | `laporan.py` (skeleton) | (ttd) |
| Pert. 13 | Menambah Custom Exception `LaporanKosongException`, method `catat_transaksi()` & rekap produk, method `cetak_struk()` | `laporan.py` v0.3 | (ttd) |
| Pert. 14 | Unit test `test_laporan.py` (13 test positive & negative — **semua lulus**), bug fixing format struk (rata kanan angka), screenshot hasil test | `test_laporan.py` + screenshot | (ttd) |
| Pert. 15 | Integrasi dengan `main.py` (struk otomatis tercetak setelah transaksi, menu laporan penjualan), finalisasi dokumentasi | Source code utuh (ZIP) + laporan | (ttd) |

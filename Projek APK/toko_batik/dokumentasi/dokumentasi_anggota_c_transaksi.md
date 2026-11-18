# Dokumentasi Class `Transaksi` — Anggota C

| | |
|---|---|
| Mata Kuliah | Pemrograman Berorientasi Objek (INF2516) — Semester 3 |
| Proyek | Tugas Besar — Sistem Kasir Toko Batik |
| Class Utama | `Transaksi` (`transaksi.py`) |
| Peran Saya | Developer, Tester, dan Dokumentator class ini |

---

## 1. Deskripsi dan Fungsi Utama

Class `Transaksi` menjalankan peran **kasir**: mengelola keranjang belanja, menghitung total harga, dan memfinalisasi pembelian. Class ini merupakan pusat integrasi karena **memanggil class `ProdukBatik` (Anggota A)** saat memeriksa dan mengurangi stok, serta **menyimpan objek `Pelanggan` (Anggota B)** sebagai pembeli. Hasil `proses_transaksi()` (Dict ringkasan) diteruskan ke **`Laporan` (Anggota D)** dan ke riwayat pelanggan melalui `main.py`.

Sesuai ketentuan dokumen Tugas Besar, class ini mendefinisikan **Custom Exception `StokHabisException`** yang terpicu saat pelanggan memesan jumlah melebihi stok tersedia.

## 2. Rancangan Atribut (Encapsulation)

| Atribut | Tipe | Akses | Deskripsi |
|---|---|---|---|
| `__id_transaksi` | `str` | private, read-only | ID otomatis `TRX-001`, `TRX-002`, … |
| `__pelanggan` | `Pelanggan` | private | Objek pelanggan pembeli |
| `__tanggal` | `datetime` | private | Waktu transaksi dibuat |
| `__daftar_item` | `List[Dict]` | private | **Collection (List of Dict)** keranjang: `{"produk", "jumlah", "subtotal"}` |
| `__total_harga` | `int` | private | Total harga; hanya berubah lewat `tambah_item()` |
| `__status` | `str` | private | `"BERJALAN"` → `"SELESAI"` (finalisasi satu arah) |
| `_jumlah_transaksi` | `int` | class attribute | Penghitung objek untuk ID otomatis |

## 3. Rancangan Method

| Method | Deskripsi | Exception |
|---|---|---|
| `__init__(pelanggan, tanggal=None)` | Konstruktor; validasi pelanggan harus objek `Pelanggan` | `ValueError` |
| property `id_transaksi`, `pelanggan`, `tanggal`, `total_harga`, `status` | Getter read-only | — |
| property `daftar_item` | Getter **salinan** keranjang (encapsulation) | — |
| `tambah_item(produk, jumlah)` | Inti kasir: validasi → cek stok → gabung bila produk sama → panggil `produk.kurangi_stok()` → perbarui total | `StokHabisException`, `JumlahItemTidakValidException`, `ValueError` |
| `hitung_total()` | Menjumlahkan subtotal seluruh item | — |
| `proses_transaksi()` | Finalisasi: status → `"SELESAI"`, mengembalikan Dict ringkasan untuk `Laporan` & riwayat `Pelanggan` | `TransaksiKosongException` |
| `__str__()` | Ringkasan satu baris | — |

## 4. Custom Exception

| Exception | Dipicu Ketika |
|---|---|
| `StokHabisException` | Jumlah diminta > stok tersedia. Menyimpan atribut `nama_produk`, `stok_tersisa`, `jumlah_diminta` untuk penelusuran |
| `JumlahItemTidakValidException` | Jumlah item ≤ 0 / bukan bilangan bulat |
| `TransaksiKosongException` | Transaksi difinalisasi tanpa memiliki item |

## 5. Penerapan Encapsulation

1. Seluruh atribut private; keranjang `__daftar_item` **tidak** bisa diubah langsung — hanya lewat `tambah_item()` yang memvalidasi.
2. Getter `daftar_item` mengembalikan **salinan list**.
3. `total_harga` dan `status` tidak punya setter — nilainya murni hasil proses method internal, sehingga total tidak bisa dipalsukan dari luar.
4. Setelah `"SELESAI"`, transaksi tidak dapat diubah lagi.

## 6. Collection yang Digunakan

- **List of Dict** — `__daftar_item` (keranjang belanja), tiap elemen `{"produk": ProdukBatik, "jumlah": int, "subtotal": int}`.
- **Dict** — struktur ringkasan hasil `proses_transaksi()` (dipakai class lain).

## 7. Unit Test

File `test_transaksi.py` — 16 test case (7 positive, 9 negative), semua **lulus (green)**:
- Positive: ID otomatis, status awal `BERJALAN`, tambah item (stok produk berkurang 10 → 8), penggabungan item sama (1 baris, jumlah 5), hitung total multi produk, ringkasan `proses_transaksi()`, `__str__`.
- Negative: jumlah 0/negatif, stok habis (stok tetap tidak berubah), pesan exception informatif, atribut exception terisi, transaksi kosong, pelanggan/produk bukan objek valid.

## 8. Contoh Penggunaan

```python
from produk import ProdukBatik
from pelanggan import Pelanggan
from transaksi import Transaksi, StokHabisException

kain = ProdukBatik("Kain Batik Parang", "Parang", "Kain Batik",
                   "2 meter", 350_000, 10)
budi = Pelanggan("Budi Santoso", "081234567890")

trx = Transaksi(budi)
trx.tambah_item(kain, 2)          # total Rp700.000, stok jadi 8
try:
    trx.tambah_item(kain, 50)      # stok tidak cukup
except StokHabisException as e:
    print(e)
ringkasan = trx.proses_transaksi() # status -> SELESAI, siap dicatat Laporan
```

## 9. Logbook Individu

| Pertemuan | Aktivitas (coding, testing, bug fixing) | Output | Paraf Ketua |
|---|---|---|---|
| Pert. 11 | Desain UML class `Transaksi`: rancangan keranjang (List of Dict), relasi memanggil class `Produk` & menyimpan `Pelanggan` | File gambar UML draft | (ttd) |
| Pert. 12 | Coding skeleton class `Transaksi` (atribut private, kerangka method kosong) | `transaksi.py` (skeleton) | (ttd) |
| Pert. 13 | Menambah Custom Exception `StokHabisException` (+ 2 exception pendukung), integrasi pemanggilan `produk.kurangi_stok()` | `transaksi.py` v0.3 | (ttd) |
| Pert. 14 | Unit test `test_transaksi.py` (16 test positive & negative — **semua lulus**), bug fixing penggabungan item produk sama, screenshot hasil test | `test_transaksi.py` + screenshot | (ttd) |
| Pert. 15 | Integrasi dengan `main.py` (alur kasir lengkap: cari pelanggan → tambah item → struk), finalisasi dokumentasi | Source code utuh (ZIP) + laporan | (ttd) |

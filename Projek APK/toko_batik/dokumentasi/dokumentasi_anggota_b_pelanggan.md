# Dokumentasi Class `Pelanggan` — Anggota B

| | |
|---|---|
| Mata Kuliah | Pemrograman Berorientasi Objek (INF2516) — Semester 3 |
| Proyek | Tugas Besar — Sistem Kasir Toko Batik |
| Class Utama | `Pelanggan` (`pelanggan.py`) |
| Peran Saya | Developer, Tester, dan Dokumentator class ini |

---

## 1. Deskripsi dan Fungsi Utama

Class `Pelanggan` mengelola **data pelanggan toko**: identitas (ID otomatis, nama, no. telepon, email) dan **riwayat belanja**. Class ini juga menyediakan fitur pencarian pelanggan (`cari_pelanggan`) yang dipakai `main.py` sebelum transaksi dibuat — jika ID tidak ditemukan, `PelangganTidakTerdaftarException` dilempar dan ditangani dengan pesan yang informatif.

Setiap transaksi yang selesai, ringkasan belanja (Dict hasil `Transaksi.proses_transaksi()`) dicatat ke riwayat pelanggan melalui `tambah_riwayat()`.

## 2. Rancangan Atribut (Encapsulation)

| Atribut | Tipe | Akses | Deskripsi |
|---|---|---|---|
| `__id_pelanggan` | `str` | private, read-only | ID unik otomatis `PLG-001`, `PLG-002`, … |
| `__nama` | `str` | private | Nama pelanggan, tidak boleh kosong |
| `__no_telepon` | `str` | private | 10–13 digit angka |
| `__email` | `str` | private | Format mengandung `@` dan `.`; opsional (default `"-"`) |
| `__riwayat_belanja` | `List[Dict]` | private | **Collection (List)** berisi ringkasan transaksi tiap belanja |
| `_jumlah_pelanggan` | `int` | class attribute | Penghitung objek untuk ID otomatis |

## 3. Rancangan Method

| Method | Deskripsi | Exception |
|---|---|---|
| `__init__(nama, no_telepon, email="-")` | Konstruktor dengan validasi lewat setter | `NomorTeleponTidakValidException`, `ValueError` |
| property `id_pelanggan`, `nama`, `no_telepon`, `email`, `riwayat_belanja` | Getter; `riwayat_belanja` mengembalikan **salinan list** | — |
| setter `nama` / `no_telepon` / `email` | Validasi: nama tidak kosong; telepon 10–13 digit; email berformat benar | `NomorTeleponTidakValidException`, `ValueError` |
| `tambah_riwayat(ringkasan)` | Menyimpan Dict ringkasan transaksi ke riwayat; wajib berkey `id_transaksi` & `total` | `ValueError` |
| `total_belanja()` | Menjumlahkan total seluruh riwayat belanja | — |
| `tampilkan_riwayat()` | String riwayat belanja (atau pesan "belum memiliki riwayat") | — |
| `cari_pelanggan(daftar, id)` *(static)* | Mencari pelanggan pada `Dict {id: Pelanggan}`; tidak peka huruf besar/kecil | `PelangganTidakTerdaftarException` |

## 4. Custom Exception

| Exception | Dipicu Ketika |
|---|---|
| `PelangganTidakTerdaftarException` | ID pelanggan tidak ada di daftar saat akan bertransaksi (dipakai di `main.py`) |
| `NomorTeleponTidakValidException` | No. telepon bukan 10–13 digit angka |

## 5. Penerapan Encapsulation

1. Atribut private `__nama`, `__no_telepon`, dll. + validasi pada setter.
2. **`riwayat_belanja` hanya bisa diisi lewat `tambah_riwayat()`** (dengan validasi), dan getter mengembalikan **salinan** sehingga list internal tidak bisa dimanipulasi dari luar.
3. `id_pelanggan` read-only (dibuat otomatis sistem).

## 6. Collection yang Digunakan

- **List** — `__riwayat_belanja`: kumpulan Dict ringkasan transaksi milik pelanggan.
- **Dict** — dipakai `main.py` sebagai daftar pelanggan terdaftar `{id_pelanggan: objek Pelanggan}`, parameternya juga dipakai `cari_pelanggan()`.

## 7. Unit Test

File `test_pelanggan.py` — 21 test case (11 positive, 10 negative), semua **lulus (green)**:
- Positive: ID otomatis, getter/setter valid, email opsional, tambah riwayat, total belanja, cari ditemukan (termasuk huruf kecil).
- Negative: telepon terlalu pendek/berisi huruf, nama kosong, email tanpa `@`, ringkasan bukan Dict / tanpa key wajib / total negatif, pelanggan tidak terdaftar (pesan memuat ID).

## 8. Contoh Penggunaan

```python
from pelanggan import Pelanggan, PelangganTidakTerdaftarException

daftar = {}
budi = Pelanggan("Budi Santoso", "081234567890", "budi@email.com")
daftar[budi.id_pelanggan] = budi

try:
    pelanggan = Pelanggan.cari_pelanggan(daftar, "PLG-999")
except PelangganTidakTerdaftarException as e:
    print(e)   # Pelanggan dengan ID 'PLG-999' tidak terdaftar.
```

## 9. Logbook Individu

| Pertemuan | Aktivitas (coding, testing, bug fixing) | Output | Paraf Ketua |
|---|---|---|---|
| Pert. 11 | Desain UML class `Pelanggan`: atribut private, rancangan riwayat belanja (List) & exception pelanggan tidak terdaftar | File gambar UML draft | (ttd) |
| Pert. 12 | Coding skeleton class `Pelanggan` (atribut private, kerangka getter/setter, list riwayat) | `pelanggan.py` (skeleton) | (ttd) |
| Pert. 13 | Menambah Custom Exception (`PelangganTidakTerdaftarException`, `NomorTeleponTidakValidException`) + method `cari_pelanggan()` | `pelanggan.py` v0.3 | (ttd) |
| Pert. 14 | Unit test `test_pelanggan.py` (21 test positive & negative — **semua lulus**), perbaikan validasi email, screenshot hasil test | `test_pelanggan.py` + screenshot | (ttd) |
| Pert. 15 | Integrasi dengan `main.py` (pencarian & registrasi pelanggan), riwayat belanja terisi otomatis setelah transaksi, finalisasi dokumentasi | Source code utuh (ZIP) + laporan | (ttd) |

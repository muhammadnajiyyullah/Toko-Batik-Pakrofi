# Template Laporan Tugas Besar PBO

> Salin dokumen ini, lengkapi bagian bertanda `[...]`, lalu ekspor ke PDF.

## Halaman Judul

**TUGAS BESAR PEMROGRAMAN BERORIENTASI OBJEK**
**SISTEM PENJUALAN BATIK BERBASIS KONSOL (PYTHON)**
**TOKO BATIK ROFI**

- Mata Kuliah: INF2516 — Pemrograman Berorientasi Objek
- Semester: 3
- Kelas: [...]
- Dosen: [...]
- Kelompok: [...]
- Anggota:
  1. [Nama] — [NIM] — Class `ProdukBatik`
  2. [Nama] — [NIM] — Class `Pelanggan`
  3. [Nama] — [NIM] — Class `Transaksi`
  4. [Nama] — [NIM] — Class `Laporan`

## 1. Latar Belakang

[Contoh] Toko Batik Rofi masih mencatat penjualan secara manual sehingga
rawan kesalahan stok dan perhitungan diskon. Aplikasi berbasis konsol ini
dibuat untuk mencatat produk, pelanggan, transaksi, dan laporan penjualan
secara terstruktur dengan menerapkan konsep PBO.

## 2. Deskripsi Sistem

- Nama sistem: Toko Batik Rofi
- Jenis aplikasi: CLI (Command Line Interface) berbasis Python, dilengkapi website Flask
- Fungsi utama: pengelolaan produk, pelanggan, transaksi, dan laporan
- Aturan bisnis: stok tidak boleh minus, harga > 0, member mendapat diskon 10%

## 3. Diagram UML

[Tempel hasil render `docs/uml_toko_batik.puml` di sini.]

Penjelasan relasi:

- `BatikTulis`, `BatikCap`, `BatikPrint` mewarisi `ProdukBatik`.
- `PelangganReguler`, `PelangganMember` mewarisi `Pelanggan`.
- `Transaksi` berkomposisi dengan `ProdukBatik` dan terhubung ke `Pelanggan`.
- `Laporan` menyimpan banyak `Transaksi`.

## 4. Dokumentasi Class

### 4.1 ProdukBatik — [Nama Anggota A]

- Atribut: `__kode`, `__nama`, `__harga_dasar`, `__stok`
- Property: `kode`, `nama`, `harga_dasar`, `stok`
- Method: `harga_jual()`, `kurangi_stok()`, `tambah_stok()`, `info()`
- Encapsulation: [jelaskan private attribute dan setter]
- Inheritance: [jelaskan subclass]
- Polymorphism: [jelaskan override harga_jual]
- Exception: `DataProdukTidakValidError`
- Screenshot unit test: [tempel]

### 4.2 Pelanggan — [Nama Anggota B]

- Atribut: `__id`, `__nama`, `__no_hp`, `__riwayat_belanja`
- Property: `id`, `nama`, `no_hp`, `jenis`, `riwayat_belanja`
- Method: `tambah_riwayat()`, `lihat_riwayat()` (mengembalikan list salinan),
  `diskon()`, `info()`
- Encapsulation: [riwayat dikembalikan sebagai salinan]
- Inheritance: [PelangganReguler, PelangganMember]
- Polymorphism: [override diskon]
- Exception: `PelangganTidakTerdaftarError`, `DataPelangganTidakValidError`
- Screenshot unit test: [tempel]

### 4.3 Transaksi — [Nama Anggota C]

- Atribut: `__id_transaksi`, `__pelanggan`, `__item`, `__tanggal`
- Method: `tambah_item()`, `hitung_subtotal()`, `hitung_diskon()`,
  `hitung_total()`, `proses()`, `to_dict()`, `info()`
- Komposisi: [Transaksi memakai ProdukBatik dan Pelanggan]
- Custom exception: `StokHabisError`, `JumlahTidakValidError`,
  `TransaksiTidakValidError`
- Atomicity: [stok divalidasi semua dulu sebelum dikurangi]
- Screenshot unit test: [tempel]

### 4.4 Laporan — [Nama Anggota D]

- Atribut: `__daftar_transaksi` (list), `__rekap_produk` (dict)
- Method: `tambah_transaksi()`, `total_pendapatan()`, `produk_terlaris()`,
  `rekap_per_pelanggan()`, `cetak_struk()`, `cetak_ringkasan()`
- Collection: [jelaskan list dan dict rekap]
- Exception: `LaporanKosongError`, `TransaksiTidakValidError`
- Screenshot unit test: [tempel]

## 5. Integrasi main.py

[Jelaskan menu 1–8 dan alur transaksi. Tempel screenshot program konsol dan website.]

## 6. Hasil Unit Test

Perintah: `python -m unittest discover tests -v`

Hasil: 53 test, OK.

[Tempel screenshot.]

## 7. Hasil Menjalankan Program

[Tempel screenshot menu, transaksi, struk, dan laporan.]

## 8. Kendala dan Solusi

| Kendala | Solusi |
|---|---|
| [ ... ] | [ ... ] |

## 9. Kesimpulan

[Ringkas pencapaian: seluruh ketentuan blueprint terpenuhi, 53 unit test
lulus, dan aplikasi konsol maupun website berjalan tanpa error.]

## Lampiran

- Logbook anggota A: [ ... ]
- Logbook anggota B: [ ... ]
- Logbook anggota C: [ ... ]
- Logbook anggota D: [ ... ]
- Source code (ZIP)

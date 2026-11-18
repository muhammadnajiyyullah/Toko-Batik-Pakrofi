# Analisis Blueprint — Toko Batik Rofi

Dokumen ini merangkum analisis `Blueprint_Toko_Batik_Rofi.docx` dan bagaimana setiap ketentuan diterjemahkan menjadi kode.

---

## 1. Ketentuan Utama Blueprint

| Aspek | Ketentuan | Status Implementasi |
| --- | --- | --- |
| Aturan class | 1 anggota = 1 class utama, minimal 3–4 class mandiri | Terpenuhi: `ProdukBatik`, `Pelanggan`, `Transaksi`, `Laporan` |
| Class turunan | Tanggung jawab pemilik class induk | Terpenuhi: 3 turunan produk dan 2 turunan pelanggan |
| Encapsulation | Atribut private + `@property` | Terpenuhi di seluruh class |
| Inheritance | Minimal satu hierarki class | Terpenuhi |
| Polymorphism | Method dioverride subclass | `harga_jual()` dan `diskon()` |
| Custom Exception | Minimal satu per class relevan | 7 custom exception, semuanya mewarisi `TokoBatikError` |
| Collection | List/Dict | Item transaksi, riwayat, daftar pelanggan, rekap laporan |
| Unit Test | Library `unittest` | 53 test di folder `tests/` |
| Integrasi | `main.py` menyatukan seluruh class | Terpenuhi, ditambah `toko.py` sebagai service |
| Output tambahan | Website | Flask + REST API + konsol browser |

---

## 2. Analisis Pembagian Class

### 2.1 Anggota A — `ProdukBatik`

**Tanggung jawab:** menyimpan identitas produk, harga dasar, stok, dan aturan harga jual.

| Kebutuhan blueprint | Implementasi |
| --- | --- |
| Atribut private `__kode`, `__nama`, `__harga_dasar`, `__stok` | `produk_batik.py` |
| Getter semua atribut | `kode`, `nama`, `jenis`, `harga_dasar`, `stok` |
| Setter tervalidasi | `harga_dasar` (> 0), `stok` (≥ 0) |
| `kurangi_stok()`, `tambah_stok()` | Tersedia, memakai `JumlahTidakValidError` dan `StokHabisError` |
| `harga_jual()` polymorphic | `BatikTulis` ×1,5; `BatikCap` ×1,2; `BatikPrint` ×1,0 |
| Exception | `DataProdukTidakValidError`, `StokHabisError`, `JumlahTidakValidError` |

**Keputusan desain:** validasi teks dan angka dipusatkan pada helper statis private agar tidak duplikatif. Setter dipanggil dari constructor sehingga validasi hanya ditulis sekali.

### 2.2 Anggota B — `Pelanggan`

**Tanggung jawab:** menyimpan data pelanggan, riwayat belanja, dan aturan diskon.

| Kebutuhan blueprint | Implementasi |
| --- | --- |
| Atribut private `__id`, `__nama`, `__no_hp`, `__riwayat_belanja` | `pelanggan.py` |
| Property read-only | `id`, `nama`, `no_hp`, `jenis`, `riwayat_belanja` |
| Riwayat tidak bisa diubah dari luar | Property mengembalikan salinan list |
| `tambah_riwayat()`, `lihat_riwayat()` | Tersedia |
| `diskon()` polymorphic | Reguler 0%, Member 10% |
| Daftar pelanggan `{id: objek}` | `DaftarPelanggan` |
| Fungsi `cari_pelanggan(id)` | Method `DaftarPelanggan.cari_pelanggan()` dan fungsi modul `cari_pelanggan()` |
| Exception | `PelangganTidakTerdaftarError`, `DataPelangganTidakValidError` |

**Keputusan desain:** ID pelanggan dinormalisasi menjadi huruf besar agar pencarian konsisten. Nomor HP divalidasi minimal 8 digit dan hanya boleh berisi angka, spasi, `+`, atau `-`.

### 2.3 Anggota C — `Transaksi`

**Tanggung jawab:** mencatat item yang dibeli, menghitung subtotal/diskon/total, dan mengurangi stok secara aman.

| Kebutuhan blueprint | Implementasi |
| --- | --- |
| Atribut private `__id_transaksi`, `__pelanggan`, `__item`, `__tanggal` | `transaksi.py` |
| Item berupa `(produk, jumlah)` | List `self.__item` |
| `tambah_item()` | Validasi produk dan jumlah |
| `hitung_subtotal()`, `hitung_diskon()`, `hitung_total()` | Tersedia |
| `proses()` | Memeriksa seluruh stok, baru mengurangi stok |
| Exception | `StokHabisError`, `JumlahTidakValidError`, `TransaksiTidakValidError` |
| Komposisi | Memakai `ProdukBatik` dan `Pelanggan` |

**Keputusan desain:** kebutuhan stok digabung per kode produk. Jika produk yang sama ditambahkan dua kali, total kebutuhannya yang dicek. Ini mencegah kasus stok 4, lalu dua item masing-masing 3 dan 2 lolos karena dicek terpisah. Stok baru dikurangi setelah semua item dinyatakan aman, sehingga transaksi gagal tidak mengubah data apa pun.

### 2.4 Anggota D — `Laporan`

**Tanggung jawab:** menyimpan transaksi yang sudah diproses dan menyusun rekap.

| Kebutuhan blueprint | Implementasi |
| --- | --- |
| Atribut private `__daftar_transaksi`, `__rekap_produk` | `laporan.py` |
| `tambah_transaksi()` | Hanya menerima transaksi yang sudah diproses |
| `total_pendapatan()` | Menjumlahkan total semua transaksi |
| `produk_terlaris()` | Berdasarkan dict rekap produk |
| `rekap_per_pelanggan()` | Dict `{id: {nama, jenis, jumlah_transaksi, total_belanja}}` |
| `cetak_struk()` | Teks struk siap cetak |
| `cetak_ringkasan()` | Teks laporan lengkap |
| Collection | List transaksi + dict rekap |
| Exception | `LaporanKosongError`, `TransaksiTidakValidError` |

**Keputusan desain:** rekap produk dan pelanggan diperbarui saat transaksi ditambahkan, bukan dihitung ulang setiap kali laporan diminta. Ini memperlihatkan penggunaan collection secara nyata dan menjaga laporan tetap cepat.

### 2.5 Custom Exception Bersama

Seluruh exception mewarisi `TokoBatikError`:

```text
TokoBatikError
├── DataProdukTidakValidError
├── DataPelangganTidakValidError
├── PelangganTidakTerdaftarError
├── StokHabisError
├── JumlahTidakValidError
├── TransaksiTidakValidError
└── LaporanKosongError
```

Dengan satu induk, `main.py` dan `app.py` cukup menangkap `TokoBatikError` untuk menangani seluruh kesalahan logika toko.

---

## 3. Analisis Alur Integrasi

Blueprint menetapkan alur:

```text
pilih pelanggan
  → cek PelangganTidakTerdaftarError
pilih produk + jumlah
  → cek StokHabisError / JumlahTidakValidError
proses()
  → hitung subtotal, diskon, total
  → kurangi stok
cetak struk
simpan ke riwayat pelanggan
simpan ke laporan
```

Implementasi memindahkan orkestrasi ini ke `toko.py`:

```text
TokoBatik.buat_transaksi(id_pelanggan, items)
  ├── cari_pelanggan()
  ├── Transaksi(...)
  ├── tambah_item() untuk setiap item
  ├── proses()  ← validasi stok + kurangi stok
  ├── laporan.tambah_transaksi()
  └── pelanggan.tambah_riwayat()
```

Dengan cara ini, `main.py` (CLI) dan `app.py` (website) memakai alur yang persis sama. Tidak ada logika bisnis yang diduplikasi di front-end.

---

## 4. Analisis Kebutuhan Website

Blueprint awalnya menetapkan aplikasi konsol. Permintaan pengembangan website diselesaikan tanpa melanggar ketentuan PBO:

- **Logika bisnis tetap di class Python.** Flask hanya menyediakan halaman, JSON API, dan validasi bentuk input.
- **Website menyediakan dua gaya penggunaan:**
  1. Dasbor dan form visual untuk pengguna umum.
  2. Halaman **Konsol** yang meniru terminal dan menjalankan perintah teks melalui `console.py`.
- **Data disimpan di memori** agar demo mudah dijalankan tanpa database. Tombol **Reset Data** mengembalikan data demo.
- **Semua transaksi tetap melewati `Transaksi.proses()`**, sehingga jaminan stok dan diskon sama dengan versi CLI.

### Arsitektur Website

```text
Browser
  ├── HTML/CSS/JS  (templates/index.html, static/)
  │      ├── form produk/pelanggan/transaksi
  │      ├── tabel & laporan
  │      └── terminal konsol
  │
  └── REST API (app.py)
         └── TokoBatik (toko.py)
                ├── ProdukBatik
                ├── Pelanggan
                ├── Transaksi
                └── Laporan
```

### Endpoint Utama

- `GET /api/dashboard`
- `GET|POST /api/produk`
- `GET|POST /api/pelanggan`
- `GET|POST /api/transaksi`
- `GET /api/transaksi/<id>/struk`
- `GET /api/laporan`
- `POST /api/console`
- `POST /api/reset`

---

## 5. Analisis Pengujian

| Class | Test yang ditulis | File |
| --- | --- | --- |
| ProdukBatik | Objek valid, harga ≤ 0, stok negatif, kode/nama kosong, harga jual tiap subclass, kurangi/tambah stok, setter | `test_produk_batik.py` |
| Pelanggan | Diskon 0% dan 10%, riwayat read-only, data tidak valid, ID duplikat, pencarian | `test_pelanggan.py` |
| Transaksi | Total tanpa/dengan diskon, stok habis, stok tidak berubah saat gagal, item duplikat, proses ganda | `test_transaksi.py` |
| Laporan | Laporan kosong, pendapatan, produk terlaris, rekap pelanggan, struk, ringkasan | `test_laporan.py` |
| Integrasi | Alur service lengkap, reset, perintah konsol | `test_integrasi.py` |
| Website | Halaman utama, API produk/pelanggan/transaksi, validasi, konsol, reset | `test_web.py` |

Perintah:

```bash
python -m unittest discover tests -v
```

Hasil saat ini: **53 test lulus**.

---

## 6. Checklist Blueprint

- [x] Setiap class utama hanya dipegang satu orang (pembagian terdokumentasi).
- [x] Atribut private dengan `@property`.
- [x] Inheritance terlihat pada produk dan pelanggan.
- [x] Polymorphism terlihat pada `harga_jual()` dan `diskon()`.
- [x] Minimal satu custom exception pada class relevan.
- [x] Seluruh unit test lulus.
- [x] `main.py` berjalan tanpa error.
- [x] Integrasi website memakai class yang sama.
- [ ] Logbook tiap anggota dan video presentasi (dokumen terpisah, bukan bagian kode).

---

## 7. Catatan Pengembangan Lanjutan

Jika proyek ingin dikembangkan:

1. Tambahkan penyimpanan permanen (SQLite/JSON) agar data tidak hilang saat server restart.
2. Tambahkan autentikasi admin untuk halaman produk dan laporan.
3. Tambahkan fitur edit/hapus produk dan pelanggan.
4. Tambahkan ekspor laporan ke PDF/Excel.
5. Tambahkan test end-to-end browser (Playwright/Selenium) untuk alur form.

# Toko Batik Rofi

Sistem Penjualan Batik berbasis Python yang menyediakan **dua antarmuka**:

1. **Konsol (CLI)** — `python main.py`, sesuai blueprint Tugas Besar PBO.
2. **Website (Flask)** — `python app.py`, antarmuka modern yang memakai logika class Python yang sama, lengkap dengan terminal interaktif di dalam browser.

Blueprint Tugas Besar PBO (INF2516) dijadikan acuan pembagian class, konsep PBO, custom exception, collection, dan unit test. Analisis lengkap ada di [`docs/analisis_blueprint.md`](docs/analisis_blueprint.md). Pratinjau tampilan website ada di [`docs/preview-dasbor.png`](docs/preview-dasbor.png).

---

## Fitur

- Daftar produk batik dengan tiga jenis: **BatikTulis**, **BatikCap**, dan **BatikPrint**.
- Harga jual otomatis: tulis ×1,5, cap ×1,2, print ×1,0 dari harga dasar.
- Validasi harga, stok, kode, nama, dan nomor HP.
- Pelanggan **reguler** (diskon 0%) dan **member** (diskon 10%).
- Transaksi multi-item dengan pemeriksaan stok menyeluruh sebelum stok dikurangi.
- Riwayat belanja per pelanggan.
- Laporan penjualan: total pendapatan, produk terlaris, rekap per produk, dan rekap per pelanggan.
- Struk transaksi siap cetak.
- Website: dasbor, tabel produk/pelanggan/transaksi, form transaksi, laporan, dan konsol interaktif.

---

## Struktur Folder

```text
toko_batik_rofi/
├── produk_batik.py        # ProdukBatik + BatikTulis/BatikCap/BatikPrint
├── pelanggan.py           # Pelanggan + PelangganReguler/PelangganMember
├── transaksi.py           # Transaksi
├── laporan.py             # Laporan
├── exceptions.py          # custom exception bersama
├── utils.py               # format rupiah
├── toko.py                # service integrasi seluruh class
├── console.py             # parser perintah untuk konsol website
├── main.py                # antarmuka konsol (CLI)
├── app.py                 # website Flask + REST API
├── templates/index.html   # halaman website
├── static/css/style.css   # tema visual
├── static/js/app.js       # interaksi website
├── tests/                 # unit test unittest
├── docs/                  # analisis blueprint
├── requirements.txt
└── README.md
```

---

## Menjalankan Versi Konsol

```bash
cd toko_batik_rofi
python main.py
```

Menu yang tersedia:

1. Lihat daftar produk
2. Tambah produk
3. Daftarkan pelanggan
4. Lihat daftar pelanggan
5. Buat transaksi
6. Lihat riwayat pelanggan
7. Cetak laporan penjualan
8. Keluar

Data demo otomatis dimuat saat program dijalankan.

---

## Menjalankan Website

```bash
cd toko_batik_rofi
python -m pip install -r requirements.txt
python app.py
```

Buka **http://127.0.0.1:5000**.

Halaman website:

- **Dasbor** — ringkasan pendapatan, transaksi, pelanggan, produk terlaris, stok menipis, dan transaksi terbaru.
- **Produk** — daftar produk dan form tambah produk.
- **Pelanggan** — daftar pelanggan dan form pendaftaran.
- **Transaksi** — kasir multi-item dengan perhitungan diskon langsung dan struk.
- **Laporan** — rekap produk/pelanggan dan laporan teks siap cetak.
- **Konsol** — terminal interaktif yang menjalankan perintah yang sama dengan versi CLI.

### Perintah Konsol Website

```text
help
produk
pelanggan
transaksi
laporan
terlaris
riwayat <id_pelanggan>
struk <id_transaksi>
tambah-produk <tulis|cap|print> <kode> <harga> <stok> <nama...>
tambah-pelanggan <id> <reguler|member> <no_hp> <nama...>
beli <id_pelanggan> <kode> <jumlah> [<kode> <jumlah> ...]
tambah-stok <kode> <jumlah>
reset
clear
```

Contoh:

```text
beli C002 BP01 2
riwayat C002
tambah-produk tulis BT03 275000 6 Batik Tulis Sido Mukti
```

---

## Endpoint API Website

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| GET | `/api/dashboard` | Ringkasan dasbor |
| GET | `/api/produk` | Daftar produk |
| POST | `/api/produk` | Tambah produk |
| GET | `/api/pelanggan` | Daftar pelanggan |
| POST | `/api/pelanggan` | Daftar pelanggan baru |
| GET | `/api/transaksi` | Riwayat transaksi |
| POST | `/api/transaksi` | Proses transaksi baru |
| GET | `/api/transaksi/<id>/struk` | Teks struk |
| GET | `/api/laporan` | Data laporan |
| POST | `/api/console` | Jalankan perintah konsol |
| POST | `/api/reset` | Kembalikan data demo |

Contoh body transaksi:

```json
{
  "id_pelanggan": "C001",
  "items": [
    { "kode": "BT01", "jumlah": 2 },
    { "kode": "BC01", "jumlah": 1 }
  ]
}
```

---

## Menjalankan Unit Test

```bash
cd toko_batik_rofi
python -m unittest discover tests -v
```

Cakupan test:

- `test_produk_batik.py` — validasi, enkapsulasi, harga jual polymorphism, stok.
- `test_pelanggan.py` — diskon, riwayat read-only, pencarian, ID duplikat.
- `test_transaksi.py` — total, diskon, stok gagal tidak mengubah data, item duplikat.
- `test_laporan.py` — laporan kosong, pendapatan, produk terlaris, rekap, struk.
- `test_integrasi.py` — alur service dan perintah konsol.
- `test_web.py` — smoke test halaman dan API Flask.

---

## Penerapan Konsep PBO

| Konsep | Implementasi |
| --- | --- |
| **Encapsulation** | Atribut private (`__kode`, `__stok`, `__riwayat_belanja`, dll.) dengan `@property` dan setter tervalidasi. |
| **Inheritance** | `BatikTulis/BatikCap/BatikPrint` mewarisi `ProdukBatik`; `PelangganReguler/PelangganMember` mewarisi `Pelanggan`. |
| **Polymorphism** | `harga_jual()` dan `diskon()` di-override oleh subclass. |
| **Custom Exception** | `TokoBatikError` sebagai induk, lalu `DataProdukTidakValidError`, `PelangganTidakTerdaftarError`, `StokHabisError`, `JumlahTidakValidError`, `LaporanKosongError`, dll. |
| **Collection** | `list` untuk item transaksi/riwayat, `dict` untuk daftar pelanggan, rekap produk, dan rekap pelanggan. |
| **Komposisi** | `Transaksi` memiliki `Pelanggan` dan daftar `ProdukBatik`; `Laporan` menyimpan daftar `Transaksi`. |
| **Unit Test** | 53 test `unittest` di folder `tests/`. |

---

## Catatan

- Data website disimpan di memori server, sama seperti versi CLI. Restart server atau tekan **Reset Data** untuk kembali ke data demo.
- Website memakai Flask hanya sebagai lapisan presentasi/API. Seluruh aturan bisnis tetap berada di class Python agar ketentuan blueprint tetap terpenuhi.

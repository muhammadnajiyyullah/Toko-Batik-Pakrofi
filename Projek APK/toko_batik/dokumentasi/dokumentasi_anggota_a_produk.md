# Dokumentasi Class `ProdukBatik` — Anggota A

| | |
|---|---|
| Mata Kuliah | Pemrograman Berorientasi Objek (INF2516) — Semester 3 |
| Proyek | Tugas Besar — Sistem Kasir Toko Batik |
| Class Utama | `ProdukBatik` (`produk.py`) |
| Peran Saya | Developer, Tester, dan Dokumentator class ini |

---

## 1. Deskripsi dan Fungsi Utama

Class `ProdukBatik` merepresentasikan **produk batik yang dijual di toko**. Class ini menjadi sumber data tunggal untuk informasi produk: identitas (ID otomatis), nama, motif, jenis, ukuran, harga, dan stok. Setiap perubahan harga/stok **selalu tervalidasi** sebelum disimpan sehingga objek produk tidak pernah berada dalam kondisi tidak valid (harga nol, stok negatif, dsb.).

Class ini dipanggil oleh class `Transaksi` (Anggota C) melalui method `kurangi_stok()` setiap kali terjadi pembelian, dan dibaca oleh class `Laporan` (Anggota D) untuk keperluan cetak struk serta rekap penjualan.

## 2. Rancangan Atribut (Encapsulation)

Seluruh atribut bersifat **private** (name mangling `__`) dan hanya diakses melalui `@property` / setter yang memvalidasi nilai.

| Atribut | Tipe | Akses | Deskripsi |
|---|---|---|---|
| `__id_produk` | `str` | private, read-only | ID unik otomatis berformat `BT-001`, `BT-002`, … (dari atribut class `_jumlah_produk`) |
| `__nama` | `str` | private | Nama produk, tidak boleh kosong |
| `__motif` | `str` | private | Motif batik (Parang, Mega Mendung, Kawung, …) |
| `__jenis` | `str` | private | Salah satu dari konstanta `JENIS_VALID` = ("Kain Batik", "Pakaian Jadi", "Aksesori") |
| `__ukuran` | `str` | private | Ukuran produk (2 meter / L / M / All size) |
| `__harga` | `int` | private | Harga dalam Rupiah, harus angka > 0 |
| `__stok` | `int` | private | Jumlah stok, bilangan bulat ≥ 0 |
| `_jumlah_produk` | `int` | class attribute | Penghitung objek untuk pembuatan ID otomatis |

## 3. Rancangan Method

| Method | Deskripsi | Exception yang Mungkin Terjadi |
|---|---|---|
| `__init__(nama, motif, jenis, ukuran, harga, stok)` | Konstruktor; semua nilai divalidasi lewat setter | `HargaTidakValidException`, `StokTidakValidException`, `ValueError` |
| `id_produk`, `nama`, `motif`, `jenis`, `ukuran`, `harga`, `stok` (property) | Getter semua atribut | — |
| `nama`, `motif`, `jenis`, `ukuran`, `harga`, `stok` (setter) | Setter dengan validasi masing-masing | sesuai kolom validasi |
| `tambah_stok(jumlah)` | Menambah stok (restock); jumlah harus bilangan bulat > 0 | `StokTidakValidException` |
| `kurangi_stok(jumlah)` | Mengurangi stok saat pembelian; dipanggil class `Transaksi` | `StokTidakValidException` |
| `tampilkan_info()` | Mengembalikan string ringkasan produk | — |
| `__str__()` | Representasi string objek | — |

## 4. Custom Exception

| Exception | Dipicu Ketika |
|---|---|
| `HargaTidakValidException` | Harga ≤ 0 atau bukan angka (setter/konstruktor) |
| `StokTidakValidException` | Stok < 0, atau jumlah tambah/kurang ≤ 0 / bukan bilangan bulat, atau pengurangan melebihi sisa stok |

## 5. Penerapan Encapsulation

1. **Atribut private** `__nama`, `__harga`, dll. — tidak dapat diakses/diubah langsung dari luar class.
2. **Validasi di setter** — setiap penulisan `self.harga = nilai` (termasuk dari konstruktor) otomatis melewati validasi.
3. **Read-only** — `id_produk` hanya punya getter (ID tidak boleh diubah).
4. **Konstanta class** `JENIS_VALID` membatasi nilai jenis produk.

## 6. Unit Test

File `test_produk.py` — 19 test case (9 positive, 10 negative), semuanya **lulus (green)**:
- Positive: ID otomatis, getter nilai awal, setter valid, tambah/kurangi stok, `tampilkan_info()`, `__str__`.
- Negative: harga 0/negatif/teks, stok negatif, kurangi stok melebihi sisa (stok tetap tidak berubah), nama kosong, jenis tidak dikenal.

## 7. Contoh Penggunaan

```python
from produk import ProdukBatik, HargaTidakValidException

kain = ProdukBatik("Kain Batik Parang", "Parang", "Kain Batik",
                   "2 meter", 350_000, 10)
print(kain.tampilkan_info())   # [BT-001] Kain Batik Parang | ...
kain.kurangi_stok(2)           # stok menjadi 8 (dipanggil Transaksi)
try:
    kain.harga = 0             # validasi menolak
except HargaTidakValidException as e:
    print(e)
```

## 8. Logbook Individu

| Pertemuan | Aktivitas (coding, testing, bug fixing) | Output | Paraf Ketua |
|---|---|---|---|
| Pert. 11 | Desain UML class `ProdukBatik`: menentukan atribut private & method validasi harga/stok | File gambar UML draft | (ttd) |
| Pert. 12 | Coding skeleton class `ProdukBatik` (atribut private, kerangka getter/setter) | `produk.py` (skeleton) | (ttd) |
| Pert. 13 | Menambah Custom Exception (`HargaTidakValidException`, `StokTidakValidException`) + method validasi | `produk.py` v0.3 | (ttd) |
| Pert. 14 | Membuat & menjalankan unit test (`test_produk.py`): 19 test positive & negative — **semua lulus (green)**, screenshot hasil test | `test_produk.py` + screenshot | (ttd) |
| Pert. 15 | Integrasi dengan `main.py` (stok produk berkurang saat transaksi), perbaikan kecil format `tampilkan_info()`, finalisasi dokumentasi | Source code utuh (ZIP) + laporan | (ttd) |

"""
=====================================================================
 TUGAS BESAR PBO  |  SISTEM KASIR TOKO BATIK
 Modul : produk.py
 Class : ProdukBatik  ->  CLASS UTAMA ANGGOTA A
=====================================================================
 Mengelola data produk batik yang dijual: nama, motif, jenis,
 ukuran, harga, dan stok.

 Custom Exception (didefinisikan di modul ini):
   1. HargaTidakValidException -> harga <= 0 atau bukan angka.
   2. StokTidakValidException  -> stok < 0 atau jumlah
      (tambah/kurang) tidak valid.

 Catatan integrasi:
   - Class Transaksi (Anggota C) memanggil kurangi_stok()
     pada class ini setiap kali item ditambahkan ke keranjang.
   - Class Laporan (Anggota D) membaca nama & harga produk
     melalui property daftar_item milik Transaksi.
=====================================================================
"""

from typing import Union


class HargaTidakValidException(Exception):
    """Custom Exception: harga produk tidak valid (<= 0 / bukan angka)."""

    def __init__(self, harga: Union[int, float, str]) -> None:
        # Pesan dibuat informatif agar mudah dipahami pengguna/kasir.
        super().__init__(
            f"Harga tidak valid: '{harga}'. Harga harus berupa angka > 0."
        )


class StokTidakValidException(Exception):
    """Custom Exception: nilai stok atau perubahan stok tidak valid."""

    def __init__(self, pesan: str) -> None:
        super().__init__(pesan)


class ProdukBatik:
    """
    Class ProdukBatik — CLASS UTAMA ANGGOTA A.

    Penerapan ENCAPSULATION:
      - Seluruh atribut instance bersifat PRIVATE (prefiks double
        underscore / name mangling), mis. self.__harga.
      - Akses dari luar class HANYA melalui @property (getter) dan
        @<atribut>.setter yang memvalidasi nilai sebelum disimpan.
      - id_produk bersifat READ-ONLY (tidak memiliki setter) karena
        dibuat otomatis oleh sistem.
    """

    # Atribut class: penghitung objek produk yang pernah dibuat,
    # dipakai untuk membuat ID produk otomatis (BT-001, BT-002, ...).
    _jumlah_produk = 0

    # Konstanta class: pilihan jenis produk yang diperbolehkan.
    JENIS_VALID = ("Kain Batik", "Pakaian Jadi", "Aksesori")

    def __init__(self, nama: str, motif: str, jenis: str,
                 ukuran: str, harga: Union[int, float], stok: int) -> None:
        """
        Konstruktor ProdukBatik.

        Seluruh nilai divalidasi melalui property setter sehingga
        objek tidak pernah berada pada kondisi tidak valid.
        """
        ProdukBatik._jumlah_produk += 1
        self.__id_produk = f"BT-{ProdukBatik._jumlah_produk:03d}"

        # Penulisan self.<atribut> = nilai secara OTOMATIS memanggil
        # setter (validasi) -- bukan mengisi atribut private langsung.
        self.nama = nama
        self.motif = motif
        self.jenis = jenis
        self.ukuran = ukuran
        self.harga = harga
        self.stok = stok

    # ------------------- GETTER / SETTER -------------------

    @property
    def id_produk(self) -> str:
        """Getter ID produk (read-only, dibuat otomatis oleh sistem)."""
        return self.__id_produk

    @property
    def nama(self) -> str:
        """Getter nama produk."""
        return self.__nama

    @nama.setter
    def nama(self, nilai: str) -> None:
        """Setter nama produk dengan validasi tidak boleh kosong."""
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Nama produk tidak boleh kosong.")
        self.__nama = nilai.strip()

    @property
    def motif(self) -> str:
        """Getter motif batik (Parang, Mega Mendung, dll)."""
        return self.__motif

    @motif.setter
    def motif(self, nilai: str) -> None:
        """Setter motif dengan validasi tidak boleh kosong."""
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Motif produk tidak boleh kosong.")
        self.__motif = nilai.strip()

    @property
    def jenis(self) -> str:
        """Getter jenis produk."""
        return self.__jenis

    @jenis.setter
    def jenis(self, nilai: str) -> None:
        """Setter jenis dengan validasi terhadap JENIS_VALID."""
        if not isinstance(nilai, str) or nilai.strip() not in self.JENIS_VALID:
            raise ValueError(
                f"Jenis produk '{nilai}' tidak valid. "
                f"Pilihan: {self.JENIS_VALID}."
            )
        self.__jenis = nilai.strip()

    @property
    def ukuran(self) -> str:
        """Getter ukuran produk (mis. 2 meter / L / M / All size)."""
        return self.__ukuran

    @ukuran.setter
    def ukuran(self, nilai: str) -> None:
        """Setter ukuran dengan validasi tidak boleh kosong."""
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Ukuran produk tidak boleh kosong.")
        self.__ukuran = nilai.strip()

    @property
    def harga(self) -> int:
        """Getter harga produk (dalam Rupiah)."""
        return self.__harga

    @harga.setter
    def harga(self, nilai: Union[int, float]) -> None:
        """Setter harga + validasi: harus angka dan > 0."""
        # isinstance(bool) dicek lebih dulu karena bool adalah subkelas int.
        if isinstance(nilai, bool) or not isinstance(nilai, (int, float)) or nilai <= 0:
            raise HargaTidakValidException(nilai)
        self.__harga = int(nilai)

    @property
    def stok(self) -> int:
        """Getter jumlah stok yang tersedia."""
        return self.__stok

    @stok.setter
    def stok(self, nilai: int) -> None:
        """Setter stok + validasi: bilangan bulat dan >= 0."""
        if isinstance(nilai, bool) or not isinstance(nilai, int) or nilai < 0:
            raise StokTidakValidException(
                f"Stok tidak valid: '{nilai}'. Stok harus bilangan bulat >= 0."
            )
        self.__stok = nilai

    # ------------------- METHOD -------------------

    def tambah_stok(self, jumlah: int) -> None:
        """Menambah stok produk (mis. saat restock barang dari gudang)."""
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise StokTidakValidException(
                f"Jumlah penambahan stok tidak valid: '{jumlah}'. Harus bilangan bulat > 0."
            )
        self.stok = self.__stok + jumlah  # tetap melewati validasi setter

    def kurangi_stok(self, jumlah: int) -> None:
        """
        Mengurangi stok produk saat terjadi pembelian.

        Method ini dipanggil oleh class Transaksi (Anggota C)
        setiap kali sebuah item ditambahkan ke keranjang belanja.
        """
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise StokTidakValidException(
                f"Jumlah pengurangan stok tidak valid: '{jumlah}'. Harus bilangan bulat > 0."
            )
        if jumlah > self.__stok:
            raise StokTidakValidException(
                f"Stok '{self.__nama}' tidak mencukupi. "
                f"Tersisa {self.__stok}, diminta {jumlah}."
            )
        self.stok = self.__stok - jumlah  # tetap melewati validasi setter

    def tampilkan_info(self) -> str:
        """Mengembalikan ringkasan info produk dalam satu baris string."""
        return (
            f"[{self.__id_produk}] {self.__nama} | Motif: {self.__motif} | "
            f"{self.__jenis} ({self.__ukuran}) | Rp{self.__harga:,} | Stok: {self.__stok}"
        )

    def __str__(self) -> str:
        """Representasi string objek produk saat diprint."""
        return self.tampilkan_info()

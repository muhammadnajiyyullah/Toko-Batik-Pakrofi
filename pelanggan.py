"""Class pelanggan Toko Batik Rofi (Anggota B).

Menerapkan:
- Encapsulation : atribut private + @property read-only.
- Inheritance   : PelangganReguler dan PelangganMember mewarisi Pelanggan.
- Polymorphism  : diskon() di-override oleh setiap subclass.
- Collection    : DaftarPelanggan menyimpan objek dalam dict {id: objek}.
"""

from exceptions import (
    DataPelangganTidakValidError,
    PelangganTidakTerdaftarError,
)


class Pelanggan:
    """Data dasar seorang pelanggan toko batik."""

    def __init__(self, id_pelanggan, nama, no_hp):
        self.__id = ""
        self.__nama = ""
        self.__no_hp = ""
        self.__riwayat_belanja = []

        self.__id = self.__validasi_teks(id_pelanggan, "ID pelanggan").upper()
        self.__nama = self.__validasi_teks(nama, "Nama pelanggan")
        self.__no_hp = self.__validasi_no_hp(no_hp)

    # ------------------------------------------------------------------
    # Helper validasi internal
    # ------------------------------------------------------------------
    @staticmethod
    def __validasi_teks(nilai, label):
        if not isinstance(nilai, str) or not nilai.strip():
            raise DataPelangganTidakValidError(f"{label} tidak boleh kosong.")
        return nilai.strip()

    @staticmethod
    def __validasi_no_hp(nilai):
        if not isinstance(nilai, str) or not nilai.strip():
            raise DataPelangganTidakValidError("Nomor HP tidak boleh kosong.")

        nomor = nilai.strip()
        karakter_valid = set("0123456789+- ")
        if not all(karakter in karakter_valid for karakter in nomor):
            raise DataPelangganTidakValidError(
                "Nomor HP hanya boleh berisi angka, spasi, tanda +, atau -."
            )
        if sum(karakter.isdigit() for karakter in nomor) < 8:
            raise DataPelangganTidakValidError(
                "Nomor HP minimal berisi 8 digit angka."
            )
        return nomor

    # ------------------------------------------------------------------
    # Property read-only
    # ------------------------------------------------------------------
    @property
    def id(self):
        return self.__id

    @property
    def nama(self):
        return self.__nama

    @property
    def no_hp(self):
        return self.__no_hp

    @property
    def jenis(self):
        """Jenis pelanggan berdasarkan nama class, contoh: reguler, member."""
        jenis = type(self).__name__.replace("Pelanggan", "").lower()
        return jenis or "reguler"

    @property
    def riwayat_belanja(self):
        """Mengembalikan salinan list agar riwayat tidak bisa diubah dari luar."""
        return list(self.__riwayat_belanja)

    # ------------------------------------------------------------------
    # Method utama
    # ------------------------------------------------------------------
    def diskon(self):
        """Diskon dasar; subclass meng-override method ini."""
        return 0.0

    def tambah_riwayat(self, transaksi):
        """Menyimpan transaksi ke riwayat belanja pelanggan."""
        if transaksi is None or not hasattr(transaksi, "id_transaksi"):
            raise DataPelangganTidakValidError(
                "Transaksi yang disimpan ke riwayat tidak valid."
            )
        self.__riwayat_belanja.append(transaksi)
        return len(self.__riwayat_belanja)

    def lihat_riwayat(self):
        """Mengembalikan salinan riwayat belanja pelanggan."""
        return list(self.__riwayat_belanja)

    def info(self):
        """Ringkasan pelanggan dalam satu baris."""
        persen = self.diskon() * 100
        teks_diskon = f"{persen:.0f}%"
        return (
            f"[{self.__id}] {self.__nama} ({type(self).__name__}) | "
            f"HP: {self.__no_hp} | Diskon: {teks_diskon} | "
            f"Transaksi: {len(self.__riwayat_belanja)}"
        )


class PelangganReguler(Pelanggan):
    """Pelanggan reguler tidak mendapat diskon."""

    def diskon(self):
        return 0.0


class PelangganMember(Pelanggan):
    """Pelanggan member mendapat diskon 10%."""

    def diskon(self):
        return 0.10


class DaftarPelanggan:
    """Koleksi pelanggan yang disimpan dalam dict {id: objek}."""

    def __init__(self):
        self.__data = {}

    def tambah(self, pelanggan):
        if not isinstance(pelanggan, Pelanggan):
            raise DataPelangganTidakValidError(
                "Objek yang ditambahkan bukan Pelanggan."
            )
        if pelanggan.id in self.__data:
            raise DataPelangganTidakValidError(
                f"Pelanggan dengan ID '{pelanggan.id}' sudah terdaftar."
            )
        self.__data[pelanggan.id] = pelanggan
        return pelanggan

    def cari_pelanggan(self, id_pelanggan):
        kunci = str(id_pelanggan).strip().upper()
        if kunci not in self.__data:
            raise PelangganTidakTerdaftarError(
                f"Pelanggan dengan ID '{id_pelanggan}' tidak terdaftar."
            )
        return self.__data[kunci]

    def semua(self):
        return list(self.__data.values())

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data.values())

    def __contains__(self, id_pelanggan):
        return str(id_pelanggan).strip().upper() in self.__data


def cari_pelanggan(daftar, id_pelanggan):
    """Mencari pelanggan dari DaftarPelanggan atau dict {id: objek}."""
    if isinstance(daftar, DaftarPelanggan):
        return daftar.cari_pelanggan(id_pelanggan)

    kunci = str(id_pelanggan).strip().upper()
    try:
        return daftar[kunci]
    except (KeyError, TypeError):
        raise PelangganTidakTerdaftarError(
            f"Pelanggan dengan ID '{id_pelanggan}' tidak terdaftar."
        )

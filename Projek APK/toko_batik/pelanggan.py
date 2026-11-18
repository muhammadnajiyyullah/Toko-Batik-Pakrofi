"""
=====================================================================
 TUGAS BESAR PBO  |  SISTEM KASIR TOKO BATIK
 Modul : pelanggan.py
 Class : Pelanggan  ->  CLASS UTAMA ANGGOTA B
=====================================================================
 Mengelola data pelanggan toko: identitas dan riwayat belanja.

 Custom Exception (didefinisikan di modul ini):
   1. PelangganTidakTerdaftarException -> ID pelanggan tidak ada
      di daftar pelanggan (dipakai saat akan bertransaksi).
   2. NomorTeleponTidakValidException  -> nomor telepon tidak
      sesuai format (10-13 digit angka).

 Collection yang digunakan:
   - List  : __riwayat_belanja, kumpulan ringkasan transaksi
             milik pelanggan (tiap elemen berupa Dict).

 Catatan integrasi:
   - main.py memanggil cari_pelanggan() sebelum membuat Transaksi.
   - Class Transaksi (Anggota C) menyimpan objek Pelanggan ini.
   - Setelah transaksi selesai, main.py menambahkan ringkasan
     transaksi lewat tambah_riwayat().
=====================================================================
"""

from typing import Dict, List


class PelangganTidakTerdaftarException(Exception):
    """Custom Exception: pelanggan tidak terdaftar di sistem."""

    def __init__(self, id_pelanggan: str) -> None:
        super().__init__(f"Pelanggan dengan ID '{id_pelanggan}' tidak terdaftar.")
        self.id_pelanggan = id_pelanggan  # data ID disimpan utk penelusuran


class NomorTeleponTidakValidException(Exception):
    """Custom Exception: format nomor telepon tidak valid."""

    def __init__(self, no_telepon: str) -> None:
        super().__init__(
            f"No. telepon '{no_telepon}' tidak valid. Harus 10-13 digit angka."
        )


class Pelanggan:
    """
    Class Pelanggan — CLASS UTAMA ANGGOTA B.

    Penerapan ENCAPSULATION:
      - Seluruh atribut instance bersifat PRIVATE (name mangling).
      - Getter/setter memvalidasi data: nama wajib diisi, no. telepon
        harus 10-13 digit angka, email harus berformat benar.
      - __riwayat_belanja tidak boleh diubah langsung dari luar;
        penambahan hanya lewat tambah_riwayat() dan getter
        mengembalikan SALINAN list (mencegah manipulasi data).
    """

    # Atribut class: penghitung objek pelanggan -> ID otomatis PLG-001, ...
    _jumlah_pelanggan = 0

    def __init__(self, nama: str, no_telepon: str, email: str = "-") -> None:
        """
        Konstruktor Pelanggan.

        Nilai divalidasi lewat property setter; email bersifat
        opsional (default "-") jika pelanggan tidak memiliki email.
        """
        Pelanggan._jumlah_pelanggan += 1
        self.__id_pelanggan = f"PLG-{Pelanggan._jumlah_pelanggan:03d}"

        self.nama = nama
        self.no_telepon = no_telepon
        self.email = email
        # Collection: list riwayat belanja (diisi ringkasan transaksi).
        self.__riwayat_belanja: List[Dict] = []

    # ------------------- GETTER / SETTER -------------------

    @property
    def id_pelanggan(self) -> str:
        """Getter ID pelanggan (read-only, dibuat otomatis)."""
        return self.__id_pelanggan

    @property
    def nama(self) -> str:
        """Getter nama pelanggan."""
        return self.__nama

    @nama.setter
    def nama(self, nilai: str) -> None:
        """Setter nama dengan validasi tidak boleh kosong."""
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Nama pelanggan tidak boleh kosong.")
        self.__nama = nilai.strip()

    @property
    def no_telepon(self) -> str:
        """Getter nomor telepon pelanggan."""
        return self.__no_telepon

    @no_telepon.setter
    def no_telepon(self, nilai: str) -> None:
        """Setter no. telepon + validasi: 10-13 digit angka."""
        bersih = str(nilai).strip() if nilai is not None else ""
        if not bersih.isdigit() or not (10 <= len(bersih) <= 13):
            raise NomorTeleponTidakValidException(bersih)
        self.__no_telepon = bersih

    @property
    def email(self) -> str:
        """Getter email pelanggan ('-' jika tidak diisi)."""
        return self.__email

    @email.setter
    def email(self, nilai: str) -> None:
        """Setter email + validasi format sederhana (berisi @ dan .)."""
        nilai = "-" if nilai is None else str(nilai).strip()
        if nilai in ("", "-"):
            self.__email = "-"  # email opsional
            return
        if "@" not in nilai or "." not in nilai.split("@")[-1]:
            raise ValueError(f"Email '{nilai}' tidak valid.")
        self.__email = nilai

    @property
    def riwayat_belanja(self) -> List[Dict]:
        """Getter riwayat belanja (SALINAN list agar data asli aman)."""
        return list(self.__riwayat_belanja)

    # ------------------- METHOD -------------------

    def tambah_riwayat(self, ringkasan: Dict) -> None:
        """
        Menambah ringkasan transaksi ke riwayat belanja pelanggan.

        Parameter ringkasan adalah Dict hasil Transaksi.proses_transaksi()
        yang minimal berisi key 'id_transaksi' dan 'total'.
        """
        if not isinstance(ringkasan, dict):
            raise ValueError("Ringkasan transaksi harus berupa dictionary.")
        if "id_transaksi" not in ringkasan or "total" not in ringkasan:
            raise ValueError(
                "Ringkasan transaksi wajib memiliki key 'id_transaksi' dan 'total'."
            )
        if ringkasan["total"] < 0:
            raise ValueError("Total belanja tidak boleh negatif.")
        # dict(ringkasan) -> disimpan sebagai salinan agar data aman.
        self.__riwayat_belanja.append(dict(ringkasan))

    def total_belanja(self) -> int:
        """Menjumlahkan seluruh total belanja pelanggan dari riwayat."""
        return sum(r["total"] for r in self.__riwayat_belanja)

    def tampilkan_riwayat(self) -> str:
        """Mengembalikan string riwayat belanja untuk ditampilkan di layar."""
        if not self.__riwayat_belanja:
            return f"{self.__nama} ({self.__id_pelanggan}) belum memiliki riwayat belanja."
        baris = [f"Riwayat belanja {self.__nama} ({self.__id_pelanggan}):"]
        for r in self.__riwayat_belanja:
            jumlah_item = len(r.get("item", []))
            baris.append(
                f"  - {r['id_transaksi']} | {r.get('tanggal', '-')} | "
                f"Rp{r['total']:,} | {jumlah_item} jenis item"
            )
        return "\n".join(baris)

    @staticmethod
    def cari_pelanggan(daftar_pelanggan: Dict[str, "Pelanggan"],
                        id_pelanggan: str) -> "Pelanggan":
        """
        Mencari pelanggan berdasarkan ID pada dictionary pelanggan.

        Mengembalikan objek Pelanggan jika ditemukan; jika tidak,
        melempar PelangganTidakTerdaftarException (dipakai main.py
        dan saat membuat Transaksi).
        """
        if not isinstance(daftar_pelanggan, dict):
            raise ValueError("Daftar pelanggan harus berupa dictionary {id: Pelanggan}.")
        id_cari = str(id_pelanggan).strip().upper()
        if id_cari not in daftar_pelanggan:
            raise PelangganTidakTerdaftarException(id_cari)
        return daftar_pelanggan[id_cari]

    def __str__(self) -> str:
        """Representasi string objek pelanggan saat diprint."""
        return f"[{self.__id_pelanggan}] {self.__nama} | {self.__no_telepon} | {self.__email}"

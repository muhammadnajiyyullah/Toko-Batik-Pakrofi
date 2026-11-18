"""Fungsi bantu kecil yang dipakai bersama oleh beberapa class."""


def format_rupiah(nilai):
    """Mengubah angka menjadi format rupiah, contoh: 150000 -> Rp150.000."""
    if nilai is None:
        return "-"
    return "Rp{:,.0f}".format(nilai).replace(",", ".")

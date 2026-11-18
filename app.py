"""Website Toko Batik Rofi berbasis Flask.

Logika bisnis tetap berada di class Python (produk_batik.py, pelanggan.py,
transaksi.py, laporan.py, dan toko.py). File ini hanya menjadi jembatan
antara website dan class-class tersebut.

Jalankan:
    python app.py
Lalu buka http://127.0.0.1:5000
"""

from threading import RLock

from flask import Flask, jsonify, render_template, request

from console import KonsolToko
from exceptions import TokoBatikError
from toko import TokoBatik

app = Flask(__name__)
toko = TokoBatik()
konsol = KonsolToko(toko)
kunci = RLock()


# ----------------------------------------------------------------------
# Helper response
# ----------------------------------------------------------------------
def sukses(data=None, pesan=None, status=200):
    body = {"ok": True}
    if data is not None:
        body["data"] = data
    if pesan:
        body["pesan"] = pesan
    return jsonify(body), status


def gagal(pesan, status=400):
    return jsonify({"ok": False, "error": pesan}), status


def ambil_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Body JSON tidak valid.")
    return data


def ambil_int(data, kunci_data, label):
    try:
        return int(data[kunci_data])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{label} harus berupa angka bulat.")


# ----------------------------------------------------------------------
# Error handler
# ----------------------------------------------------------------------
@app.errorhandler(TokoBatikError)
def tangani_toko_error(error):
    return gagal(str(error), 400)


@app.errorhandler(ValueError)
def tangani_value_error(error):
    return gagal(f"Input tidak valid: {error}", 400)


@app.errorhandler(404)
def tangani_404(_error):
    if request.path.startswith("/api/"):
        return gagal("Endpoint tidak ditemukan.", 404)
    return render_template("index.html"), 404


# ----------------------------------------------------------------------
# Halaman
# ----------------------------------------------------------------------
@app.get("/")
def index():
    return render_template("index.html")


# ----------------------------------------------------------------------
# API dashboard
# ----------------------------------------------------------------------
@app.get("/api/dashboard")
def api_dashboard():
    with kunci:
        return sukses(toko.dashboard_data())


# ----------------------------------------------------------------------
# API produk
# ----------------------------------------------------------------------
@app.get("/api/produk")
def api_produk():
    with kunci:
        return sukses(toko.produk_data())


@app.post("/api/produk")
def api_tambah_produk():
    data = ambil_json()
    with kunci:
        produk = toko.tambah_produk(
            data.get("jenis", ""),
            data.get("kode", ""),
            data.get("nama", ""),
            ambil_int(data, "harga_dasar", "Harga dasar"),
            ambil_int(data, "stok", "Stok"),
        )
        return sukses(
            toko.produk_ke_dict(produk),
            "Produk berhasil ditambahkan.",
            201,
        )


# ----------------------------------------------------------------------
# API pelanggan
# ----------------------------------------------------------------------
@app.get("/api/pelanggan")
def api_pelanggan():
    with kunci:
        return sukses(toko.pelanggan_data())


@app.post("/api/pelanggan")
def api_tambah_pelanggan():
    data = ambil_json()
    with kunci:
        pelanggan = toko.tambah_pelanggan(
            data.get("id", ""),
            data.get("nama", ""),
            data.get("no_hp", ""),
            data.get("tipe", "reguler"),
        )
        rekap = toko.laporan.rekap_per_pelanggan().get(pelanggan.id, {})
        return sukses(
            toko.pelanggan_ke_dict(pelanggan, rekap),
            "Pelanggan berhasil didaftarkan.",
            201,
        )


# ----------------------------------------------------------------------
# API transaksi
# ----------------------------------------------------------------------
@app.get("/api/transaksi")
def api_transaksi():
    with kunci:
        return sukses(toko.transaksi_data())


@app.post("/api/transaksi")
def api_buat_transaksi():
    data = ambil_json()
    items_raw = data.get("items")
    if not isinstance(items_raw, list) or not items_raw:
        raise ValueError("Transaksi minimal memiliki satu item.")

    items = []
    for item in items_raw:
        if not isinstance(item, dict):
            raise ValueError("Format item transaksi tidak valid.")
        items.append(
            (
                item.get("kode", ""),
                ambil_int(item, "jumlah", "Jumlah"),
            )
        )

    with kunci:
        transaksi = toko.buat_transaksi(
            data.get("id_pelanggan", ""), items
        )
        return sukses(
            {
                "transaksi": transaksi.to_dict(),
                "struk": toko.cetak_struk(transaksi.id_transaksi),
            },
            "Transaksi berhasil diproses.",
            201,
        )


@app.get("/api/transaksi/<id_transaksi>/struk")
def api_struk(id_transaksi):
    with kunci:
        return sukses({"struk": toko.cetak_struk(id_transaksi)})


# ----------------------------------------------------------------------
# API laporan
# ----------------------------------------------------------------------
@app.get("/api/laporan")
def api_laporan():
    with kunci:
        return sukses(toko.laporan_data())


# ----------------------------------------------------------------------
# API konsol
# ----------------------------------------------------------------------
@app.post("/api/console")
def api_console():
    data = ambil_json()
    perintah = data.get("command", "")
    with kunci:
        return sukses({"lines": konsol.jalankan(perintah)})


@app.post("/api/reset")
def api_reset():
    with kunci:
        toko.reset()
        return sukses(toko.dashboard_data(), "Data demo berhasil direset.")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

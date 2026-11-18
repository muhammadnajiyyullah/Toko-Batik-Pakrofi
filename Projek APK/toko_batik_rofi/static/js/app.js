/* =====================================================================
   Toko Batik Rofi — front-end website
   ===================================================================== */
"use strict";

const state = {
  dashboard: null,
  produk: [],
  pelanggan: [],
  transaksi: [],
  laporan: null,
  filterProduk: "",
  filterPelanggan: "",
  consoleHistory: [],
  consoleIndex: -1,
};

const pageMeta = {
  dashboard: { title: "Dasbor", eyebrow: "Ringkasan" },
  produk: { title: "Produk", eyebrow: "Inventaris" },
  pelanggan: { title: "Pelanggan", eyebrow: "CRM" },
  transaksi: { title: "Transaksi", eyebrow: "Kasir" },
  laporan: { title: "Laporan", eyebrow: "Analitik" },
  konsol: { title: "Konsol", eyebrow: "Terminal" },
};

const $ = (id) => document.getElementById(id);

/* ============================== Utilitas ============================== */
function rupiah(nilai) {
  const angka = Number(nilai || 0);
  return "Rp" + angka.toLocaleString("id-ID", { maximumFractionDigits: 0 });
}

function esc(nilai) {
  return String(nilai ?? "").replace(/[&<>"']/g, (karakter) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[karakter]));
}

function setText(id, teks) {
  const element = $(id);
  if (element) element.textContent = teks;
}

function emptyRow(colspan, teks) {
  return `<tr class="empty-row"><td colspan="${colspan}">${esc(teks)}</td></tr>`;
}

function jenisBadge(jenis) {
  const kelas = { tulis: "badge-gold", cap: "badge-teal", print: "badge-clay" }[jenis];
  return `<span class="badge ${kelas || "badge-muted"}">${esc(jenis)}</span>`;
}

function tipeBadge(jenis) {
  return `<span class="badge ${jenis === "member" ? "badge-gold" : "badge-muted"}">${esc(jenis)}</span>`;
}

function stokBadge(stok) {
  if (stok === 0) return `<span class="badge badge-danger">Habis</span>`;
  if (stok <= 5) return `<span class="badge badge-clay">${stok} · menipis</span>`;
  return `<span class="badge badge-success">${stok}</span>`;
}

async function api(path, options = {}) {
  const pengaturan = {
    headers: { "Content-Type": "application/json" },
    ...options,
  };
  if (options.body !== undefined) {
    pengaturan.body = JSON.stringify(options.body);
  }

  const respons = await fetch(path, pengaturan);
  const data = await respons.json().catch(() => ({}));
  if (!respons.ok || data.ok === false) {
    throw new Error(data.error || data.pesan || "Terjadi kesalahan pada server.");
  }
  return data.data;
}

let toastTimer = null;
function toast(pesan, tipe = "") {
  const element = $("toast");
  element.textContent = pesan;
  element.className = `toast show ${tipe}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    element.className = "toast";
  }, 3600);
}

/* ============================== Modal ============================== */
function showModal(judul, teks) {
  $("modalTitle").textContent = judul;
  $("modalBody").textContent = teks;
  $("modal").classList.add("open");
  $("modal").setAttribute("aria-hidden", "false");
}

function closeModal() {
  $("modal").classList.remove("open");
  $("modal").setAttribute("aria-hidden", "true");
}

function initModal() {
  $("modalClose").addEventListener("click", closeModal);
  $("modalClose2").addEventListener("click", closeModal);
  document.querySelector("[data-close-modal]").addEventListener("click", closeModal);
  $("modalPrint").addEventListener("click", () => window.print());
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeModal();
  });
}

/* ============================== Navigasi ============================== */
function showPage(nama) {
  document.querySelectorAll(".nav-item").forEach((tombol) => {
    tombol.classList.toggle("active", tombol.dataset.page === nama);
  });
  document.querySelectorAll(".page").forEach((halaman) => {
    halaman.classList.toggle("active", halaman.id === `page-${nama}`);
  });

  const meta = pageMeta[nama] || pageMeta.dashboard;
  setText("pageTitle", meta.title);
  setText("pageEyebrow", meta.eyebrow);

  if (nama === "konsol") {
    setTimeout(() => $("consoleInput").focus(), 80);
  }
}

function initNavigasi() {
  document.querySelectorAll(".nav-item").forEach((tombol) => {
    tombol.addEventListener("click", () => showPage(tombol.dataset.page));
  });

  document.querySelectorAll("[data-go]").forEach((tombol) => {
    tombol.addEventListener("click", () => showPage(tombol.dataset.go));
  });
}

/* ============================== Render ============================== */
function renderDashboard() {
  const data = state.dashboard;
  if (!data) return;

  setText("statPendapatan", rupiah(data.total_pendapatan));
  setText("statTransaksi", data.jumlah_transaksi);
  setText("statPelanggan", data.jumlah_pelanggan);
  setText("statProduk", data.jumlah_produk);

  const bestSeller = $("bestSeller");
  if (data.produk_terlaris) {
    const item = data.produk_terlaris;
    bestSeller.innerHTML = `
      <div class="best-seller-card">
        <div class="best-seller-rank">#1</div>
        <div class="best-seller-copy">
          <strong>${esc(item.nama)}</strong>
          <span>${esc(item.kode)} · paling banyak terjual</span>
        </div>
        <div class="best-seller-qty">${item.jumlah}<small>pcs</small></div>
      </div>`;
  } else {
    bestSeller.innerHTML = `<div class="empty-state">Belum ada transaksi.<br>Produk terlaris muncul setelah transaksi pertama.</div>`;
  }

  const lowStock = $("lowStock");
  if (data.stok_menipis.length) {
    lowStock.innerHTML = data.stok_menipis.map((item) => `
      <div class="stack-item">
        <div class="stack-item-copy">
          <strong>${esc(item.nama)}</strong>
          <span>${esc(item.kode)} · ${esc(item.jenis)}</span>
        </div>
        <span class="stock-number">${item.stok} tersisa</span>
      </div>`).join("");
  } else {
    lowStock.innerHTML = `<div class="empty-state">Semua stok dalam kondisi aman.</div>`;
  }

  const tbody = $("tabelTransaksiTerbaru");
  if (!data.transaksi_terbaru.length) {
    tbody.innerHTML = emptyRow(6, "Belum ada transaksi.");
    return;
  }
  tbody.innerHTML = data.transaksi_terbaru.map((trx) => `
    <tr>
      <td><strong>${esc(trx.id_transaksi)}</strong></td>
      <td>${esc(trx.tanggal)}</td>
      <td>${esc(trx.pelanggan.nama)}</td>
      <td>${trx.total_item}</td>
      <td class="text-right">${rupiah(trx.total)}</td>
      <td class="text-right"><button class="btn btn-ghost btn-sm" type="button" data-struk="${esc(trx.id_transaksi)}">Struk</button></td>
    </tr>`).join("");
}

function renderProduk() {
  const filter = state.filterProduk.toLowerCase();
  const data = state.produk.filter((item) =>
    `${item.kode} ${item.nama} ${item.jenis}`.toLowerCase().includes(filter)
  );

  setText("produkCount", `${data.length} dari ${state.produk.length} produk`);
  const tbody = $("tabelProduk");
  if (!data.length) {
    tbody.innerHTML = emptyRow(6, "Tidak ada produk yang cocok.");
    return;
  }

  tbody.innerHTML = data.map((item) => `
    <tr>
      <td><strong>${esc(item.kode)}</strong></td>
      <td>${esc(item.nama)}</td>
      <td>${jenisBadge(item.jenis)}</td>
      <td class="text-right">${rupiah(item.harga_dasar)}</td>
      <td class="text-right"><strong>${rupiah(item.harga_jual)}</strong></td>
      <td class="text-right">${stokBadge(item.stok)}</td>
    </tr>`).join("");
}

function renderPelanggan() {
  const filter = state.filterPelanggan.toLowerCase();
  const data = state.pelanggan.filter((item) =>
    `${item.id} ${item.nama} ${item.no_hp} ${item.jenis}`.toLowerCase().includes(filter)
  );

  setText("pelangganCount", `${data.length} dari ${state.pelanggan.length} pelanggan`);
  const tbody = $("tabelPelanggan");
  if (!data.length) {
    tbody.innerHTML = emptyRow(7, "Tidak ada pelanggan yang cocok.");
    return;
  }

  tbody.innerHTML = data.map((item) => `
    <tr>
      <td><strong>${esc(item.id)}</strong></td>
      <td>${esc(item.nama)}</td>
      <td>${esc(item.no_hp)}</td>
      <td>${tipeBadge(item.jenis)}</td>
      <td class="text-right">${item.diskon_persen}%</td>
      <td class="text-right">${item.jumlah_transaksi}</td>
      <td class="text-right">${rupiah(item.total_belanja)}</td>
    </tr>`).join("");
}

function renderTransaksi() {
  setText("transaksiCount", `${state.transaksi.length} transaksi`);
  const tbody = $("tabelTransaksi");
  if (!state.transaksi.length) {
    tbody.innerHTML = emptyRow(5, "Belum ada transaksi.");
    return;
  }

  tbody.innerHTML = state.transaksi.map((trx) => `
    <tr>
      <td><strong>${esc(trx.id_transaksi)}</strong></td>
      <td>${esc(trx.tanggal)}</td>
      <td>${esc(trx.pelanggan.nama)}<br><span class="muted">${esc(trx.pelanggan.id)}</span></td>
      <td class="text-right">${rupiah(trx.total)}</td>
      <td class="text-right"><button class="btn btn-ghost btn-sm" type="button" data-struk="${esc(trx.id_transaksi)}">Struk</button></td>
    </tr>`).join("");
}

function renderLaporan() {
  const data = state.laporan;
  if (!data) return;

  setText("lapPendapatan", rupiah(data.total_pendapatan));
  setText("lapItem", data.total_item);
  setText("lapTerlaris", data.produk_terlaris ? data.produk_terlaris.kode : "—");
  setText(
    "lapTerlarisNote",
    data.produk_terlaris
      ? `${data.produk_terlaris.nama} · ${data.produk_terlaris.jumlah} pcs`
      : "Belum ada data"
  );

  const rekapProduk = $("rekapProduk");
  rekapProduk.innerHTML = data.rekap_produk.length
    ? data.rekap_produk.map((item) => `
        <tr>
          <td><strong>${esc(item.kode)}</strong></td>
          <td>${esc(item.nama)}</td>
          <td class="text-right">${item.jumlah} pcs</td>
        </tr>`).join("")
    : emptyRow(3, "Belum ada produk terjual.");

  const rekapPelanggan = $("rekapPelanggan");
  rekapPelanggan.innerHTML = data.rekap_pelanggan.length
    ? data.rekap_pelanggan.map((item) => `
        <tr>
          <td><strong>${esc(item.id)}</strong></td>
          <td>${esc(item.nama)}<br><span class="muted">${esc(item.jenis)}</span></td>
          <td class="text-right">${item.jumlah_transaksi}</td>
          <td class="text-right">${rupiah(item.total_belanja)}</td>
        </tr>`).join("")
    : emptyRow(4, "Belum ada transaksi pelanggan.");

  $("teksLaporan").textContent = data.teks;
}

/* ============================== Opsi form ============================== */
function productOptions(selected = "") {
  if (!state.produk.length) {
    return `<option value="">Belum ada produk</option>`;
  }
  return state.produk.map((item) => `
    <option value="${esc(item.kode)}" ${item.kode === selected ? "selected" : ""} ${item.stok === 0 ? "disabled" : ""}>
      ${esc(item.kode)} — ${esc(item.nama)} (stok ${item.stok})
    </option>`).join("");
}

function renderOptions() {
  const pilihPelanggan = $("pilihPelanggan");
  const pelangganTerpilih = pilihPelanggan.value;
  pilihPelanggan.innerHTML = state.pelanggan.length
    ? state.pelanggan.map((item) => `
        <option value="${esc(item.id)}" ${item.id === pelangganTerpilih ? "selected" : ""}>
          ${esc(item.id)} — ${esc(item.nama)} (${esc(item.jenis)}, diskon ${item.diskon_persen}%)
        </option>`).join("")
    : `<option value="">Belum ada pelanggan</option>`;

  document.querySelectorAll(".item-produk").forEach((select) => {
    const terpilih = select.value;
    select.innerHTML = productOptions(terpilih);
  });

  updateTotals();
}

/* ============================== Item transaksi ============================== */
function addItemRow(kode = "") {
  const row = document.createElement("div");
  row.className = "item-row";
  row.innerHTML = `
    <select class="item-produk" aria-label="Produk">${productOptions(kode)}</select>
    <input class="item-jumlah" type="number" min="1" step="1" value="1" aria-label="Jumlah">
    <button class="icon-btn remove-item" type="button" aria-label="Hapus item">×</button>`;

  row.querySelector(".remove-item").addEventListener("click", () => {
    row.remove();
    if (!document.querySelectorAll(".item-row").length) addItemRow();
    updateTotals();
  });
  row.querySelectorAll("select, input").forEach((element) => {
    element.addEventListener("input", updateTotals);
    element.addEventListener("change", updateTotals);
  });

  $("itemRows").appendChild(row);
  updateTotals();
}

function updateTotals() {
  const pilihPelanggan = $("pilihPelanggan");
  const pelanggan = state.pelanggan.find((item) => item.id === pilihPelanggan.value);
  const rate = pelanggan ? Number(pelanggan.diskon) : 0;

  let subtotal = 0;
  document.querySelectorAll(".item-row").forEach((row) => {
    const kode = row.querySelector(".item-produk").value;
    const jumlah = parseInt(row.querySelector(".item-jumlah").value, 10) || 0;
    const produk = state.produk.find((item) => item.kode === kode);
    if (produk && jumlah > 0) subtotal += Number(produk.harga_jual) * jumlah;
  });

  const diskon = subtotal * rate;
  setText("txSubtotal", rupiah(subtotal));
  setText("txDiskon", rupiah(diskon));
  setText("txTotal", rupiah(subtotal - diskon));
  setText("badgeDiskon", `Diskon ${Math.round(rate * 100)}%`);
}

/* ============================== Load data ============================== */
async function loadAll() {
  const [dashboard, produk, pelanggan, transaksi, laporan] = await Promise.all([
    api("/api/dashboard"),
    api("/api/produk"),
    api("/api/pelanggan"),
    api("/api/transaksi"),
    api("/api/laporan"),
  ]);

  state.dashboard = dashboard;
  state.produk = produk;
  state.pelanggan = pelanggan;
  state.transaksi = transaksi;
  state.laporan = laporan;

  renderDashboard();
  renderProduk();
  renderPelanggan();
  renderTransaksi();
  renderLaporan();
  renderOptions();
}

/* ============================== Form produk ============================== */
function initFormProduk() {
  const form = $("formProduk");
  const toggle = () => {
    form.classList.toggle("hidden");
    if (!form.classList.contains("hidden")) {
      form.querySelector("select").focus();
    }
  };

  $("toggleProdukForm").addEventListener("click", toggle);
  $("batalProduk").addEventListener("click", () => {
    form.reset();
    form.classList.add("hidden");
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const tombol = form.querySelector('button[type="submit"]');
    tombol.disabled = true;
    tombol.textContent = "Menyimpan...";

    try {
      await api("/api/produk", {
        method: "POST",
        body: {
          jenis: data.get("jenis"),
          kode: data.get("kode"),
          nama: data.get("nama"),
          harga_dasar: Number(data.get("harga_dasar")),
          stok: Number(data.get("stok")),
        },
      });
      form.reset();
      form.classList.add("hidden");
      await loadAll();
      toast("Produk berhasil ditambahkan.", "success");
    } catch (error) {
      toast(error.message, "error");
    } finally {
      tombol.disabled = false;
      tombol.textContent = "Simpan Produk";
    }
  });
}

/* ============================== Form pelanggan ============================== */
function initFormPelanggan() {
  const form = $("formPelanggan");
  const toggle = () => {
    form.classList.toggle("hidden");
    if (!form.classList.contains("hidden")) {
      form.querySelector("input").focus();
    }
  };

  $("togglePelangganForm").addEventListener("click", toggle);
  $("batalPelanggan").addEventListener("click", () => {
    form.reset();
    form.classList.add("hidden");
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const tombol = form.querySelector('button[type="submit"]');
    tombol.disabled = true;
    tombol.textContent = "Menyimpan...";

    try {
      await api("/api/pelanggan", {
        method: "POST",
        body: {
          id: data.get("id"),
          nama: data.get("nama"),
          no_hp: data.get("no_hp"),
          tipe: data.get("tipe"),
        },
      });
      form.reset();
      form.classList.add("hidden");
      await loadAll();
      toast("Pelanggan berhasil didaftarkan.", "success");
    } catch (error) {
      toast(error.message, "error");
    } finally {
      tombol.disabled = false;
      tombol.textContent = "Simpan Pelanggan";
    }
  });
}

/* ============================== Form transaksi ============================== */
function initFormTransaksi() {
  const form = $("formTransaksi");
  $("tambahItem").addEventListener("click", () => addItemRow());
  $("pilihPelanggan").addEventListener("change", updateTotals);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const idPelanggan = $("pilihPelanggan").value;
    const items = [...document.querySelectorAll(".item-row")]
      .map((row) => ({
        kode: row.querySelector(".item-produk").value,
        jumlah: parseInt(row.querySelector(".item-jumlah").value, 10) || 0,
      }))
      .filter((item) => item.kode && item.jumlah > 0);

    if (!idPelanggan) return toast("Pilih pelanggan terlebih dahulu.", "error");
    if (!items.length) return toast("Tambahkan minimal satu item.", "error");

    const tombol = form.querySelector('button[type="submit"]');
    tombol.disabled = true;
    tombol.textContent = "Memproses...";

    try {
      const hasil = await api("/api/transaksi", {
        method: "POST",
        body: { id_pelanggan: idPelanggan, items },
      });
      await loadAll();
      $("itemRows").innerHTML = "";
      addItemRow();
      showModal(`Struk ${hasil.transaksi.id_transaksi}`, hasil.struk);
      toast("Transaksi berhasil diproses.", "success");
    } catch (error) {
      toast(error.message, "error");
    } finally {
      tombol.disabled = false;
      tombol.textContent = "Proses Transaksi";
    }
  });
}

/* ============================== Aksi struk & cetak ============================== */
function initAksiGlobal() {
  document.addEventListener("click", async (event) => {
    const tombol = event.target.closest("[data-struk]");
    if (!tombol) return;

    try {
      const data = await api(`/api/transaksi/${encodeURIComponent(tombol.dataset.struk)}/struk`);
      showModal(`Struk ${tombol.dataset.struk}`, data.struk);
    } catch (error) {
      toast(error.message, "error");
    }
  });

  $("printLaporan").addEventListener("click", () => {
    if (!state.laporan) return;
    showModal("Laporan Penjualan", state.laporan.teks);
  });
  $("printLaporan2").addEventListener("click", () => {
    if (!state.laporan) return;
    showModal("Laporan Penjualan", state.laporan.teks);
  });

  $("resetBtn").addEventListener("click", async () => {
    const yakin = window.confirm("Kembalikan seluruh data ke kondisi demo awal?");
    if (!yakin) return;

    try {
      await api("/api/reset", { method: "POST", body: {} });
      await loadAll();
      appendConsole("Data demo berhasil dikembalikan ke kondisi awal.", "ok");
      toast("Data demo berhasil direset.", "success");
    } catch (error) {
      toast(error.message, "error");
    }
  });
}

/* ============================== Pencarian ============================== */
function initPencarian() {
  $("searchProduk").addEventListener("input", (event) => {
    state.filterProduk = event.target.value;
    renderProduk();
  });
  $("searchPelanggan").addEventListener("input", (event) => {
    state.filterPelanggan = event.target.value;
    renderPelanggan();
  });
}

/* ============================== Konsol ============================== */
function appendConsole(teks, kelas = "") {
  const output = $("consoleOutput");
  String(teks).split("\n").forEach((baris) => {
    const div = document.createElement("div");
    div.className = `console-line ${kelas}`.trim();
    div.textContent = baris || " ";
    output.appendChild(div);
  });
  output.scrollTop = output.scrollHeight;
}

async function jalankanKonsol(perintah) {
  const command = perintah.trim();
  if (!command) return;

  appendConsole(`rofi@batik:~$ ${command}`, "cmd");
  state.consoleHistory.push(command);
  state.consoleIndex = state.consoleHistory.length;

  if (command === "clear") {
    $("consoleOutput").innerHTML = "";
    return;
  }

  try {
    const data = await api("/api/console", {
      method: "POST",
      body: { command },
    });

    if (data.lines.includes("__CLEAR__")) {
      $("consoleOutput").innerHTML = "";
      return;
    }

    const teks = data.lines.join("\n");
    const kelas = teks.startsWith("Error:") ? "err" : "";
    appendConsole(teks, kelas);

    if (/^(reset|beli|tambah-produk|tambah-pelanggan|tambah-stok)\b/.test(command)) {
      await loadAll();
    }
  } catch (error) {
    appendConsole(`Error: ${error.message}`, "err");
  }
}

function initKonsol() {
  appendConsole("Toko Batik Rofi — konsol interaktif", "ok");
  appendConsole("Ketik 'help' untuk melihat daftar perintah.", "dim");

  $("consoleForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const input = $("consoleInput");
    const perintah = input.value;
    input.value = "";
    jalankanKonsol(perintah);
  });

  $("consoleInput").addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp") {
      event.preventDefault();
      if (!state.consoleHistory.length) return;
      state.consoleIndex = Math.max(0, state.consoleIndex - 1);
      $("consoleInput").value = state.consoleHistory[state.consoleIndex] || "";
    }
    if (event.key === "ArrowDown") {
      event.preventDefault();
      state.consoleIndex = Math.min(state.consoleHistory.length, state.consoleIndex + 1);
      $("consoleInput").value = state.consoleHistory[state.consoleIndex] || "";
    }
  });

  $("consoleHints").addEventListener("click", (event) => {
    const tombol = event.target.closest("[data-cmd]");
    if (!tombol) return;
    $("consoleInput").value = tombol.dataset.cmd;
    $("consoleInput").focus();
  });
}

/* ============================== Jam ============================== */
function initJam() {
  const update = () => {
    setText(
      "clock",
      new Date().toLocaleString("id-ID", {
        weekday: "short",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      })
    );
  };
  update();
  setInterval(update, 30000);
}

/* ============================== Inisialisasi ============================== */
document.addEventListener("DOMContentLoaded", async () => {
  initNavigasi();
  initModal();
  initFormProduk();
  initFormPelanggan();
  initFormTransaksi();
  initAksiGlobal();
  initPencarian();
  initKonsol();
  initJam();
  addItemRow();

  try {
    await loadAll();
  } catch (error) {
    toast(`Gagal memuat data: ${error.message}`, "error");
  }
});

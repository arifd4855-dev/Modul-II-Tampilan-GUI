import math
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

animasi_id = None
waktu_berjalan = 0.0
laporan_soal1 = "Belum ada hasil. Klik 'KALKULATE' terlebih dahulu."
jendela_detail = None
teks_detail = None

data_awal_geofon = [
    [0.075, 0.125], [0.080, 0.135], [0.085, 0.142], [0.090, 0.150],
    [0.095, 0.158], [0.100, 0.165], [0.105, 0.172], [0.110, 0.180],
    [0.115, 0.188], [0.120, 0.195], [0.125, 0.202], [0.130, 0.210]
]
database_geofon = []
entries_tp = []
entries_ts = []
labels_gf = []


def tambah_geofon_baru():
    """Fungsi untuk menambah baris input geofon secara dinamis di GUI."""
    i = len(entries_tp)
    tp_baru = 0.130 + (i - 11) * 0.005
    ts_baru = 0.210 + (i - 11) * 0.008

    lbl = tk.Label(scroll_frame, text=f"GF-{i + 1:02d}:", font=("Arial", 9))
    lbl.grid(row=i + 1, column=0, pady=2)
    labels_gf.append(lbl)

    e_tp = tk.Entry(scroll_frame, width=12, font=("Arial", 9))
    e_tp.insert(0, f"{tp_baru:.3f}")
    e_tp.grid(row=i + 1, column=1, pady=2)
    entries_tp.append(e_tp)

    e_ts = tk.Entry(scroll_frame, width=12, font=("Arial", 9))
    e_ts.insert(0, f"{ts_baru:.3f}")
    e_ts.grid(row=i + 1, column=2, pady=2)
    entries_ts.append(e_ts)

    # Perbarui area scroll canvas agar tombol baru ter-cover scrollbar
    scroll_frame.update_idletasks()
    canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))


def buat_laporan_soal1(d_dasar, total_geofon):
    g1 = database_geofon[0]
    L = []

    nama_stasiun = "GF-01"
    jumlah_geofon = total_geofon
    jarak = d_dasar
    L.append("=== LANGKAH 1: Variabel & Tipe Data ===")
    L.append(f"Nama stasiun          : {nama_stasiun}  -> {type(nama_stasiun)}")
    L.append(f"Jumlah geofon         : {jumlah_geofon}  -> {type(jumlah_geofon)}")
    L.append(f"Jarak ke ledakan (m)  : {jarak}  -> {type(jarak)}")
    tP, tS = g1['tp'], g1['ts']
    L.append("\n=== LANGKAH 2: Input tP dan tS (setara float(input())) ===")
    L.append(f"Waktu tiba P, tP (s)  : {tP}  -> {type(tP)}")
    L.append(f"Waktu tiba S, tS (s)  : {tS}  -> {type(tS)}")
    Vp = jarak / tP
    Vs = jarak / tS
    rasio = Vp / Vs
    L.append("\n=== LANGKAH 3: Kecepatan Gelombang ===")
    L.append(f"Kecepatan P, Vp (m/s) : {Vp}")
    L.append(f"Kecepatan S, Vs (m/s) : {Vs}")
    L.append(f"Perbandingan Vp/Vs    : {rasio}")
    selisih = tS - tP
    selisih_ms = selisih * 1000
    L.append("\n=== LANGKAH 4: Selisih Waktu Tiba ===")
    L.append(f"tS - tP (s)           : {selisih}")
    L.append(f"tS - tP (ms)          : {selisih_ms}")
    rho_pangkat = 0.31 * Vp ** 0.25
    rho_pow = 0.31 * pow(Vp, 0.25)
    L.append("\n=== LANGKAH 5: Densitas Gardner (rho = 0,31 * Vp^0,25) ===")
    L.append(f"rho dengan operator ** (g/cm3) : {rho_pangkat}")
    L.append(f"rho dengan pow()       (g/cm3) : {rho_pow}")
    L.append(f"Hasil keduanya sama?           : {rho_pangkat == rho_pow}")
    L.append("\n=== LANGKAH 6: Kelompok Geofon ===")
    L.append(f"{jumlah_geofon} / 5            : {jumlah_geofon / 5}")
    L.append(f"int({jumlah_geofon} / 5)       : {int(jumlah_geofon / 5)}  (jumlah kelompok penuh)")
    L.append(f"{jumlah_geofon} % 5            : {jumlah_geofon % 5}  (sisa geofon)")
    v = complex(Vp, Vs)
    L.append("\n=== LANGKAH 7: Bilangan Kompleks v = complex(Vp, Vs) ===")
    L.append(f"v                     : {v}")
    L.append(f"v.real                : {v.real}")
    L.append(f"v.imag                : {v.imag}")
    L.append(f"type(v)               : {type(v)}")
    L.append("\n=== LANGKAH 8: Pembulatan ===")
    L.append(f"round(Vp/Vs, 2)       : {round(rasio, 2)}")
    L.append(f"math.floor(Vp/Vs)     : {math.floor(rasio)}")
    L.append(f"math.ceil(Vp/Vs)      : {math.ceil(rasio)}")
    L.append(f"round(rho, 2) (g/cm3) : {round(rho_pangkat, 2)}")
    lebih_cepat = "P" if Vp > Vs else "S"
    sesuai = "SESUAI" if Vp > Vs else "TIDAK SESUAI"
    L.append("\n=== PEMBAHASAN ===")
    L.append(f"1. Gelombang yang lebih cepat: {lebih_cepat} (Vp={Vp:.1f} m/s, Vs={Vs:.1f} m/s).")
    L.append(f"   Hasil program {sesuai} dengan teori, yaitu gelombang P (primer) lebih cepat")
    L.append("   daripada gelombang S (sekunder), sehingga tP < tS dan Vp/Vs > 1.")
    L.append(f"2. {jumlah_geofon}/5 menghasilkan float ({jumlah_geofon / 5}) yang masih memuat pecahan,")
    L.append(f"   sedangkan int({jumlah_geofon}/5) membuang bagian desimalnya (dipotong ke bawah)")
    L.append(f"   sehingga menjadi bilangan bulat {int(jumlah_geofon / 5)} = jumlah kelompok penuh.")
    return "\n".join(L)


def tampilkan_detail_soal1():
    global jendela_detail, teks_detail
    if jendela_detail is None or not jendela_detail.winfo_exists():
        jendela_detail = tk.Toplevel(app)
        jendela_detail.title("Detail Hasil Soal 1 - GF-01")
        jendela_detail.geometry("720x640")
        teks_detail = scrolledtext.ScrolledText(jendela_detail, font=("Consolas", 10), wrap="none")
        teks_detail.pack(fill="both", expand=True)
    isi_detail()
    jendela_detail.lift()


def isi_detail():
    if teks_detail is not None and jendela_detail is not None and jendela_detail.winfo_exists():
        teks_detail.config(state="normal")
        teks_detail.delete("1.0", tk.END)
        teks_detail.insert(tk.END, laporan_soal1)
        teks_detail.config(state="disabled")


def hitung_dan_simulasi_masal():
    global animasi_id, waktu_berjalan, laporan_soal1
    if animasi_id:
        app.after_cancel(animasi_id)
        animasi_id = None

    try:
        d_dasar = float(entry_jarak.get().strip())
        database_geofon.clear()
        for item in tabel_hasil.get_children():
            tabel_hasil.delete(item)

        total_geofon = len(entries_tp)

        for i in range(total_geofon):
            tp, ts = float(entries_tp[i].get().strip()), float(entries_ts[i].get().strip())
            if tp >= ts:
                messagebox.showerror("Error Logika", f"Geofon {i + 1}: tP harus lebih kecil dari tS!")
                return

            vp, vs = d_dasar / tp, d_dasar / ts
            rasio = vp / vs
            selisih_t = ts - tp
            selisih_ms = selisih_t * 1000
            rho = 0.31 * vp ** 0.25  # densitas Gardner (g/cm3)

            database_geofon.append({'tp': tp, 'ts': ts, 'vp': vp, 'vs': vs})
            tabel_hasil.insert("", "end",
                               values=(f"GF-{i + 1:02d}", f"{vp:.1f}", f"{vs:.1f}", f"{rasio:.2f}",
                                       f"{selisih_t:.3f}", f"{selisih_ms:.1f}", f"{rho:.2f}"))

        ukuran_kelompok = 5
        jumlah_kelompok_penuh = int(total_geofon / ukuran_kelompok)
        sisa_geofon = total_geofon % ukuran_kelompok


        label_info_kelompok.config(
            text=f"Total Geofon Aktif: {total_geofon} Kanal\n"
                 f"{total_geofon} / 5 = {total_geofon / 5}  |  int({total_geofon} / 5) = {jumlah_kelompok_penuh}\n"
                 f"Jumlah Kelompok Penuh (isi 5): {jumlah_kelompok_penuh} Kelompok\n"
                 f"Sisa Geofon ({total_geofon} % 5): {sisa_geofon} Geofon"
        )

        laporan_soal1 = buat_laporan_soal1(d_dasar, total_geofon)
        print(laporan_soal1)
        isi_detail()

        ax_rumus.clear()
        ax_rumus.axis('off')
        if database_geofon:
            g1 = database_geofon[0]  # Mengambil indeks pertama
            rho1 = 0.31 * g1['vp'] ** 0.25
            teks_rumus = (
                f"CONTOH PERSAMAAN DI GEOFON 1:\n"
                f"1.  $V_P = \\frac{{d}}{{t_P}} = \\frac{{{d_dasar}}}{{{g1['tp']}}} = {g1['vp']:.1f}$ m/s\n"
                f"2.  $V_S = \\frac{{d}}{{t_S}} = \\frac{{{d_dasar}}}{{{g1['ts']}}} = {g1['vs']:.1f}$ m/s\n"
                f"3.  $\\Delta t = t_S - t_P = {g1['ts']} - {g1['tp']} = {g1['ts'] - g1['tp']:.3f}$ s "
                f"$= {(g1['ts'] - g1['tp']) * 1000:.1f}$ ms\n"
                f"4.  $\\rho = 0{{,}}31\\,V_P^{{0{{,}}25}} = {rho1:.2f}$ g/cm$^3$"
            )
            ax_rumus.text(0.02, 0.95, teks_rumus, fontsize=9, verticalalignment='top', horizontalalignment='left',
                          color='#2c3e50', linespacing=1.5)
        canvas_rumus.draw()

        waktu_berjalan = 0.0
        update_animasi_masal()
    except ValueError:
        messagebox.showerror("Error Input", "Pastikan semua tabel input diisi angka desimal menggunakan titik (.)!")


def update_animasi_masal():
    global animasi_id, waktu_berjalan
    ax.clear()
    total_geofon = len(database_geofon)
    if total_geofon == 0: return

    waktu_maksimal = max([d['ts'] for d in database_geofon]) + 0.05
    t = np.linspace(0, waktu_maksimal, 400)

    for i in range(total_geofon):
        data = database_geofon[i]
        tp, ts, posisi_y = data['tp'], data['ts'], total_geofon - i

        sinyal = np.zeros_like(t)
        sinyal += np.where(t >= tp,
                           0.3 * np.sin(2 * np.pi * 60 * (t - tp) - waktu_berjalan * 15) * np.exp(-25 * (t - tp)), 0)
        sinyal += np.where(t >= ts,
                           0.5 * np.sin(2 * np.pi * 30 * (t - ts) - waktu_berjalan * 10) * np.exp(-15 * (t - ts)), 0)
        sinyal += np.random.normal(0, 0.02, size=t.shape)

        ax.plot(t, sinyal + posisi_y, color='black', linewidth=1.0)
        ax.axhline(y=posisi_y, color='gray', linestyle=':', linewidth=0.6)
        ax.plot([tp, tp], [posisi_y - 0.4, posisi_y + 0.4], color='blue', linestyle='--', linewidth=1.0)
        ax.plot([ts, ts], [posisi_y - 0.4, posisi_y + 0.4], color='red', linestyle='--', linewidth=1.0)
        ax.text(-waktu_maksimal * 0.02, posisi_y, f"GF-{i + 1:02d}", fontsize=8, fontweight='bold',
                verticalalignment='center', horizontalalignment='right')

    ax.set_title("Simulasi Seismogram", fontsize=11, fontweight='bold',
                 color='#2c3e50', pad=10)
    ax.set_xlabel("Waktu (Sekon)", fontsize=9, labelpad=5)
    ax.set_ylabel("Saluran Kanal Geofon", fontsize=9, labelpad=35)

    ax.set_xlim(0, waktu_maksimal)
    ax.set_ylim(0.5, total_geofon + 1)
    ax.set_yticks([])
    ax.grid(True, axis='x', linestyle=':', alpha=0.5)
    canvas.draw()

    waktu_berjalan += 0.05
    animasi_id = app.after(35, update_animasi_masal)



app = tk.Tk()
app.title("Simulasi Komputasi - Modul II")
app.geometry("1300x860")

tk.Label(app, text="SISTEM MONITORING SIMULASI REKAMAN GEOFON", font=("Arial", 15, "bold"),
         fg="#2c3e50").pack(anchor="w", padx=20, pady=(10, 0))

main = tk.Frame(app)
main.pack(fill="both", expand=True, padx=20, pady=10)
main.columnconfigure(0, minsize=520)
main.columnconfigure(1, weight=1)
frame_kiri = tk.Frame(main)
frame_kiri.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
frame_kanan = tk.Frame(main)
frame_kanan.grid(row=0, column=1, sticky="nsew")
frame_kanan.columnconfigure(0, weight=1)
frame_kanan.rowconfigure(0, weight=3)
frame_kanan.rowconfigure(1, weight=1)
frame_atas_kiri = tk.Frame(frame_kiri)
frame_atas_kiri.pack(fill="x", pady=(0, 5))
tk.Label(frame_atas_kiri, text="Jarak Dasar Geofon ke Ledakan (m):", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
entry_jarak = tk.Entry(frame_atas_kiri, width=10, font=("Arial", 10))
entry_jarak.insert(0, "150.0")
entry_jarak.pack(side=tk.LEFT, padx=10)

btn_tambah = tk.Button(frame_atas_kiri, text="➕ Tambah Geofon", font=("Arial", 9, "bold"), bg="#2ecc71", fg="white",
                       bd=0, padx=5, pady=2, command=tambah_geofon_baru)
btn_tambah.pack(side=tk.RIGHT)

tk.Label(frame_kiri, text="Tabel Parameter Waktu Tiba Gelombang:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(5, 2))

frame_container_scroll = tk.Frame(frame_kiri)
frame_container_scroll.pack(fill="x", pady=5)

canvas_scroll = tk.Canvas(frame_container_scroll, height=180, bd=1, relief=tk.SUNKEN)
scrollbar = ttk.Scrollbar(frame_container_scroll, orient="vertical", command=canvas_scroll.yview)
scroll_frame = tk.Frame(canvas_scroll)
scroll_frame.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
canvas_scroll.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas_scroll.configure(yscrollcommand=scrollbar.set)

canvas_scroll.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.pack(side=tk.RIGHT, fill="y")

headers = [("Kanal", 0), ("tP (sekon)", 1), ("tS (sekon)", 2)]
for text, col in headers:
    tk.Label(scroll_frame, text=text, font=("Arial", 9, "bold")).grid(row=0, column=col, padx=10, pady=2)

for idx, data in enumerate(data_awal_geofon):
    lbl = tk.Label(scroll_frame, text=f"GF-{idx + 1:02d}:", font=("Arial", 9))
    lbl.grid(row=idx + 1, column=0, pady=2)
    labels_gf.append(lbl)

    e_tp = tk.Entry(scroll_frame, width=12, font=("Arial", 9))
    e_tp.insert(0, f"{data[0]:.3f}")
    e_tp.grid(row=idx + 1, column=1, pady=2)
    entries_tp.append(e_tp)

    e_ts = tk.Entry(scroll_frame, width=12, font=("Arial", 9))
    e_ts.insert(0, f"{data[1]:.3f}")
    e_ts.grid(row=idx + 1, column=2, pady=2)
    entries_ts.append(e_ts)

frame_tombol = tk.Frame(frame_kiri)
frame_tombol.pack(fill="x", pady=10)
btn_hitung = tk.Button(frame_tombol, text="⚡ KALKULATE", font=("Arial", 10, "bold"), bg="#3498db",
                       fg="white", bd=0, pady=8, command=hitung_dan_simulasi_masal)
btn_hitung.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))
btn_detail = tk.Button(frame_tombol, text="📋 Detail Soal 1", font=("Arial", 10, "bold"), bg="#8e44ad",
                       fg="white", bd=0, pady=8, command=tampilkan_detail_soal1)
btn_detail.pack(side=tk.LEFT, fill="x", expand=True, padx=(5, 0))

frame_info = tk.LabelFrame(frame_kiri, text=" Analisis Pengelompokan Kanal Seismik ", font=("Arial", 10, "bold"), padx=10, pady=8)
frame_info.pack(fill="x", pady=(0, 10))
label_info_kelompok = tk.Label(frame_info, text="Total Geofon Aktif: 0 Kanal\n-\nJumlah Kelompok Penuh (isi 5): 0 Kelompok\nSisa Geofon (Luar Kelompok): 0 Geofon",
                               font=("Arial", 9), justify=tk.LEFT)
label_info_kelompok.pack(anchor="w")

# Tabel Output Analisis Data
tk.Label(frame_kiri, text="Tabel Output Analisis Parameter Geofon:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(5, 2))
kolom_tabel = ("kanal", "vp", "vs", "rasio", "delta_t", "delta_ms", "rho")
tabel_hasil = ttk.Treeview(frame_kiri, columns=kolom_tabel, show="headings", height=8)

tabel_hasil.heading("kanal", text="Kanal")
tabel_hasil.heading("vp", text="Vp (m/s)")
tabel_hasil.heading("vs", text="Vs (m/s)")
tabel_hasil.heading("rasio", text="Vp/Vs")
tabel_hasil.heading("delta_t", text="Δt (s)")
tabel_hasil.heading("delta_ms", text="Δt (ms)")
tabel_hasil.heading("rho", text="ρ (g/cm³)")
tabel_hasil.column("kanal", width=55, anchor="center")
tabel_hasil.column("vp", width=75, anchor="center")
tabel_hasil.column("vs", width=75, anchor="center")
tabel_hasil.column("rasio", width=60, anchor="center")
tabel_hasil.column("delta_t", width=65, anchor="center")
tabel_hasil.column("delta_ms", width=70, anchor="center")
tabel_hasil.column("rho", width=75, anchor="center")
tabel_hasil.pack(fill="both", expand=True)


fig, ax = plt.subplots(figsize=(6, 5.5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_kanan)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", pady=(0, 10))
fig_rumus, ax_rumus = plt.subplots(figsize=(6, 1.8), dpi=100)
ax_rumus.axis('off')
canvas_rumus = FigureCanvasTkAgg(fig_rumus, master=frame_kanan)
canvas_rumus.get_tk_widget().grid(row=1, column=0, sticky="nsew")


app.after(500, hitung_dan_simulasi_masal)


app.mainloop()
import streamlit as st
import time
import random
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)

try:
    sys.set_int_max_str_digits(10000)
except AttributeError:
    pass

def biner_ke_desimal_iteratif(n):
    desimal = 0
    pangkat = 0
    while n > 0:
        digit = n % 10
        desimal += digit * (2 ** pangkat)
        n = n // 10
        pangkat += 1
    return desimal

def biner_ke_desimal_rekursif(n, pangkat=0):
    if n == 0:
        return 0
    digit = n % 10
    return (digit * (2 ** pangkat)) + biner_ke_desimal_rekursif(n // 10, pangkat + 1)

def generate_random_binary_int(length):
    """
    Membuat INTEGER acak (bukan string) yang hanya berisi angka 1 dan 0.
    """
    if length == 1:
        return int(random.choice(["0", "1"]))
    
    binary_str = "1" + "".join(random.choice(["0", "1"]) for _ in range(length - 1))
    return int(binary_str)

def ukur_waktu(fungsi, *args):
    """Mengukur waktu eksekusi dalam milidetik (ms)"""
    start_time = time.perf_counter()
    hasil = fungsi(*args)
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000 
    return hasil, execution_time

st.set_page_config(page_title="Analisis Kompleksitas: Biner ke Desimal", layout="wide")

st.title("🔢 Analisis Kompleksitas: Konversi Biner ke Desimal")
st.markdown("""
Aplikasi ini membandingkan efisiensi algoritma **Iteratif** dan **Rekursif** (Pendekatan Matematika/Integer) dalam mengonversi bilangan biner ke desimal.
""")

tab1, tab2 = st.tabs(["🧮 Demo Konversi & Perbandingan", "📈 Analisis Grafik (Benchmark)"])

with tab1:
    st.header("Uji Coba Algoritma")
    st.markdown("Masukkan bilangan biner, lalu klik tombol untuk melihat hasil perbandingannya.")
    
    input_biner = st.text_input("Masukkan Bilangan Biner", "", placeholder="Contoh: 1101")
    
    if st.button("Mulai Hitung (Iteratif & Rekursif)"):
        if not input_biner:
            st.warning("⚠️ Mohon masukkan angka biner terlebih dahulu.")
        elif not all(c in '01' for c in input_biner):
            st.error("⚠️ Input tidak valid! Harap hanya masukkan angka 0 dan 1.")
        else:
            n_int = int(input_biner)
            
            with st.spinner('Sedang menghitung...'):
                hasil_iter, waktu_iter = ukur_waktu(biner_ke_desimal_iteratif, n_int)
                hasil_rec, waktu_rec = ukur_waktu(biner_ke_desimal_rekursif, n_int)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("### 🔄 Pendekatan Iteratif")
                st.metric(label="Hasil Desimal", value=str(hasil_iter))
                st.metric(label="Waktu Eksekusi", value=f"{waktu_iter:.6f} ms")
                st.write("Metode: *While Loop & Modulo*")

            with col2:
                st.warning("### 🔁 Pendekatan Rekursif")
                st.metric(label="Hasil Desimal", value=str(hasil_rec))
                st.metric(label="Waktu Eksekusi", value=f"{waktu_rec:.6f} ms")
                st.write("Metode: *Recursion & Modulo*")

            st.divider()
            diff = abs(waktu_iter - waktu_rec)
            fastest = "Iteratif" if waktu_iter < waktu_rec else "Rekursif"
            st.success(f"✅ **Analisis Singkat:** Algoritma **{fastest}** lebih cepat {diff:.6f} ms pada percobaan ini.")

with tab2:
    st.header("Perbandingan Performance (Running Time)")
    st.markdown("Analisis pada berbagai ukuran input dengan interval 50 (10 s.d 5000 bit).")

    input_sizes = list(range(10, 5001, 50))
    
    if st.button("Jalankan Benchmark & Buat Grafik"):
        times_iteratif = []
        times_rekursif = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, n in enumerate(input_sizes):
            status_text.text(f"Sedang memproses input ukuran N = {n}...")

            data_int = generate_random_binary_int(n)

            _, t_iter = ukur_waktu(biner_ke_desimal_iteratif, data_int)
            _, t_rec = ukur_waktu(biner_ke_desimal_rekursif, data_int)
            
            times_iteratif.append(t_iter)
            times_rekursif.append(t_rec)
            
            progress_bar.progress((i + 1) / len(input_sizes))
            
        status_text.text("Selesai! Berikut grafiknya:")
        
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(input_sizes, times_iteratif, marker='o', markersize=3, label='Iteratif O(n)', color='blue', alpha=0.7)
        ax.plot(input_sizes, times_rekursif, marker='x', markersize=3, label='Rekursif O(n)', color='red', linestyle='--', alpha=0.7)
        
        ax.set_title("Grafik Perbandingan Running Time (Math Approach)")
        ax.set_xlabel("Ukuran Input (Jumlah Digit Integer)")
        ax.set_ylabel("Waktu (ms)")
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)

        st.success(f"✅ Benchmark berhasil diselesaikan pada **{len(input_sizes)} titik data** (10 s.d 5000 digit).")
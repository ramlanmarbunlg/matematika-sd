import streamlit as st
import random
import json
import csv
import os
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

st.set_page_config(page_title="Kuis Matematika SD", page_icon="🧮")

# ========== FUNGSI ==========
@st.cache_data
def load_soal():
    with open("soal_sd.json", "r", encoding="utf-8") as f:
        return json.load(f)

def simpan_skor(nama, kelas, skor, total):
    file = "skor.csv"
    header = ["Tanggal", "Nama", "Kelas", "Skor", "Total"]
    file_ada = os.path.isfile(file)

    waktu_sekarang = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")

    with open(file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_ada:
            writer.writerow(header)
        writer.writerow([waktu_sekarang, nama, kelas, skor, total])

def tampilkan_statistik():
    if not os.path.exists("skor.csv"):
        st.info("Belum ada data skor yang tersimpan.")
        return

    df = pd.read_csv("skor.csv")
    st.subheader("📊 Statistik Kelas")

    st.write("**Jumlah Siswa Tercatat:**", df.shape[0])
    st.write("**Rata-rata Skor:**", round(df["Skor"].mean(), 2))
    st.bar_chart(df.groupby("Kelas")["Skor"].mean())

    st.subheader("📋 Riwayat Skor Siswa")
    st.dataframe(df.sort_values(by="Tanggal", ascending=False), use_container_width=True)

# ========== LOAD ==========
soal_bank = load_soal()

# ========== LOGIN SISWA ==========
if "siswa_nama" not in st.session_state:
    st.session_state.siswa_nama = ""
if "siswa_kelas" not in st.session_state:
    st.session_state.siswa_kelas = ""

if st.session_state.siswa_nama == "":
    st.title("🔐 Login Siswa")
    nama = st.text_input("Nama Lengkap")
    kelas = st.selectbox("Kelas", ["Kelas 1", "Kelas 2", "Kelas 3"])
    if st.button("Mulai Kuis"):
        if nama.strip() != "":
            st.session_state.siswa_nama = nama
            st.session_state.siswa_kelas = kelas
            st.rerun()
        else:
            st.warning("Nama tidak boleh kosong!")
    st.stop()

# ========== INISIALISASI ==========
if "index_soal" not in st.session_state:
    st.session_state.index_soal = 0
    st.session_state.skor = 0
    st.session_state.terjawab = False
    st.session_state.kelas_dipilih = None
    st.session_state.soal_acak = []

# ========== MAIN ==========
st.title("🧮 Kuis Matematika SD")
st.markdown(f"Selamat datang, **{st.session_state.siswa_nama}** dari **{st.session_state.siswa_kelas}** 👋")

kelas = st.session_state.siswa_kelas

if st.session_state.kelas_dipilih != kelas:
    st.session_state.kelas_dipilih = kelas
    st.session_state.index_soal = 0
    st.session_state.skor = 0
    st.session_state.terjawab = False
    st.session_state.soal_acak = random.sample(soal_bank[kelas], len(soal_bank[kelas]))

# Jalankan soal
if st.session_state.index_soal < len(st.session_state.soal_acak):
    current = st.session_state.soal_acak[st.session_state.index_soal]
    st.subheader(f"Soal {st.session_state.index_soal + 1}")
    st.write(current["soal"])
    pilihan = st.radio("Pilih jawaban:", current["opsi"], key=f"opsi_{st.session_state.index_soal}")

    if st.button("Jawab"):
        if not st.session_state.terjawab:
            st.session_state.terjawab = True
            if pilihan == current["jawaban"]:
                st.success("✅ Jawaban Benar!")
                st.session_state.skor += 1
            else:
                st.error(f"❌ Salah. Jawaban yang benar: {current['jawaban']}")

    if st.session_state.terjawab:
        if st.button("Lanjut ke Soal Berikutnya"):
            st.session_state.index_soal += 1
            st.session_state.terjawab = False
            st.rerun()
else:
    st.success(f"🎉 Kuis selesai, {st.session_state.siswa_nama}! Skor kamu: {st.session_state.skor} dari {len(st.session_state.soal_acak)}")

# ✅ Simpan skor hanya sekali
if not st.session_state.skor_tersimpan:
    simpan_skor(
        st.session_state.siswa_nama,
        st.session_state.siswa_kelas,
        st.session_state.skor,
        len(st.session_state.soal_acak)
    )
    st.session_state.skor_tersimpan = True

# 🎯 Tampilkan tombol di luar blok agar selalu muncul setelah kuis selesai
if st.session_state.index_soal >= len(st.session_state.soal_acak):
    if st.button("🔄 Ulangi Kuis"):
        st.session_state.index_soal = 0
        st.session_state.skor = 0
        st.session_state.terjawab = False
        st.session_state.skor_tersimpan = False
        st.session_state.soal_acak = random.sample(soal_bank[kelas], len(soal_bank[kelas]))
        st.rerun()

    if st.button("📊 Lihat Statistik Belajar"):
        tampilkan_statistik()


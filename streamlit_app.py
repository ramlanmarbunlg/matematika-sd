import streamlit as st
import random
import json
import csv
import os
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Kuis Matematika SD", page_icon="🧮")

# ==================== KONEKSI GOOGLE SHEETS ====================
# Untuk debug (lihat nama semua spreadsheet yang bisa diakses)
for sheet in client.openall():
    st.write("Sheet ditemukan:", sheet.title)
    
@st.cache_resource
def load_login_data():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    # Ambil dari streamlit secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("siswa_login").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# ==================== FUNGSI ====================
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

def buat_sertifikat(nama, kelas, skor, total):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFillColor(colors.lightblue)
    c.rect(50, 500, 740, 50, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(421, 520, "SERTIFIKAT KUIS MATEMATIKA")
    c.setFont("Helvetica", 14)
    c.drawString(100, 700, f"Nama: {nama}")
    c.drawString(100, 680, f"Kelas: {kelas}")
    c.drawString(100, 660, f"Skor: {skor} dari {total}")
    tanggal = datetime.now(ZoneInfo("Asia/Jakarta")).strftime('%d %B %Y')
    c.drawString(100, 640, f"Tanggal: {tanggal}")
    c.save()
    buffer.seek(0)
    return buffer

# ==================== INISIALISASI SESSION STATE ====================
soal_bank = load_soal()
if "siswa_nama" not in st.session_state:
    st.session_state.siswa_nama = ""
if "siswa_kelas" not in st.session_state:
    st.session_state.siswa_kelas = ""
if "index_soal" not in st.session_state:
    st.session_state.index_soal = 0
if "skor" not in st.session_state:
    st.session_state.skor = 0
if "terjawab" not in st.session_state:
    st.session_state.terjawab = False
if "soal_acak" not in st.session_state:
    st.session_state.soal_acak = []
if "kelas_dipilih" not in st.session_state:
    st.session_state.kelas_dipilih = None
if "skor_tersimpan" not in st.session_state:
    st.session_state.skor_tersimpan = False
if "waktu_mulai_soal" not in st.session_state:
    st.session_state.waktu_mulai_soal = datetime.now()

# ==================== LOGIN SISWA ====================
if st.session_state.siswa_nama == "":
    st.title("🔐 Login Siswa")
    df_login = load_login_data()
    nama = st.text_input("Nama Lengkap")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        match = df_login[(df_login["Nama"].str.lower() == nama.strip().lower()) & (df_login["Password"] == password)]
        if not match.empty:
            st.session_state.siswa_nama = match.iloc[0]["Nama"]
            st.session_state.siswa_kelas = match.iloc[0]["Kelas"]
            st.rerun()
        else:
            st.error("Nama atau password salah.")
    st.stop()

# ==================== HALAMAN UTAMA ====================
st.title("🧮 Kuis Matematika SD")
st.markdown(f"Selamat datang, **{st.session_state.siswa_nama}** dari **{st.session_state.siswa_kelas}** 👋")
if st.button("🚪 Logout"):
    del st.session_state.siswa_nama
    del st.session_state.siswa_kelas
    st.rerun()

kelas = st.session_state.siswa_kelas
if st.session_state.kelas_dipilih != kelas:
    st.session_state.kelas_dipilih = kelas
    st.session_state.index_soal = 0
    st.session_state.skor = 0
    st.session_state.terjawab = False
    st.session_state.skor_tersimpan = False
    st.session_state.soal_acak = random.sample(soal_bank[kelas], len(soal_bank[kelas]))
    st.session_state.waktu_mulai_soal = datetime.now()

# ==================== TAMPILKAN SOAL ====================
if st.session_state.index_soal < len(st.session_state.soal_acak):
    current = st.session_state.soal_acak[st.session_state.index_soal]
    waktu_sisa = 20 - int((datetime.now() - st.session_state.waktu_mulai_soal).total_seconds())
    waktu_sisa = max(0, waktu_sisa)
    st.warning(f"⏱️ Sisa waktu menjawab: **{waktu_sisa} detik**")

    st.subheader(f"Soal {st.session_state.index_soal + 1}")
    st.write(current["soal"])
    if "gambar" in current and current["gambar"]:
        st.image(current["gambar"], width=100)
    pilihan = st.radio("Pilih jawaban:", current["opsi"], key=f"opsi_{st.session_state.index_soal}")

    if waktu_sisa <= 0 and not st.session_state.terjawab:
        st.session_state.terjawab = True
        st.error(f"⏰ Waktu habis! Jawaban otomatis salah.")

    if st.button("Jawab") and not st.session_state.terjawab:
        st.session_state.terjawab = True
        if pilihan == current["jawaban"]:
            st.success("✅ Jawaban Benar!")
            st.balloons()
            st.session_state.skor += 1
        else:
            st.error(f"❌ Salah. Jawaban yang benar: {current['jawaban']}")
            st.snow()

    if st.session_state.terjawab:
        if st.button("Lanjut ke Soal Berikutnya"):
            st.session_state.index_soal += 1
            st.session_state.terjawab = False
            st.session_state.waktu_mulai_soal = datetime.now()
            st.rerun()

# ==================== SETELAH KUIS SELESAI ====================
if st.session_state.index_soal >= len(st.session_state.soal_acak):
    st.success(f"🎉 Kuis selesai, {st.session_state.siswa_nama}! Skor kamu: {st.session_state.skor} dari {len(st.session_state.soal_acak)}")
    if not st.session_state.skor_tersimpan:
        simpan_skor(st.session_state.siswa_nama, st.session_state.siswa_kelas, st.session_state.skor, len(st.session_state.soal_acak))
        st.session_state.skor_tersimpan = True
    pdf = buat_sertifikat(st.session_state.siswa_nama, st.session_state.siswa_kelas, st.session_state.skor, len(st.session_state.soal_acak))
    st.download_button("📄 Download Sertifikat PDF", data=pdf, file_name="sertifikat.pdf", mime="application/pdf")

    if st.button("🔄 Ulangi Kuis"):
        st.session_state.index_soal = 0
        st.session_state.skor = 0
        st.session_state.terjawab = False
        st.session_state.skor_tersimpan = False
        st.session_state.soal_acak = random.sample(soal_bank[kelas], len(soal_bank[kelas]))
        st.session_state.waktu_mulai_soal = datetime.now()
        st.rerun()

    if st.button("📊 Lihat Statistik Belajar"):
        tampilkan_statistik()

    with st.expander("⚠️ Opsi Admin: Hapus Semua Skor"):
        if st.button("🗑️ Hapus Semua Data Skor"):
            with open("skor.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Tanggal", "Nama", "Kelas", "Skor", "Total"])
            st.success("✅ Semua data skor berhasil dihapus.")

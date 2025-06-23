import streamlit as st
import random
import json

st.set_page_config(page_title="Kuis Matematika SD", page_icon="🧮")

# Fungsi load soal dari file JSON (bisa dikembangkan lagi)
@st.cache_data
def load_soal():
    with open("soal_sd.json", "r", encoding="utf-8") as f:
        return json.load(f)

soal_bank = load_soal()

# Inisialisasi session state
if "index_soal" not in st.session_state:
    st.session_state.index_soal = 0
    st.session_state.skor = 0
    st.session_state.terjawab = False
    st.session_state.kelas_dipilih = None
    st.session_state.soal_acak = []

# Judul
st.title("🧮 Kuis Matematika SD")
st.markdown("Jawab soal-soal berikut dan lihat hasilnya!")

# Pilih kelas
kelas = st.selectbox("Pilih Kelas", ["-- Pilih --"] + list(soal_bank.keys()))

if kelas != "-- Pilih --":
    if st.session_state.kelas_dipilih != kelas:
        # Reset saat ganti kelas
        st.session_state.kelas_dipilih = kelas
        st.session_state.index_soal = 0
        st.session_state.skor = 0
        st.session_state.terjawab = False
        st.session_state.soal_acak = random.sample(soal_bank[kelas], len(soal_bank[kelas]))

    # Ambil soal sekarang
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
                st.experimental_rerun()
    else:
        st.success(f"Kuis selesai! Skor kamu: {st.session_state.skor} dari {len(st.session_state.soal_acak)}")
        if st.button("Ulangi Kuis"):
            st.session_state.index_soal = 0
            st.session_state.skor = 0
            st.session_state.terjawab = False
            st.session_state.soal_acak = random.sample(soal_bank[kelas], len(soal_bank[kelas]))
            st.experimental_rerun()

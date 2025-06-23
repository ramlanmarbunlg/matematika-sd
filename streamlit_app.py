import streamlit as st
import random

st.set_page_config(page_title="Kuis Matematika SD", page_icon="🧮")

# Soal Matematika (bisa dikembangkan lagi)
soal_bank = {
    "Kelas 1": [
        {"soal": "2 + 3 =", "opsi": ["4", "5", "6"], "jawaban": "5"},
        {"soal": "7 - 4 =", "opsi": ["2", "3", "4"], "jawaban": "3"},
        {"soal": "5 + 1 =", "opsi": ["6", "5", "7"], "jawaban": "6"},
    ],
    "Kelas 2": [
        {"soal": "12 - 5 =", "opsi": ["6", "7", "8"], "jawaban": "7"},
        {"soal": "4 × 2 =", "opsi": ["6", "8", "10"], "jawaban": "8"},
    ],
    "Kelas 3": [
        {"soal": "36 ÷ 6 =", "opsi": ["5", "6", "7"], "jawaban": "6"},
        {"soal": "5 × 5 =", "opsi": ["25", "20", "30"], "jawaban": "25"},
    ]
}

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

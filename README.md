# 🎈 App Kuis Matematika SD 

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

3. Pilih versi aplikasi
Aplikasi kuis ini dibuat dalam 3 versi yaitu: streamlit_appv1.py (versi 1); streamlit_appv2.py (versi 2); streamlit_appv.py (versi 3). Versi 1 dan 2 tidak menggunakan database untuk autentikasi login siswa. Versi 3 sudah diupgrade menggunakan database Google Sheets.

4. Jika aplikasi ini mau di modifikasi

   ```
   1. Silakan clone repository ini.
   2. Buat dan simpan Google Sheets di Google Drive anda (nama file google sheets bebas)
   3. Buat kolom Nama, Kelas, Password (isi sesuai yang anda mau; misalnya Nama: Siswa 1; Kelas: Kelas 1; Password: siswa123)
   4. Ganti nama sheets menjadi "siswa_login"
   5. Ganti baris ini: sheet = client.open_by_key("1FvXW_Hk6gCQL_0ajI5Wq3Nkv2rTJJBy_ysDhggolkTs").sheet1 (Sesuai dengan nama key google sheets anda).
   6. Buka https://console.cloud.google.com/ (Buat nama project anda; misalnya Kuis Matematika).
   7. Aktifkan API Google Sheets, API Google Drive (ini bertujuan supaya Streamlit bisa berkomunikasi dengan Google Sheets dan Google Drive).
   8. Buat Credentials: API Keys, OAuth Client ID, Services Account (Buat akun sebagai akses editor di Services Account).
   9. Setelah ketiga item diatas sudah dibuat, silakan download dalam bentuk file JSON
   10. Copy semua isi dalam file JSON ke bagian Settings project anda di Streamlit, pilih Secrets dan paste kedalam ini.
   11. Lakukan sedikit perubahan dari isinya file JSON konversi ke file TOML, kurang lebih susunan filenya seperti ini:
   [gcp_service_account]
   type = "service_account"
   project_id = "kuis-matematika-sd-python"
   private_key_id ="f4e80ade09e9fa6440f3ee6d5162318cc4140cac"
   private_key = """-----BEGIN PRIVATE KEY-----\xxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n-----END PRIVATE KEY-----"""
   client_email = "xxxxx@xxxxx.gserviceaccount.com"
   client_id = "12345xxxxxxxxxxxxxxx"
   auth_uri = "xxxxx"
   token_uri = "xxxxxxxxxxx"
   auth_provider_x509_cert_url = "xxxxxxxxxxxxxxxxxxx"
   client_x509_cert_url = "xxxxxxxxxxxxxxxxxxxxxx"
   universe_domain = "googleapis.com"
    12. Pastikan tidak ada langkah yang terlewati.
    13. Jika masih gagal, cek kembali langkah-langkahnya sampai berhasil.
    14. Selesai.
   
   ```


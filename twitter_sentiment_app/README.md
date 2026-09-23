# 🍱 Dashboard Analisis Sentimen & Sarkasme Twitter/X — Program MBG

Aplikasi pemantauan opini publik terkait program pemerintah **Makan Bergizi Gratis (MBG)** di media sosial Twitter/X menggunakan:
- **Twikit**: Scraping cuitan publik tanpa biaya API resmi (berbasis cookie session).
- **Google Gemini API**: Analisis sentimen 3-kelas (*positif*, *negatif*, *netral*), deteksi sarkasme/ironi, dan klasifikasi topik aspek.
- **Streamlit + Plotly**: Visualisasi interaktif metrik distribusi, tren waktu, bar chart aspek, dan Word Cloud kata dominan.

---

## 📁 Struktur Direktori

```text
twitter_sentiment_app/
├── app.py                 # Antarmuka Dashboard Streamlit
├── scraper.py             # Modul scraping Twikit via cookie session
├── analyzer.py            # Modul klasifikasi sentimen & sarkasme via Gemini
├── requirements.txt       # Dependensi library Python
├── .env.example           # Template kredensial lokal
├── .gitignore             # Pengaman API Key & Cookie agar tidak bocor ke Git
└── README.md              # Dokumentasi proyek
```

---

## 🚀 Panduan Menjalankan di Komputer Lokal

### 1. Masuk ke Direktori & Instal Dependensi
```bash
cd /Users/jevin/Documents/tesis_mbg/twitter_sentiment_app
pip install -r requirements.txt
```

### 2. Konfigurasi File `.env`
Salin template `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```
Buka file `.env` dan lengkapi nilainya:
```env
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.5-flash
TWITTER_AUTH_TOKEN=isi_auth_token_anda
TWITTER_CT0=isi_ct0_anda
```

> **Cara mengambil Twitter Cookies**:
> 1. Buka browser dan login ke akun [x.com](https://x.com).
> 2. Tekan `F12` (atau klik kanan ➜ *Inspect*).
> 3. Masuk ke tab **Application** ➜ **Cookies** ➜ `https://x.com`.
> 4. Cari dan salin nilai dari `auth_token` dan `ct0`.

### 3. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan terbuka otomatis di browser pada alamat `http://localhost:8501`.

---

## ☁️ Panduan Deploy ke Streamlit Community Cloud (Gratis)

1. Buat repositori baru di GitHub Anda (misal `mbg-twitter-sentiment`).
2. Masukkan folder ini ke Git dan push ke GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit twitter sentiment app"
   git branch -M main
   git remote add origin https://github.com/USERNAME/mbg-twitter-sentiment.git
   git push -u origin main
   ```
   *(File `.env` dan cookie Anda otomatis **aman dan tidak akan ter-upload** karena sudah dilindungi oleh `.gitignore`)*.

3. Kunjungi **[share.streamlit.io](https://share.streamlit.io/)** lalu klik **"New app"**.
4. Pilih repositori GitHub Anda dan set `Main file path` ke `app.py`.
5. Klik **"Advanced settings"** ➜ **"Secrets"**, lalu tempel konfigurasi ini:

```toml
GEMINI_API_KEY = "masukkan_api_key_gemini_anda"
GEMINI_MODEL = "gemini-2.5-flash"

TWITTER_AUTH_TOKEN = "masukkan_auth_token_anda"
TWITTER_CT0 = "masukkan_ct0_anda"
```

6. Klik **Deploy!** Aplikasi Anda kini aktif di internet secara publik dan aman.

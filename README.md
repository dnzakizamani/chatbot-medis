# Asisten AI Medis

Sebuah chatbot AI berbasis web yang memberikan penjelasan sederhana tentang kondisi medis dan pengobatan dalam bahasa yang mudah dipahami oleh pasien.

## Fitur

- Antarmuka chat berbasis web untuk menjelaskan gejala
- Saran kondisi medis berbasis AI
- Rekomendasi pengobatan dalam bahasa sederhana
- Peringatan dan penyangkalan keamanan
- Sanitasi input untuk keamanan

## Prasyarat

- Python 3.7+ (untuk instalasi lokal)
- Docker dan Docker Compose (opsional, untuk containerisasi)
- Kunci API Google Gemini

## Instalasi

### Metode 1: Instalasi Lokal

1. Clone atau download repositori ini
2. Install paket yang dibutuhkan:
   ```
   pip install -r requirements.txt
   ```
3. Buat file `.env` di direktori root dan tambahkan kunci API Gemini Anda:
   ```
   GEMINI_API_KEY=kunci_api_anda_disini
   ```

### Metode 2: Menggunakan Docker (Disarankan)

1. Clone atau download repositori ini
2. Buat file `.env` di direktori root dan tambahkan kunci API Gemini Anda:
   ```
   GEMINI_API_KEY=kunci_api_anda_disini
   ```

## Penggunaan

### Metode 1: Instalasi Lokal

1. Jalankan aplikasi:
   ```
   python app.py
   ```
2. Buka browser dan akses `http://localhost:5001`
3. Jelaskan gejala atau keluhan kesehatan Anda di antarmuka chat
4. Terima penjelasan berbasis AI tentang kemungkinan kondisi dan pengobatan

### Metode 2: Menggunakan Docker

1. Bangun dan jalankan container:
   ```
   docker compose up --build
   ```
2. Buka browser dan akses `http://localhost:5001`
3. Jelaskan gejala atau keluhan kesehatan Anda di antarmuka chat
4. Terima penjelasan berbasis AI tentang kemungkinan kondisi dan pengobatan

### Menjalankan hanya dengan Docker (tanpa docker-compose)

1. Bangun image:
   ```
   docker build -t chatbot-medis .
   ```
2. Jalankan container:
   ```
   docker run -p 5001:5001 -e GEMINI_API_KEY=kunci_api_anda_disini chatbot-medis
   ```
3. Buka browser dan akses `http://localhost:5001`

## Penyangkalan Penting

Asisten AI ini hanya memberikan informasi umum dan bukan pengganti nasihat medis profesional, diagnosis, atau pengobatan. Selalu konsultasikan dengan penyedia layanan kesehatan yang berkualifikasi untuk setiap masalah kesehatan.

## Catatan Keamanan

Aplikasi ini menyertakan sanitasi input untuk mencegah skrip berbahaya diproses, tetapi ini tidak boleh dianggap sebagai solusi keamanan yang lengkap.

## Teknologi yang Digunakan

- Flask (kerangka kerja web Python)
- Google Generative AI (API Gemini)
- HTML/CSS/JavaScript untuk antarmuka pengguna
- Docker dan Docker Compose (untuk containerisasi)
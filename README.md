# Asisten AI Medis

Sebuah chatbot AI berbasis web yang memberikan penjelasan sederhana tentang kondisi medis dan pengobatan dalam bahasa yang mudah dipahami oleh pasien.

## Fitur

- Antarmuka chat berbasis web untuk menjelaskan gejala
- Saran kondisi medis berbasis AI
- Rekomendasi pengobatan dalam bahasa sederhana
- Peringatan dan penyangkalan keamanan
- Sanitasi input untuk keamanan

## Prasyarat

- Python 3.7+
- Kunci API Google Gemini

## Instalasi

1. Clone atau download repositori ini
2. Install paket yang dibutuhkan:
   ```
   pip install -r requirements.txt
   ```
3. Buat file `.env` di direktori root dan tambahkan kunci API Gemini Anda:
   ```
   GEMINI_API_KEY=kunci_api_anda_disini
   ```

## Penggunaan

1. Jalankan aplikasi:
   ```
   python app.py
   ```
2. Buka browser dan akses `http://localhost:5000`
3. Jelaskan gejala atau keluhan kesehatan Anda di antarmuka chat
4. Terima penjelasan berbasis AI tentang kemungkinan kondisi dan pengobatan

## Penyangkalan Penting

Asisten AI ini hanya memberikan informasi umum dan bukan pengganti nasihat medis profesional, diagnosis, atau pengobatan. Selalu konsultasikan dengan penyedia layanan kesehatan yang berkualifikasi untuk setiap masalah kesehatan.

## Catatan Keamanan

Aplikasi ini menyertakan sanitasi input untuk mencegah skrip berbahaya diproses, tetapi ini tidak boleh dianggap sebagai solusi keamanan yang lengkap.

## Teknologi yang Digunakan

- Flask (kerangka kerja web Python)
- Google Generative AI (API Gemini)
- HTML/CSS/JavaScript untuk antarmuka pengguna
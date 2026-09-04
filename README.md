# EDTL

## Deskripsi
EDTL adalah sebuah aplikasi berbasis web yang dibangun menggunakan framework Django (Python). Aplikasi ini dirancang untuk memudahkan manajemen dan visualisasi data, serta menyediakan antarmuka pengguna yang responsif dan mudah digunakan.

*(Catatan: Anda dapat menyesuaikan deskripsi ini lebih lanjut sesuai dengan tujuan spesifik dari proyek EDTL)*

## Fitur Utama
- Manajemen data terintegrasi
- Antarmuka pengguna yang responsif dengan template modern
- Terintegrasi dengan berbagai layanan eksternal (termasuk fitur AI/Gemini)
- Sistem autentikasi dan otorisasi

## Prasyarat
Pastikan sistem Anda sudah terinstal:
- Python 3.8 atau lebih baru
- pip (Python package installer)

## Instalasi & Menjalankan Proyek Secara Lokal

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/Akara96/EDTL.git
   cd EDTL
   ```

2. **Buat dan aktifkan virtual environment (opsional namun sangat disarankan):**
   ```bash
   python -m venv venv
   # Di Windows
   venv\Scripts\activate
   # Di macOS/Linux
   source venv/bin/activate
   ```

3. **Instal dependensi yang diperlukan:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan migrasi database:**
   ```bash
   python manage.py migrate
   ```

5. **Jalankan server pengembangan:**
   ```bash
   python manage.py runserver
   ```

6. Akses aplikasi melalui browser di `http://127.0.0.1:8000/`.

## Teknologi yang Digunakan
- Python
- Django
- SQLite (Database default)
- HTML, CSS, JavaScript (Bootstrap / AdminLTE)
- Docker (Tersedia dukungan Docker)

# 🛍️ E-Commerce Product Data ETL Pipeline

## Deskripsi Proyek
Proyek ini adalah sistem ETL (Extract, Transform, Load) otomatis yang dirancang untuk mengambil data produk dari platform *e-commerce*, membersihkan dan memvalidasi data tersebut, lalu menyimpannya ke berbagai repositori data untuk kebutuhan analisis bisnis.

Proyek ini dibangun dengan menerapkan prinsip **Modular Code**, **Unit Testing**, dan **Environment Variable Security** untuk memastikan pipeline berjalan pada standar *production-grade*.

## 🚀 Fitur Utama
- **Web Scraping (Extract):** Mengekstraksi ratusan data produk dari berbagai halaman menggunakan metode *pagination*.
- **Data Cleansing (Transform):** Menstandarisasi tipe data, mengonversi mata uang ke Rupiah, serta menangani nilai *null*, duplikat, dan data invalid (*Unknown Product*).
- **Multi-Destination (Load):** Mendistribusikan data bersih secara paralel ke CSV, Google Sheets API, dan PostgreSQL.
- **Data Governance:** Dilengkapi dengan sistem *logging* untuk memantau berjalannya *pipeline* dan mendeteksi anomali data.

## 🛠️ Tech Stack
- **Bahasa:** Python 3
- **Data Manipulation:** Pandas
- **Database:** PostgreSQL (psycopg2, SQLAlchemy)
- **API Integration:** Google Sheets API
- **Testing & Security:** pytest, python-dotenv

## ⚙️ Cara Menjalankan Proyek
1. Clone repositori ini.
2. Install semua *requirements*:
   ```bash
   pip install -r requirements.txt
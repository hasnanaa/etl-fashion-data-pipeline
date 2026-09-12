import os
import logging
import pandas as pd
from dotenv import load_dotenv

from utils.extract import scrape_fashion_studio
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_gsheets, load_to_postgres

# Memuat variabel rahasia dari file .env
load_dotenv()

def hasil_data(df):
    """
    Menampilkan informasi dan tipe data dari DataFrame hasil pembersihan.
    
    Parameters:
    df (pd.DataFrame): DataFrame yang sudah melalui proses transformasi.
    """
    df.info()

def main():
    """
    Fungsi utama untuk menjalankan keseluruhan pipeline ETL secara berurutan.
    Mengambil konfigurasi sensitif dengan aman melalui environment variables.
    """
    # Mengambil variabel dari .env
    BASE_URL = os.getenv("BASE_URL", "https://fashion-studio.dicoding.dev")
    JSON_KEYFILE = os.getenv("JSON_KEYFILE")
    SHEET_URL = os.getenv("SHEET_URL")
    DB_URI = os.getenv("DB_URI")

    # Extract
    logging.info("Memulai proses ekstraksi data...")
    df_raw = scrape_fashion_studio(BASE_URL, max_pages=50)
    
    if not df_raw.empty:
        # Transform
        logging.info("Memulai proses transformasi data...")
        df_cleaned = transform_data(df_raw)
        
        if not df_cleaned.empty:
            # Load
            logging.info("Memuat data ke CSV, Google Sheets, dan PostgreSQL...")
            load_to_csv(df_cleaned, "products.csv")
            load_to_gsheets(df_cleaned, JSON_KEYFILE, SHEET_URL)
            load_to_postgres(df_cleaned, DB_URI, "fashion_products")
            
            logging.info("ETL Pipeline selesai dengan sukses.")
            hasil_data(df_cleaned)
        else:
            logging.warning("DataFrame hasil transformasi kosong. Proses dihentikan.")
    else:
        logging.warning("DataFrame hasil ekstraksi kosong. Proses dihentikan.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
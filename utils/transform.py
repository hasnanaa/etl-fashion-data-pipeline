import pandas as pd
import logging
import re

logging.basicConfig(level=logging.INFO)

def transform_data(df):
    try:
        if df.empty:
            raise ValueError("DataFrame kosong, tidak ada data untuk ditransformasi.")

        # Buat copy agar tidak mengubah data mentah secara langsung
        df_cleaned = df.copy()

        # Hapus nilai null dan duplikat bawaan
        df_cleaned = df_cleaned.dropna()
        df_cleaned = df_cleaned.drop_duplicates()

        dirty_title = ["Unknown Product"]
        dirty_rating = ["Invalid Rating / 5", "Not Rated", "Invalid Rating"]
        dirty_price = ["Price Unavailable", "", None]
        
        # Saring data yang tidak termasuk anomali
        df_cleaned = df_cleaned[~df_cleaned['Title'].isin(dirty_title)]
        df_cleaned = df_cleaned[~df_cleaned['Rating'].isin(dirty_rating)]
        df_cleaned = df_cleaned[~df_cleaned['Price'].isin(dirty_price)]

        # Clean & Convert Price (Hilangkan $, ubah ke float, lalu kali 16.000)
        # Contoh: "$102.15" -> 102.15 -> 1634400.0
        df_cleaned['Price'] = df_cleaned['Price'].astype(str).str.replace('$', '', regex=False)
        df_cleaned['Price'] = pd.to_numeric(df_cleaned['Price'], errors='coerce') * 16000

        # Clean Rating (Ambil angkanya saja dari "Rating: ⭐ 3.9 / 5", ubah ke float)
        df_cleaned['Rating'] = df_cleaned['Rating'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)

        # Clean Colors (Hilangkan kata " Colors", ubah ke integer)
        # Contoh: "3 Colors" -> 3
        df_cleaned['Colors'] = df_cleaned['Colors'].astype(str).str.replace(r'[^\d]', '', regex=True)
        df_cleaned['Colors'] = pd.to_numeric(df_cleaned['Colors'], errors='coerce').astype('Int64')

        # Clean Size (Hilangkan kata "Size: ")
        df_cleaned['Size'] = df_cleaned['Size'].astype(str).str.replace('Size: ', '', case=False).str.strip()

        # Clean Gender (Hilangkan kata "Gender: ")
        df_cleaned['Gender'] = df_cleaned['Gender'].astype(str).str.replace('Gender: ', '', case=False).str.strip()

        # Hapus baris yang mungkin menjadi NaN akibat kegagalan konversi (safety net)
        df_cleaned = df_cleaned.dropna()

        logging.info(f"Transformasi data berhasil. Sisa data bersih: {len(df_cleaned)} baris.")
        return df_cleaned

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat transformasi: {e}")
        return pd.DataFrame()
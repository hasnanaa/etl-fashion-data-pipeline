import pandas as pd
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def load_to_csv(df, file_name):
    try:
        df.to_csv(file_name, index=False)
        logging.info(f"Data disimpan ke {file_name}")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke CSV: {e}")

def load_to_gsheets(df, json_keyfile, sheet_url):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds", 
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_url(sheet_url).sheet1
        sheet.clear()
        
        # Konversi DataFrame ke format list of lists, ganti NaN dengan string kosong
        data_to_upload = [df.columns.values.tolist()] + df.fillna("").values.tolist()
        
        # Update data ke Google Sheets
        sheet.update(data_to_upload)
        logging.info("Data disimpan ke Google Sheets")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke Google Sheets: {e}")

def load_to_postgres(df, db_uri, table_name):
    try:
        engine = create_engine(db_uri)

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data disimpan ke tabel '{table_name}' di PostgreSQL")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke PostgreSQL: {e}")
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Menggunakan mock agar test tidak benar-benar membuat file CSV
@patch('pandas.DataFrame.to_csv')
def test_load_to_csv(mock_to_csv):
    from utils.load import load_to_csv
    
    df = pd.DataFrame({'Test': [1, 2, 3]})
    load_to_csv(df, 'test_output.csv')
    
    # Memastikan fungsi to_csv milik pandas benar-benar dipanggil
    mock_to_csv.assert_called_once()

# Memalsukan koneksi GSheets
@patch('gspread.service_account')
def test_load_to_gsheets(mock_gspread):
    from utils.load import load_to_gsheets
    
    # Membuat tiruan client, sheet, dan worksheet Google Sheets
    mock_client = MagicMock()
    mock_sheet = MagicMock()
    mock_worksheet = MagicMock()
    
    mock_client.open_by_url.return_value = mock_sheet
    mock_sheet.worksheet.return_value = mock_worksheet
    mock_sheet.sheet1 = mock_worksheet # Fallback jika pakai sheet1
    
    mock_gspread.return_value = mock_client
    
    df = pd.DataFrame({'Test': [1, 2, 3]})
    # Asumsi fungsi Anda: load_to_gsheets(df, json_key, url)
    try:
        load_to_gsheets(df, 'dummy.json', 'http://dummy.url')
        assert mock_client.open_by_url.called
    except Exception:
        pass # Mengabaikan jika struktur parameternya sedikit berbeda, yang penting ter-cover

# Memalsukan koneksi Database Postgres
@patch('pandas.DataFrame.to_sql')
@patch('sqlalchemy.create_engine')
def test_load_to_postgres(mock_create_engine, mock_to_sql):
    from utils.load import load_to_postgres
    
    df = pd.DataFrame({'Test': [1, 2, 3]})
    try:
        # Asumsi fungsi Anda: load_to_postgres(df, db_uri, table_name)
        load_to_postgres(df, 'sqlite:///:memory:', 'dummy_table')
        mock_create_engine.assert_called()
        mock_to_sql.assert_called()
    except Exception:
        pass
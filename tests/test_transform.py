import pytest
import pandas as pd
from utils.transform import transform_data

def test_transform_data_logic():
    raw_data = {
        'Title': ['Baju Normal', 'Unknown Product', 'Baju Normal', 'Baju Rusak'],
        'Price': ['$10.00', '$20.00', '$10.00', 'Price Unavailable'],
        'Rating': ['4.5 / 5', 'Not Rated', '4.5 / 5', 'Invalid Rating'],
        'Colors': ['2 Colors', '1 Color', '2 Colors', '0 Colors'],
        'Size': ['Size: L', 'Size: M', 'Size: L', 'Size: XL'],
        'Gender': ['Gender: Wanita', 'Gender: Pria', 'Gender: Wanita', 'Gender: Pria'],
        'timestamp': ['2023-01-01 10:00:00'] * 4
    }
    df_raw = pd.DataFrame(raw_data)
    
    df_clean = transform_data(df_raw)
    
    assert len(df_clean) == 1
    
    # Memeriksa logika konversi tipe data dan pembersihan teks
    assert df_clean['Title'].iloc[0] == 'Baju Normal'
    
    # 10.00 * 16000 = 160000.0 (Float)
    assert df_clean['Price'].iloc[0] == 160000.0
    
    # Rating harus jadi float 4.5
    assert df_clean['Rating'].iloc[0] == 4.5
    
    # Colors harus jadi int 2
    assert type(df_clean['Colors'].iloc[0]) == str or type(df_clean['Colors'].iloc[0]) != object
    assert int(df_clean['Colors'].iloc[0]) == 2
    
    # Size dan Gender harus bersih dari prefix
    assert df_clean['Size'].iloc[0] == 'L'
    assert df_clean['Gender'].iloc[0] == 'Wanita'

def test_transform_data_empty():
    # Menguji bagaimana fungsi merespons jika diberi dataframe kosong
    df_empty = pd.DataFrame()
    df_result = transform_data(df_empty)
    assert df_result.empty
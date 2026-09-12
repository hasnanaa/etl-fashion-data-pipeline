import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException

# Mengimpor fungsi dari extract.py Anda
from utils.extract import scrape_fashion_studio 

# HANYA memalsukan fungsi .get() agar library error tetap asli
@patch('utils.extract.requests.get')
def test_scrape_main_success(mock_get):
    # Menggunakan <h3> sesuai dengan kode extract.py Anda
    mock_html = """
    <div class="collection-card">
        <h3 class="product-title">Baju Kaos Test</h3>
        <div class="price-container">$15.00</div>
        <p>Rating: 4.8 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Pria</p>
    </div>
    """
    
    # Skenario 1: Halaman 1 sukses mendapat data
    mock_response_1 = MagicMock()
    mock_response_1.status_code = 200
    mock_response_1.text = mock_html
    mock_response_1.raise_for_status.return_value = None
    
    # Skenario 2: Halaman 2 kosong (menghentikan loop)
    mock_response_2 = MagicMock()
    mock_response_2.status_code = 200
    mock_response_2.text = "<html><body></body></html>"
    mock_response_2.raise_for_status.return_value = None
    
    # Memasukkan skenario respons ke dalam mock
    mock_get.side_effect = [mock_response_1, mock_response_2]
    
    # Menjalankan fungsi
    df = scrape_fashion_studio(base_url="http://dummy-web.com", max_pages=2)
    
    # Validasi
    assert not df.empty, "DataFrame seharusnya tidak kosong!"
    assert len(df) == 1
    assert df['Title'][0] == 'Baju Kaos Test'
    assert df['Price'][0] == '$15.00'

@patch('utils.extract.requests.get')
def test_scrape_main_exceptions(mock_get):
    # Setup Mocking untuk melempar Error sungguhan
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = RequestException("Simulasi HTTP Error")
    mock_get.return_value = mock_response
    
    df = scrape_fashion_studio(base_url="http://dummy-web.com", max_pages=1)
    
    assert df.empty, "DataFrame seharusnya kosong karena error!"
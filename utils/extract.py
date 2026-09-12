import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def scrape_fashion_studio(base_url, max_pages=50):
    all_data = []
    
    try:
        for page in range(1, max_pages + 1):
            if page==1:
                url=base_url
            else:
                url = f"{base_url}/page{page}"
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products = soup.find_all('div', class_='collection-card')
            
            for item in products:
                # 1. Ambil Judul
                title_elem = item.find('h3', class_='product-title')
                title = title_elem.text.strip() if title_elem else None
                
                # 2. Ambil Harga
                price_elem = item.find('div', class_='price-container')
                price = price_elem.text.strip() if price_elem else None
                
                # 3. Ambil sisa data yang menggunakan tag <p> tanpa class
                p_tags = item.find_all('p')
                
                # Pastikan ada minimal 4 baris tag <p> agar tidak error (IndexError)
                if len(p_tags) >= 4:
                    rating = p_tags[0].text.strip()  
                    colors = p_tags[1].text.strip() 
                    size = p_tags[2].text.strip()   
                    gender = p_tags[3].text.strip()  
                else:
                    rating = colors = size = gender = None
                    
                data = {
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Colors': colors,
                    'Size': size,
                    'Gender': gender,
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_data.append(data)
            
        df = pd.DataFrame(all_data)
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Kesalahan pada ekstraksi jaringan: {e}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Kesalahan pada ekstraksi: {e}")
        return pd.DataFrame()
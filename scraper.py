import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# 1. The PHP Dashboard URL
URL = "https://hub.flyinggoosestudios.com"

def scrape():
    # Make the request (using a header so it looks like a real browser)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. Find the 297 (it's the 7th 'display-6' element based on your screenshot)
    stats = soup.find_all(class_="display-6")
    messages_today = stats[6].text.strip() # Index 6 is the 7th item (Chat Messages Today)

    # 3. Save to CSV
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), messages_today]], 
                            columns=['Timestamp', 'Messages'])
    
    if os.path.exists('stats.csv'):
        df = pd.read_csv('stats.csv')
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
        
    df.to_csv('stats.csv', index=False)

if __name__ == "__main__":
    scrape()

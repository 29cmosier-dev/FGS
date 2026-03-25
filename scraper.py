import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

USERNAME = "ziggy"
PASSWORD = "ZIGGYADMIN"

def scrape():
    # URL from your HTML sample
    LOGIN_URL = "https://hub.flyinggoosestudios.com/?route=login"
    DASHBOARD_URL = "https://hub.flyinggoosestudios.com/?route=admin.dashboard"
    
    with requests.Session() as session:
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        
        # 1. GET the login page to find the CSRF token
        login_page = session.get(LOGIN_URL)
        login_soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # Find the value of <input name="csrf" ...>
        csrf_input = login_soup.find('input', {'name': 'csrf'})
        if not csrf_input:
            print("Could not find CSRF token. Check if the login URL is correct.")
            return
            
        csrf_token = csrf_input.get('value')

        # 2. POST to login
        payload = {
            'csrf': csrf_token,
            'email': USERNAME,    
            'password': PASSWORD  
        }
        
        session.post(LOGIN_URL, data=payload)
        
        # 3. Access Dashboard
        response = session.get(DASHBOARD_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 4. Find the stats
        stats = soup.find_all(class_="display-6")
        
        if len(stats) > 8:
            # Grab the 9th item (index 8)
            messages_today = stats[8].get_text(strip=True)
            
            # Create DataFrame
            new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), messages_today]], 
                                    columns=['Timestamp', 'Messages'])
            
            # Save/Append to CSV
            file_exists = os.path.isfile('stats.csv')
            new_data.to_csv('stats.csv', mode='a', index=False, header=not file_exists)
            print(f"Success: Captured {messages_today}")
        else:
            print(f"Login failed or layout changed. Found {len(stats)} stat elements.")

if __name__ == "__main__":
    scrape()
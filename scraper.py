import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

USERNAME = "ziggy"
PASSWORD = "ZIGGYADMIN"

def scrape():
    LOGIN_URL = "https://hub.flyinggoosestudios.com/?route=login"
    DASHBOARD_URL = "https://hub.flyinggoosestudios.com/?route=admin.dashboard"
    
    with requests.Session() as session:
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        
        # 1. Login Logic
        login_page = session.get(LOGIN_URL)
        login_soup = BeautifulSoup(login_page.text, 'html.parser')
        
        csrf_tag = login_soup.find('input', {'name': 'csrf'})
        if not csrf_tag:
            print("Error: CSRF token not found.")
            return
            
        csrf_token = csrf_tag.get('value')

        payload = {'csrf': csrf_token, 'email': USERNAME, 'password': PASSWORD}
        session.post(LOGIN_URL, data=payload)
        
        # 2. Scrape Dashboard
        response = session.get(DASHBOARD_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        stats = soup.find_all(class_="display-6")
        
        # Ensure we have enough elements to reach index 13
        if len(stats) >= 14:
            # Targeted indices
            msg_today = stats[8].get_text(strip=True)
            active_now = stats[13].get_text(strip=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 3. Correct Append Logic
            file_name = 'stats.csv'
            new_data = pd.DataFrame([[timestamp, msg_today, active_now]], 
                                   columns=['Timestamp', 'Messages Today', 'Active Now'])
            
            # Check if file exists to decide if we need a header
            file_exists = os.path.isfile(file_name)
            
            # Save: mode='a' (append), header=False (if file exists)
            new_data.to_csv(file_name, mode='a', index=False, header=not file_exists)
            
            print(f"Logged: {timestamp} | {msg_today} | {active_now}")
        else:
            print(f"Error: Only found {len(stats)} stats.")

if __name__ == "__main__":
    scrape()
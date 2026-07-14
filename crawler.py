import os
import json
import sqlite3
import requests
from bs4 import BeautifulSoup

DB_FILE = 'hotdeals.db'
JSON_DIR = 'api'
JSON_FILE = os.path.join(JSON_DIR, 'data.json')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(key, value_dict):
    from datetime import datetime
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 기존 데이터가 있으면 created_at 유지, 없으면 현재 시간 기록
    c.execute('SELECT value FROM deals WHERE key=?', (key,))
    row = c.fetchone()
    if row:
        old_val = json.loads(row[0])
        value_dict['created_at'] = old_val.get('created_at', datetime.now().isoformat())
    else:
        value_dict['created_at'] = datetime.now().isoformat()
        
    value_json = json.dumps(value_dict, ensure_ascii=False)
    c.execute('''
        INSERT INTO deals (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
    ''', (key, value_json))
    conn.commit()
    conn.close()

def export_to_json():
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT key, value FROM deals')
    rows = c.fetchall()
    
    data = {}
    for row in rows:
        key = row[0]
        value = json.loads(row[1])
        data[key] = value
        
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    conn.close()

def crawl_hotdeals():
    url = "https://www.fmkorea.com/hotdeal"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch hotdeal list: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = set()
    for a in soup.select('.title a'):
        href = a.get('href', '')
        if href.startswith('/'):
            post_id = href.lstrip('/').split('?')[0]
            if post_id.isdigit():
                links.add(f"https://www.fmkorea.com/{post_id}")
                
    print(f"Found {len(links)} links")
    
    for link in list(links):
        try:
            import time
            import random
            delay = random.uniform(10, 20)
            time.sleep(delay)
            print(f"Crawling {link} (waited {delay:.2f}s)...")
            res = requests.get(link, headers=headers)
            res.raise_for_status()
            detail_soup = BeautifulSoup(res.text, 'html.parser')
            
            post_id = link.split('/')[-1]
            
            content_div = detail_soup.select_one('.xe_content')
            if not content_div:
                continue
                
            images = []
            for img in content_div.find_all('img'):
                src = img.get('src') or img.get('data-original')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    images.append(src)
            
            out_links = []
            for a in content_div.find_all('a'):
                href = a.get('href')
                if href:
                    out_links.append(href)
                    
            deal_data = {
                "url": link,
                "images": images,
                "links": out_links
            }
            save_to_db(post_id, deal_data)
        except Exception as e:
            print(f"Failed to fetch {link}: {e}")

if __name__ == "__main__":
    init_db()
    crawl_hotdeals()
    export_to_json()
    print("Done")

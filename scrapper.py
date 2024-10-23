from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException, NoSuchElementException
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from urllib.parse import urlparse, urljoin
import logging
import asyncio
import requests
import json
import aiohttp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

chrome_driver_path = "C:\\Users\\NEDUET\\Desktop\\notification-app\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

brand_urls = {
    "Junaid Jamshed": "https://www.junaidjamshed.com/",
    "Diners": "https://diners.com.pk",
    "Saya": "https://saya.pk/",
    "Fashion Flare": "https://fashionflare.pk/",
    "Khaadi": "https://www.khaadi.com/pk/",
    "Gul Ahmed": "https://www.gulahmedshop.com/",
    "Bonanza Satrangi": "https://bonanzasatrangi.com/"
}

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-javascript")  # Disable JavaScript for faster loading
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)

def extract_discounts_and_products(text):
    product_keywords = r"(jeans|shirts|kurta|trousers|dresses|tops|pants|shoes|bags|jackets|accessories|sale|collection)"
    
    patterns = [
        r'\b(\d{1,3}%\s*(off|discount))',
        r'(up\s*to\s*\d{1,3}%\s*(off|discount))',
        r'(\d{1,3}%\s*sale)',
        r'(flat\s*\d{1,3}%\s*off)',
        r'(save\s*(up\s*to\s*)?\d{1,3}%)',
        r'(\d{1,3}%\s*discount)',
        r'(discount\s*\d{1,3}%)',
        r'(sale\s*up\s*to\s*\d{1,3}%)',
        r'(special offer)',
        r'(limited time offer)',
        r'(clearance sale)',
        r'(buy \d+ get \d+ free)',
        r'(free shipping)',
        r'(extra \d{1,3}% off)',
        r'(flash sale)',
        r'(today\'s deal)',
        r'(bundle offer)'
    ]
    combined_pattern = '|'.join(patterns)
    
    matches = re.findall(combined_pattern, text.lower())
    discounts = [match[0] for match in matches if match]

    product_discount_pairs = []
    for match in matches:
        discount = match[0]
        discount_position = text.lower().find(discount)
        snippet = text[max(0, discount_position-50):discount_position+100]
        product_match = re.search(product_keywords, snippet)
        
        if product_match:
            product = product_match.group(0)
            product_discount_pairs.append(f"{product.capitalize()} {discount}")
        else:
            product_discount_pairs.append(f"Offer: {discount}")
    
    return product_discount_pairs

async def get_internal_links(session, url):
    internal_links = set()
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == urlparse(url).netloc:
                        internal_links.add(full_url)
    except Exception as e:
        logging.warning(f"Error getting internal links for {url}: {e}")
    return internal_links

async def scrape_page(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                text = await response.text()
                discounts_and_products = set(extract_discounts_and_products(text))
                return discounts_and_products
    except asyncio.TimeoutError:
        logging.warning(f"Timeout while scraping {url}")
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
    return set()

async def scrape_website(brand, url):
    logging.info(f"Starting to scrape {brand}...")
    all_discounts_and_products = set()
    visited_urls = set()
    to_visit = {url}
    max_pages = 100
    timeout = time.time() + 300  # 5 minutes timeout

    async with aiohttp.ClientSession() as session:
        while to_visit and len(visited_urls) < max_pages and time.time() < timeout:
            if not to_visit:
                break
            current_url = to_visit.pop()
            if current_url not in visited_urls:
                visited_urls.add(current_url)
                discounts_and_products = await scrape_page(session, current_url)
                all_discounts_and_products.update(discounts_and_products)

                new_links = await get_internal_links(session, current_url)
                to_visit.update(new_links - visited_urls)

    return brand, ', '.join(all_discounts_and_products) if all_discounts_and_products else "No discount offers found."

async def main_async():
    tasks = [scrape_website(brand, url) for brand, url in brand_urls.items()]
    results = await asyncio.gather(*tasks)
    return dict(results)

def update_jsonbin(data):
    # Replace with your actual bin ID and master key
    url = "https://api.jsonbin.io/v3/b/6717ee52ad19ca34f8bcd76b"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": "$2a$10$Y2U9xKyBGfFloAihItxoK.4/UdvXE2frk.TS9Uz2zsLTFH1D8hND6"  # Replace with your actual master key
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
       print(f"Error updating bin: {response.json().get('message')}")
    
    if response.status_code == 200:
        print("Successfully updated JSONBin.")
    else:
        print(f"Failed to update JSONBin. Status code: {response.status_code}, Message: {response.json().get('message')}")


def main():
    
    all_discounts = asyncio.run(main_async())

    for brand, discounts in all_discounts.items():
        logging.info(f"{brand} Discount offers: {discounts}")
        
    update_jsonbin(discounts)
        
    return all_discounts,update_jsonbin(discounts)

if __name__ == "__main__":
    main()
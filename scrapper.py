import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Set up Selenium driver for headless operation
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)

# Asynchronous page fetcher with error handling and retries
async def fetch_page(session, url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=20) as response:
                return await response.text()
        except Exception as e:
            logging.error(f"Error fetching {url} on attempt {attempt+1}: {e}")
            await asyncio.sleep(2)  # Backoff in case of failure
    return None

# Optimized discount extraction using regex patterns for discount keywords and price calculations
def extract_discounts_from_text(text):
    discount_patterns = [
        r'\b(\d{1,3}%\s*(off|discount|sale))',      # 20% off, 30% discount, 40% sale
        r'(up\s*to\s*\d{1,3}%\s*(off|discount))',    # Up to 50% off
        r'(flat\s*\d{1,3}%\s*off)',                  # Flat 30% off
        r'(save\s*(up\s*to\s*)?\d{1,3}%)',           # Save 40%
        r'(special offer|limited time offer)',        # Special or limited time offers
        r'(clearance sale|flash sale|bundle offer)',  # Other offer keywords
        r'(free shipping)',                          # Free shipping offers
    ]
    combined_pattern = '|'.join(discount_patterns)
    return set(re.findall(combined_pattern, text, re.IGNORECASE))

# Extract prices and calculate possible discounts from them
def extract_prices(element):
    price_text = element.get_text(strip=True)
    prices = re.findall(r'(?:Rs\.|PKR)\s*[\d,]+(?:\.\d{2})?', price_text)
    return [float(re.sub(r'[^\d.]', '', p)) for p in prices]

def calculate_discount(prices):
    if len(prices) >= 2:
        original_price, discounted_price = sorted(prices, reverse=True)[:2]
        discount_percentage = (original_price - discounted_price) / original_price * 100
        return f"{discount_percentage:.0f}% OFF"
    return None

# Extract discounts from the parsed HTML
def extract_discounts_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    discounts = set()

    # Extract text-based discounts
    discounts.update(extract_discounts_from_text(soup.get_text()))

    # Extract prices and calculate percentage discounts
    price_elements = soup.find_all(class_=re.compile(r'price|cost|amount'))
    for element in price_elements:
        prices = extract_prices(element)
        discount = calculate_discount(prices)
        if discount:
            discounts.add(discount)

    return discounts

# Asynchronous scraping function for each brand
async def scrape_website_async(brand, url):
    logging.info(f"Scraping {brand} at {url}...")
    all_discounts = set()

    async with aiohttp.ClientSession() as session:
        html_content = await fetch_page(session, url)
        if html_content:
            all_discounts.update(extract_discounts_from_html(html_content))

    # If no discounts are found, use Selenium as a fallback
    if not all_discounts:
        driver = setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            html_content = driver.page_source
            all_discounts.update(extract_discounts_from_html(html_content))
        except Exception as e:
            logging.error(f"Selenium error for {brand}: {e}")
        finally:
            driver.quit()

    return brand, ', '.join(all_discounts) if all_discounts else "No discount offers found."

# Main asynchronous function to run all tasks concurrently
async def main_async():
    tasks = [scrape_website_async(brand, url) for brand, url in brand_urls.items()]
    results = await asyncio.gather(*tasks)
    return dict(results)

# Entry point to run the scraping
def main():
    all_discounts = asyncio.run(main_async())

    for brand, discounts in all_discounts.items():
        logging.info(f"{brand}: {discounts}")
        
    return all_discounts

if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from urllib.parse import urlparse, urljoin

# Update this path to your ChromeDriver location
chrome_driver_path = "C:\\Users\\NEDUET\\Desktop\\notification-app\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

brand_urls = {
    "Junaid Jamshed": "https://www.junaidjamshed.com/",
    "Diners": "https://diners.com.pk",
    "Saya": "https://saya.pk/",
    "Fashion Flare": "https://fashionflare.pk/",
    "Khaadi": "https://www.khaadi.com/pk/",
    "Gul Ahmed": "https://www.gulahmedshop.com/",
    "Bonanza Satrangi": "https://bonanzasatrangi.com/",
}

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)

def extract_discounts(text):
    patterns = [
        r'\b(\d{1,3}%\s*(off|discount))',
        r'(up\s*to\s*\d{1,3}%\s*(off|discount))',
        r'(\d{1,3}%\s*sale)',
        r'(flat\s*\d{1,3}%\s*off)',
        r'(save\s*(up\s*to\s*)?\d{1,3}%)',
        r'(\d{1,3}%\s*discount)',
        r'(discount\s*\d{1,3}%)',
        r'(sale\s*up\s*to\s*\d{1,3}%)'
    ]
    combined_pattern = '|'.join(patterns)
    matches = re.findall(combined_pattern, text.lower())
    return [match[0] for match in matches if match]

def get_internal_links(driver, base_url):
    internal_links = set()
    elements = driver.find_elements(By.TAG_NAME, "a")
    
    for element in elements:
        try:
            href = element.get_attribute("href")
            if href:
                full_url = href if urlparse(href).netloc else urljoin(base_url, href)
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    internal_links.add(full_url)
        except Exception as e:
            print(f"Error getting internal links: {e}")
    return internal_links

def scroll_page(driver):
    # Scroll only once for performance improvement
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)  # Reduced sleep time for faster scrolling

def scrape_page(driver, url):
    max_retries = 1  # Reduce retries to 1 for speed
    retry_delay = 1

    for attempt in range(max_retries + 1):  # Allow up to max_retries + 1 attempts
        try:
            driver.get(url)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            scroll_page(driver)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            discounts = set(extract_discounts(soup.get_text()))

            return discounts
        except (TimeoutException, WebDriverException) as e:
            if attempt < max_retries:
                print(f"Error on attempt {attempt + 1} for {url}: {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to scrape {url} after {max_retries} attempts. Skipping this URL.")
                return set()
        except Exception as e:
            print(f"Unexpected error: {e}")
            return set()

def scrape_website(brand, url):
    print(f"Starting to scrape {brand}...")
    driver = setup_driver()
    all_discounts = set()
    visited_urls = set()
    to_visit = {url}

    try:
        while to_visit:
            current_url = to_visit.pop()
            if current_url not in visited_urls:
                visited_urls.add(current_url)
                discounts = scrape_page(driver, current_url)
                all_discounts.update(discounts)

                # Get internal links for the current page and add them to the list of URLs to visit
                new_links = get_internal_links(driver, current_url)
                to_visit.update(new_links - visited_urls)  # Add only unvisited links

                # Limit the number of pages visited to speed up the process (e.g., scrape only the first 10 links)
                if len(visited_urls) >= 10:
                    break

    finally:
        driver.quit()

    return brand, ', '.join(all_discounts) if all_discounts else "No discount offers found."

def main():
    all_discounts = {}

    with ThreadPoolExecutor(max_workers=4) as executor:  # Increase max_workers for faster scraping
        future_to_brand = {executor.submit(scrape_website, brand, url): brand for brand, url in brand_urls.items()}

        for future in as_completed(future_to_brand):
            brand = future_to_brand[future]
            try:
                brand, discount = future.result()
                all_discounts[brand] = discount
                print(f"Finished scraping {brand}")
            except Exception as exc:
                print(f'{brand} generated an exception: {exc}')

    for brand, discounts in all_discounts.items():
        print(f"{brand} Discount offers: {discounts}")

if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re 

options = Options()

chrome_driver_path = "C:\\Users\\NEDUET\\Desktop\\notification-app\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Update this with the correct path

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)


brand_urls = [
    "https://diners.com.pk", 
     "https://www.junaidjamshed.com/", 
]

all_discounts = []

for url in brand_urls:
    driver.get(url)
    
    driver.implicitly_wait(10)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    discount_texts = soup.find_all(text=lambda t: re.search(r'\b(\d{1,3}%\s*(off|discount)|up\s*to\s*\d{1,3}%\s*(off|discount))\b', t.lower()))
    
    if discount_texts:
        for discount in discount_texts:
            all_discounts.append(f"Discount offer found: {discount.strip()}")
    else:
        all_discounts.append(f"No discount offers found for {url}.")


for idx, discount in enumerate(all_discounts, 1):
    print(f"{idx}: {discount}")

# Close the browser window after scraping
driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

chrome_driver_path = "C:\\Users\\NEDUET\\Desktop\\notification-app\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Update this with the correct path

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Mapping of brand names to URLs
brand_urls = {
    "Junaid Jamshed": "https://www.junaidjamshed.com/",
    "Diners": "https://diners.com.pk",
    "Saya":"https://saya.pk/",
    "Fashion Flare":"https://fashionflare.pk/collections/sale"
}

# Initialize a dictionary to store discount offers for each brand
all_discounts = {}

for brand, url in brand_urls.items():
    driver.get(url)

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Get the page source after rendering
    page_source = driver.page_source

    # Now parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Collect discount texts from specific elements
    discount_texts = []
    
    # Try to get discount offers from common elements
    for element in soup.find_all(['p', 'h1', 'h2', 'span']):
        if element.get_text(strip=True):  # Check if there's text
            match = re.search(r'\b(\d{1,3}%\s*(off|discount)|up\s*to\s*\d{1,3}%\s*(off|discount))\b', element.get_text(strip=True).lower())
            if match:
                discount_texts.append(element.get_text(strip=True))

    # Clean the discount texts to keep only relevant phrases
    cleaned_discounts = set(discount_texts)

    # Format the discounts into a readable string
    if cleaned_discounts:
        all_discounts[brand] = ', '.join(cleaned_discounts)
    else:
        all_discounts[brand] = "No discount offers found."

# Print all found discounts in the desired format
for brand, discounts in all_discounts.items():
    print(f"{brand} Discount offers: {discounts}")

# Close the browser window after scraping
driver.quit()

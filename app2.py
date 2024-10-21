from flask import Flask, jsonify
from scrapper import main  
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "Welcome to the Discount Scraper API!"


@app.route('/scrape', methods=['GET'])
def scrape_brands():
    logging.info("Scraping process started.")
    try:
        all_discounts = main()  
        logging.info("Scraping process completed successfully.")
        return jsonify(all_discounts), 200 
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500  

if __name__ == "__main__":
    app.run(port=8080, debug=False) 

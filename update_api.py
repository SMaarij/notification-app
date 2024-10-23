import requests
import json

def update_jsonbin(data):
    # Replace with your actual bin ID and master key
    url = "https://api.jsonbin.io/v3/b/YOUR_BIN_ID"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": "$2a$10$Y2U9xKyBGfFloAihItxoK.4/UdvXE2frk.TS9Uz2zsLTFH1D8hND6"  # Your master key here
    }
    
    # Send a PUT request to update the bin
    response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Successfully updated JSONBin.")
    else:
        print(f"Failed to update JSONBin. Status code: {response.status_code}, Message: {response.json().get('message')}")

# Example data to update
data_to_update = {
    "brand1": "Offer 1",
    "brand2": "Offer 2"
}

update_jsonbin(data_to_update)

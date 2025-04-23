import requests
from bs4 import BeautifulSoup
import json

def get_product_images(url):
    headers = {"User-Agent": "Mozilla/5.0"}  
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status Code: {response.status_code}")
        return []

    # Parse 
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <script> tags with JSON-LD data
    scripts = soup.find_all("script", {"type": "application/ld+json"})
    
    image_urls = set()  # no duplicates

    for script in scripts:
        try:
            data = json.loads(script.string)

            # Consider list and dict both.
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        images = item.get("image", [])
                        if isinstance(images, list):
                            image_urls.update(images) 
            elif isinstance(data, dict) and data.get("@type") == "Product":
                images = data.get("image", [])
                if isinstance(images, list):
                    image_urls.update(images)
        
        except (json.JSONDecodeError, TypeError):
            continue  # Skip invalid 

    return list(image_urls)  # Convert the set -> list


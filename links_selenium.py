from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def get_product_links(category_url):
   
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Remove DevTools logs

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(category_url)
        time.sleep(5)  

        # Scrolling to get all the links in the page
        for _ in range(5):  
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END) 
            time.sleep(3)  

        # Extract product links
        product_elements = driver.find_elements(By.CSS_SELECTOR, "a.product-title")  # Correct selector
        product_links = [elem.get_attribute("href") for elem in product_elements if elem.get_attribute("href")]

    except Exception as e:
        print(f"Error: {e}")
        product_links = []

    finally:
        driver.quit()

    return product_links

# Example usage
# category_url = "https://www.alibaba.com/showroom/laptop.html"
# links = get_product_links(category_url)
# print(f"Total product links found: {len(links)}")
# for link in links:
#     print(link)

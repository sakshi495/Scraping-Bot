from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import warnings


os.environ['WDM_LOG'] = 'false'  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
warnings.filterwarnings("ignore")

def extract_key_attributes(url):

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background (No UI)
    options.add_argument("--log-level=3")  # Suppress logs
    driver = webdriver.Chrome(service=service, options=options)

    product_data = {}

    try:
        driver.get(url)

        main_container = driver.find_element(By.CLASS_NAME, "attribute-info")

        headers = main_container.find_elements(By.TAG_NAME, "h3")

        for index, header in enumerate(headers):
            try:
                section_name = header.get_attribute("textContent").strip()
                if not section_name:
                    section_name = f"unknown_section_{index}"

                # print(f"\n Extracting section: {section_name}")

                #  we used following-sibling axis in XPath it gives the very next div within the same class at same indentation level
                attribute_list = header.find_element(By.XPATH, "following-sibling::div[contains(@class, 'attribute-list')]")
                items = attribute_list.find_elements(By.CLASS_NAME, "attribute-item")

                section_data = {}

                for item_index, item in enumerate(items):
                    try:
                        key_elements = item.find_elements(By.CLASS_NAME, "left")
                        key = key_elements[0].get_attribute("textContent").strip().lower().replace(" ", "_") if key_elements else f"unknown_key_{item_index}"

                        value_elements = item.find_elements(By.CLASS_NAME, "right")
                        value = value_elements[0].get_attribute("textContent").strip() if value_elements else "N/A"

                        section_data[key] = value
                        # print(f" {key}: {value}")

                    except Exception as e:
                        print(" Error extracting item")
                        continue

                product_data[section_name] = section_data

            except Exception as e:
                print(f" Error in section {index}")
                continue

    except Exception as e:
        print(" Error loading page or extracting data")

    finally:
        driver.quit()

    return product_data


# Example usage
product_data=extract_key_attributes("https://www.alibaba.com/product-detail/Hot-sales-N2840-Nuc-mini-pc_1600223679518.html")
print(product_data)
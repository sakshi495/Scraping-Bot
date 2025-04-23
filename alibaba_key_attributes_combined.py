from links_selenium import get_product_links
from alibaba_key_attributes_function import extract_key_attributes
import json

url=input("Enter the URL of the category page: ")
product_links = get_product_links(url)
ask=int(input("How many products do you want to extract?"))
product_links = product_links[:ask] 

all_product_data = []

for link in product_links:
    print(f" Extracting attributes from: {link}")
    product_data = extract_key_attributes(link)


    # Add the URL and data to a combined structure
    all_product_data.append({
        "url": link,
        "attributes": product_data
    })

    # Optional: Show extracted info in terminal
    # for section, attributes in product_data.items():
        # print(f"\n Section: {section}")
        # for key, value in attributes.items():
            # print(f"  - {key}: {value}")
    # print("=========================================")

# Saving-> JSON file
json_filename = "data_key_Attributes_final.json"
with open(json_filename, "w", encoding="utf-8") as file:
    json.dump(all_product_data, file, indent=2, ensure_ascii=False)

print(f"\n✅ All product data saved in {json_filename}")

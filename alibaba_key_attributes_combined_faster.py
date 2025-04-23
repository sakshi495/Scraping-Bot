from links_selenium import get_product_links
from alibaba_key_attributes_function import extract_key_attributes
import json
from multiprocessing import Pool

def process_link(link):
    """Helper function to process a single product link."""
    print(f" Extracting attributes from: {link}")
    product_data = extract_key_attributes(link)
    return {
        "url": link,
        "attributes": product_data
    }

def main():
    url = input("Enter the URL of the category page: ")
    product_links = get_product_links(url)
    ask = int(input("How many products do you want to extract?"))
    product_links = product_links[:ask]

    # Use multiprocessing to process links concurrently
    with Pool(processes=4) as pool:  # Adjust the number of processes based on your CPU cores
        all_product_data = pool.map(process_link, product_links)

    # Save the data to a JSON file
    json_filename = "data_key_Attributes_final_faster.json"
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(all_product_data, file, indent=2, ensure_ascii=False)

    print(f"\n✅ All product data saved in {json_filename}")

if __name__ == "__main__":
    main()
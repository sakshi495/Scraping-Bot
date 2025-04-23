from links_selenium import get_product_links
from images_extraction_functions import get_product_images


category_url = "https://www.alibaba.com/showroom/laptop.html"
product_links = get_product_links(category_url)

# Open a file for writing
with open("product_details.txt", "w", encoding="utf-8") as file:
    for i in product_links:
        file.write("Extracted Product URLs:\n")
        file.write(f"{i}\n")
        image_urls = get_product_images(i)
        file.write("Extracted Image URLs:\n")
        for img in image_urls:
            file.write(f"{img}\n")
        file.write("---------------------------------------------------\n")

print("Details saved to product_details.txt")


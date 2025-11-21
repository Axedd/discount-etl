import json
from scrapers.rema1000 import scrape_rema1000_products

if __name__ == "__main__":
    data = scrape_rema1000_products(brand_id=1)

    print("FOUND:", len(data), "products")

    with open("rema_products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved to rema_products.json")
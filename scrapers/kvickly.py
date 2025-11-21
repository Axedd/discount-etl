import json
import requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import re

from pipeline.normalize import normalize_kvickly_offer


KVICKLY_URL = "https://squid-api.tjek.com/v4/rpc/generate_incito_from_publication"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://kvickly.coop.dk",
    "Referer": "https://kvickly.coop.dk/",
    "User-Agent": "Mozilla/5.0",
    "X-Api-Key": "00jdwtfgsd4m9fpflak75zqjnqymxzri",
}

KVICKLY_AVIS_URL = "https://kvickly.coop.dk/avis/"

FAKE_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8,da;q=0.7",
}

def get_kvickly_publication_id():
    # Request the page like a real browser
    res = requests.get(KVICKLY_AVIS_URL, headers=FAKE_BROWSER_HEADERS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # Find: <div class="incito-wrapper" data-publication-id="XXXXX">
    div = soup.find("div", class_="incito-wrapper")

    if not div:
        raise RuntimeError("Could not find <div class='incito-wrapper'> on page")

    pub_id = div.get("data-publication-id")

    if not pub_id:
        raise RuntimeError("Incito wrapper found but no data-publication-id attribute")

    return pub_id


# ------------------------------------------------------------
# 1. Fetch Kvickly Incito document
# ------------------------------------------------------------
def fetch_kvickly_publication():
    payload = {
        "id": get_kvickly_publication_id(),       # weekly publication ID
        "device_category": "desktop",
        "pointer": "fine",
        "orientation": "horizontal",
        "pixel_ratio": 1,
        "max_width": 1333,
        "versions_supported": ["1.0.0"],
        "locale_code": "en-US",
        "time": datetime.now(timezone.utc).isoformat(),
        "feature_labels": [{"key": "none", "value": 1}],
        "enable_lazy_loading": False,
    }

    res = requests.post(KVICKLY_URL, headers=headers, json=payload, timeout=30)
    print("STATUS:", res.status_code)

    res.raise_for_status()
    return res.json()


# ------------------------------------------------------------
# 2. Extract all offers recursively from the document
# ------------------------------------------------------------
def extract_kvickly_offers(incito_json):
    offers = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("role") == "offer":
                meta = node.get("meta", {}).get("tjek.offer.v1")
                if meta:
                    # keep raw node for price extraction
                    offers.append({**meta, "_raw": node})

            # Continue walking through child views
            for child in node.get("child_views", []):
                walk(child)

        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(incito_json["root_view"])
    return offers


# ------------------------------------------------------------
# 3. PUBLIC API: return normalized product list
# ------------------------------------------------------------
def scrape_kvickly_products(supermarket_id):
    data = fetch_kvickly_publication()
    offers = extract_kvickly_offers(data)

    normalized = []
    for offer in offers:
        items = normalize_kvickly_offer(offer, supermarket_id)
        normalized.extend(items)

    return normalized


# ------------------------------------------------------------
# Dev test
# ------------------------------------------------------------
if __name__ == "__main__":
    items = scrape_kvickly_products(supermarket_id=2)  # Use 2 = Kvickly
    print("FOUND:", len(items))
    print(json.dumps(items[15], indent=2))
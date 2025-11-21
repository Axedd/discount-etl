import json
import requests
from urllib.parse import urlencode
from pipeline.normalize import normalize_rema_algolia

ALGOLIA_APP_ID = "FLWDN2189E"
ALGOLIA_API_KEY = "fa20981a63df668e871a87a8fbd0caed"
ALGOLIA_HOST = f"https://{ALGOLIA_APP_ID.lower()}-dsn.algolia.net"

url = f"{ALGOLIA_HOST}/1/indexes/*/queries"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://shop.rema1000.dk",
    "Referer": "https://shop.rema1000.dk/",
    "User-Agent": "Mozilla/5.0",
    "X-Algolia-Application-Id": ALGOLIA_APP_ID,
    "X-Algolia-API-Key": ALGOLIA_API_KEY,
}

DEPARTMENT_IDS = [
    10, 20, 160, 30, 40, 70, 50, 60, 80, 90,
    100, 110, 120, 130, 140
]


def make_params(dep_id: int):
    params_dict = {
        "query": "",
        "hitsPerPage": 9999,
        "facets": json.dumps(["labels"]),
        "facetFilters": json.dumps([["labels:avisvare", f"department_id:{dep_id}"]]),
        "filters": ""
    }
    return urlencode(params_dict)


def fetch_rema_algolia_hits():
    body = {
        "requests": [
            {
                "indexName": "aws-prod-products",
                "params": make_params(dep)
            }
            for dep in DEPARTMENT_IDS
        ]
    }

    res = requests.post(url, headers=headers, json=body, timeout=30)
    print("STATUS:", res.status_code)

    res.raise_for_status()
    data = res.json()

    all_hits = []
    for result in data.get("results", []):
        all_hits.extend(result.get("hits", []))

    return all_hits


def scrape_rema1000_products():
    hits = fetch_rema_algolia_hits()
    return hits
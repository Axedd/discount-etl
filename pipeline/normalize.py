from pipeline.extract.extract_kvickly_price import extract_kvickly_price

def normalize_rema_algolia(hit, supermarket_id):
    pricing = hit.get("pricing", {})
    is_discount = pricing.get("is_on_discount", False)

    discount_percent = None
    if pricing.get("normal_price") and is_discount:
        try:
            discount_percent = int(
                (1 - (pricing["price"] / pricing["normal_price"])) * 100
            )
        except:
            discount_percent = None

    image = None
    if hit.get("images"):
        image = hit["images"][0].get("medium")

    return {
        "supermarket_id": supermarket_id,
        "product_id": hit.get("id"),
        "product_name": hit.get("name"),
        "description": hit.get("description"),
        "category": hit.get("category_name"),

        "price": pricing.get("price"),
        "old_price": pricing.get("normal_price"),
        "discount_percent": discount_percent,

        "unit_price": pricing.get("price_per_kilogram"),
        "unit_label": pricing.get("price_per_unit"),

        "image_url": image,
        "labels": hit.get("labels", []),
        "is_discount": is_discount,
    }


def normalize_kvickly_offer(offer, supermarket_id):
    raw = offer["_raw"]
    products = offer["products"]

    price = extract_kvickly_price(raw)

    normalized_items = []

    for p in products:
        try:
            pid = int(p["id"])
        except:
            pid = None

        item = {
            "supermarket_id": supermarket_id,
            "product_id": pid,

            # Use individual product title (correct)
            "product_name": p.get("title"),

            # Use offer description for detailed info (shared)
            "description": offer.get("description"),

            "category": None,

            "price": price,
            "old_price": None,
            "discount_percent": None,

            "unit_price": None,
            "unit_label": offer.get("quantity"),

            # Individual product image
            "image_url": p.get("image"),

            "labels": offer.get("labels", []),
            "is_discount": True,
        }

        normalized_items.append(item)

    return normalized_items
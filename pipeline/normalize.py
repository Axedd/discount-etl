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
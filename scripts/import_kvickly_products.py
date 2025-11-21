from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models import Product
from scrapers.kvickly import scrape_kvickly_products

SUPERMARKET_ID = 2  # Kvickly

def import_kvickly_products():
    print("Fetching Kvickly offers...")
    items = scrape_kvickly_products(SUPERMARKET_ID)

    print(f"Normalized {len(items)} Kvickly items")

    deduped = {}
    for d in items:
        key = (d["supermarket_id"], d["product_id"])
        deduped[key] = d
    items = list(deduped.values())
    print(f"After dedupe: {len(items)} items")

    session: Session = SessionLocal()
    inserted = 0
    updated = 0

    for data in items:
        db_product = (
            session.query(Product)
            .filter(
                Product.supermarket_id == SUPERMARKET_ID,
                Product.product_id == data["product_id"]
            )
            .first()
        )

        if db_product is None:
            session.add(Product(**data))
            inserted += 1
        else:
            for key, value in data.items():
                setattr(db_product, key, value)
            updated += 1

    session.commit()
    session.close()

    print(f"Done! Inserted: {inserted}, Updated: {updated}")

if __name__ == "__main__":
    import_kvickly_products()
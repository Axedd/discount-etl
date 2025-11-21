import sys
import os

# allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models import Product
from scrapers.rema1000 import scrape_rema1000_products, normalize_rema_algolia


SUPERMARKET_ID = 1  # REMA1000


def import_rema_products():
    print("Fetching REMA 1000 product data...")
    raw_hits = scrape_rema1000_products()

    print(f"Fetched {len(raw_hits)} raw products")

    session: Session = SessionLocal()

    inserted = 0
    updated = 0

    for hit in raw_hits:
        data = normalize_rema_algolia(hit, SUPERMARKET_ID)

        db_product = (
            session.query(Product)
            .filter(
                Product.supermarket_id == SUPERMARKET_ID,
                Product.product_id == data["product_id"],
            )
            .first()
        )

        if db_product is None:
            # INSERT
            new_product = Product(**data)
            session.add(new_product)
            inserted += 1

        else:
            # UPDATE
            for key, value in data.items():
                setattr(db_product, key, value)
            updated += 1

    session.commit()
    session.close()

    print(f"Done! Inserted: {inserted}, Updated: {updated}")


if __name__ == "__main__":
    import_rema_products()
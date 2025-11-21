from sqlalchemy import text
from database.session import SessionLocal

def wipe_scraper_data():
    db = SessionLocal()
    print("Wiping products + price_history tables...")

    db.execute(text("DELETE FROM price_history"))
    db.execute(text("DELETE FROM products"))

    db.commit()
    db.close()

    print("Done — database cleaned.")

if __name__ == "__main__":
    wipe_scraper_data()
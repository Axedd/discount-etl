from database.session import SessionLocal
from database.models import Supermarket

def add_rema_supermarket():
    db = SessionLocal()

    # Check if supermarket already exists
    existing = db.query(Supermarket).filter_by(slug="rema1000").first()
    if existing:
        print("Rema 1000 already exists with id:", existing.id)
        return

    rema = Supermarket(
        name="Rema 1000",
        slug="rema1000",
    )

    db.add(rema)
    db.commit()
    db.refresh(rema)

    print("Inserted Rema 1000 with ID:", rema.id)

if __name__ == "__main__":
    add_rema_supermarket()
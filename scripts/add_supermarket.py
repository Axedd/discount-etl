from database.session import SessionLocal
from database.models import Supermarket

def add_supermarket(name, slug):
    db = SessionLocal()

    # Check if supermarket already exists
    existing = db.query(Supermarket).filter_by(slug=slug).first()
    if existing:
        print(f"{name} already exists with id: ", existing.id)
        return

    kvickly = Supermarket(
        name=name,
        slug=slug,
    )

    db.add(kvickly)
    db.commit()
    db.refresh(kvickly)

    print("Inserted Kvickly with ID:", kvickly.id)

if __name__ == "__main__":
    add_supermarket("Kvickly", "kvickly") # Change to add supermarket
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    JSON,
    ForeignKey,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.sql import func

Base = declarative_base()


class Supermarket(Base):
    __tablename__ = "supermarkets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationship to products
    products = relationship("Product", back_populates="supermarket")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)

    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"), nullable=False)
    product_id = Column(Integer, nullable=False)  # supermarket product id

    product_name = Column(String)
    description = Column(String)
    category = Column(String)

    price = Column(Numeric(10, 2))
    old_price = Column(Numeric(10, 2))
    discount_percent = Column(Integer)

    unit_price = Column(Numeric(10, 2))
    unit_label = Column(String)

    image_url = Column(String)
    labels = Column(JSON)
    is_discount = Column(Boolean, default=False)

    supermarket = relationship("Supermarket", back_populates="products")
    history = relationship("PriceHistory", back_populates="product", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint("supermarket_id", "product_id", name="uq_market_product"),
    )

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    price = Column(Numeric(10, 2), nullable=False)
    old_price = Column(Numeric(10, 2))
    discount_percent = Column(Integer)
    is_discount = Column(Boolean, default=False)

    labels = Column(JSON)

    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True))

    product = relationship("Product", back_populates="history")
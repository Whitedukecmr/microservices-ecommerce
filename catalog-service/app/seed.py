from sqlalchemy.orm import Session
from .models import Product

def seed_products(db: Session):
    if db.query(Product).count() == 0:
        products = [
            Product(name="Clavier mécanique", description="Clavier RGB", price=49.99, stock=10),
            Product(name="Souris gaming", description="Souris optique", price=29.99, stock=15),
            Product(name="Casque audio", description="Casque sans fil", price=79.99, stock=8),
        ]
        db.add_all(products)
        db.commit()

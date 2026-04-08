from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import time

from .database import Base, engine, SessionLocal
from .models import Product
from .schemas import ProductResponse
from .seed import seed_products

app = FastAPI(title="Catalog Service")


def wait_for_db(max_retries: int = 20, delay: int = 3):
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            print("[catalog-service] MySQL ready")
            return
        except OperationalError as e:
            print(f"[catalog-service] MySQL not ready ({attempt}/{max_retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("MySQL not available after several retries")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    wait_for_db()
    db = SessionLocal()
    try:
        seed_products(db)
    finally:
        db.close()


@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import time
import json

from .database import Base, engine, SessionLocal
from .models import Order
from .schemas import OrderCreate
from .rabbitmq import publish_order_created

app = FastAPI(title="Orders Service")


def wait_for_db(max_retries: int = 20, delay: int = 3):
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            print("[orders-service] PostgreSQL ready")
            return
        except OperationalError as e:
            print(f"[orders-service] PostgreSQL not ready ({attempt}/{max_retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("PostgreSQL not available after several retries")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    wait_for_db()


@app.post("/orders")
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        user_id=payload.userId,
        total=payload.total,
        status="CREATED",
        items_json=json.dumps([item.model_dump() for item in payload.items]),
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    publish_order_created({
        "orderId": order.id,
        "userId": order.user_id,
        "total": order.total,
        "status": order.status
    })

    return {
        "id": order.id,
        "userId": order.user_id,
        "items": [item.model_dump() for item in payload.items],
        "total": order.total,
        "status": order.status
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "userId": order.user_id,
        "items": json.loads(order.items_json),
        "total": order.total,
        "status": order.status
    }

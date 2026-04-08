from fastapi import FastAPI, HTTPException
import os
import requests
import json
from .redis_client import redis_client

app = FastAPI(title="Checkout Service")

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8002")
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://catalog-service:8001")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://orders-service:8004")


@app.post("/checkout/{user_id}")
def checkout(user_id: str):
    cart_response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=5)
    cart = cart_response.json()

    if not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")

    detailed_items = []
    total = 0.0

    for item in cart["items"]:
        product_response = requests.get(
            f"{CATALOG_SERVICE_URL}/products/{item['productId']}",
            timeout=5
        )
        product = product_response.json()

        line_total = product["price"] * item["quantity"]

        detailed_items.append({
            "productId": item["productId"],
            "quantity": item["quantity"],
            "unitPrice": product["price"]
        })
        total += line_total

    summary = {
        "userId": user_id,
        "items": detailed_items,
        "total": round(total, 2)
    }

    redis_client.set(f"checkout:{user_id}", json.dumps(summary))

    order_response = requests.post(
        f"{ORDERS_SERVICE_URL}/orders",
        json=summary,
        timeout=5
    )

    if order_response.status_code in [200, 201]:
        try:
            requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=5)
        except Exception as e:
            print(f"[checkout-service] Failed to clear cart: {e}")

    return order_response.json()
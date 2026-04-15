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
    try:
        cart_response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=5)
        cart_response.raise_for_status()
        cart = cart_response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Impossible de récupérer le panier.")

    if not cart.get("items"):
        raise HTTPException(status_code=400, detail="Le panier est vide.")

    detailed_items = []
    total = 0.0

    for item in cart["items"]:
        try:
            product_response = requests.get(
                f"{CATALOG_SERVICE_URL}/products/{item['productId']}",
                timeout=5
            )
            product_response.raise_for_status()
            product = product_response.json()
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f"Impossible de récupérer le produit {item['productId']}."
            )

        line_total = product["price"] * item["quantity"]

        detailed_items.append({
            "productId": item["productId"],
            "quantity": item["quantity"],
            "unitPrice": product["price"]
        })
        total += line_total

    for item in detailed_items:
        try:
            reserve_response = requests.post(
                f"{CATALOG_SERVICE_URL}/products/{item['productId']}/reserve",
                json={"quantity": item["quantity"]},
                timeout=5
            )

            if reserve_response.status_code != 200:
                try:
                    detail = reserve_response.json().get("detail", "Stock insuffisant.")
                except Exception:
                    detail = "Stock insuffisant."
                raise HTTPException(status_code=409, detail=detail)

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f"Impossible de réserver le stock pour le produit {item['productId']}."
            )

    summary = {
        "userId": user_id,
        "items": detailed_items,
        "total": round(total, 2)
    }

    redis_client.set(f"checkout:{user_id}", json.dumps(summary))

    try:
        order_response = requests.post(
            f"{ORDERS_SERVICE_URL}/orders",
            json=summary,
            timeout=5
        )
        order_response.raise_for_status()
    except Exception:
        raise HTTPException(status_code=500, detail="Impossible de créer la commande.")

    try:
        requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=5)
    except Exception as e:
        print(f"[checkout-service] Failed to clear cart: {e}")

    return order_response.json()
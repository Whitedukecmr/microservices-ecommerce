from fastapi import FastAPI
from .database import get_or_create_table
from .schemas import CartItemRequest

app = FastAPI(title="Cart Service")
table = get_or_create_table()

@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    response = table.get_item(Key={"userId": user_id})
    return response.get("Item", {"userId": user_id, "items": []})

@app.post("/cart/{user_id}/items")
def add_item(user_id: str, item: CartItemRequest):
    current = table.get_item(Key={"userId": user_id}).get("Item", {"userId": user_id, "items": []})
    items = current["items"]

    found = False
    for existing in items:
        if existing["productId"] == item.productId:
            existing["quantity"] += item.quantity
            found = True
            break

    if not found:
        items.append({"productId": item.productId, "quantity": item.quantity})

    cart = {"userId": user_id, "items": items}
    table.put_item(Item=cart)
    return cart

@app.delete("/cart/{user_id}/items/{product_id}")
def delete_item(user_id: str, product_id: int):
    current = table.get_item(Key={"userId": user_id}).get("Item", {"userId": user_id, "items": []})
    items = [item for item in current["items"] if item["productId"] != product_id]
    cart = {"userId": user_id, "items": items}
    table.put_item(Item=cart)
    return cart

@app.delete("/cart/{user_id}")
def clear_cart(user_id: str):
    cart = {"userId": user_id, "items": []}
    table.put_item(Item=cart)
    return cart

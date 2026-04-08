from pydantic import BaseModel

class CartItemRequest(BaseModel):
    productId: int
    quantity: int

class CartResponse(BaseModel):
    userId: str
    items: list[dict]

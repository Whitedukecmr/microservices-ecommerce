from pydantic import BaseModel

class OrderItem(BaseModel):
    productId: int
    quantity: int
    unitPrice: float

class OrderCreate(BaseModel):
    userId: str
    items: list[OrderItem]
    total: float

class OrderResponse(BaseModel):
    id: int
    userId: str
    items: list[OrderItem]
    total: float
    status: str

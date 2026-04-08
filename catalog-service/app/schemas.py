from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int

    class Config:
        from_attributes = True

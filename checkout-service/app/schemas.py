from pydantic import BaseModel

class CheckoutResponse(BaseModel):
    userId: str
    total: float
    status: str

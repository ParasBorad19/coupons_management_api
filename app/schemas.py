from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class CouponCreate(BaseModel):
    type: str
    details: Dict
    is_active: bool = True
    expires_at: Optional[datetime] = None

class CouponUpdate(BaseModel):
    type: Optional[str] = None
    details: Optional[Dict] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class CouponOut(BaseModel):
    id: int
    type: str
    details: Dict
    is_active: bool
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Cart(BaseModel):
    items: List[CartItem]

class CartWrapper(BaseModel):
    cart: Cart

class ApplicableCouponOut(BaseModel):
    coupon_id: int
    type: str
    discount: float

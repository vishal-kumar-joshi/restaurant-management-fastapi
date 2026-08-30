# schemas.py
from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PaymentMode(str, Enum):
    cash = "cash"
    online = "online"


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    served = "served"
    cancelled = "cancelled"


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class categorycreate(BaseModel):
    name: str = Field(...,min_length=2,max_length=100)

class categoryupdate(BaseModel):
    name: str = Field(...,min_length=2,max_length=100)

class categoryresponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class menuitemcreate(BaseModel):
    category_id: int
    name: str = Field(...,min_length=2,max_length=150)
    description: Optional[str] = None
    price: float = Field(...,gt=0)
    image: Optional[str] = None
    is_veg: bool = True
    available: bool = True

class menuitemupdate(BaseModel):
    category_id: int
    name: str = Field(...,min_length=2,max_length=150)
    description: Optional[str] = None
    price: float = Field(...,gt=0)
    image: Optional[str] = None
    is_veg: bool 
    available: bool 



class menuitemresponse(menuitemcreate):
    id: int
    category_id: int | None = None
    name: str
    description: Optional[str]
    price: float
    image: Optional[str]
    is_veg: bool
    available: bool

    class Config:
        from_attributes = True

class restauranttablecreate(BaseModel):
    table_number: int = Field(...,gt=0)

class restauranttableupdate(BaseModel):
    table_number: int = Field(...,gt=0)
    is_active: bool

class restauranttableresponse(BaseModel):
    id: int
    table_number: int
    qr_code: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


class admincreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class adminlogin(BaseModel):
    username: str
    password: str

class adminresponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class adminupdate(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)

class token(BaseModel):
    access_token: str
    token_type: str

class orderitemcreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(...,gt=0)

class orderitemresponse(BaseModel):
    id:int
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class ordercreate(BaseModel):
    table_id: int
    payment_mode: PaymentMode
    customer_note: Optional[str] = None
    items : list[orderitemcreate]

class orderstatusupdate(BaseModel):
    order_status: OrderStatus

class paymentstatusupdate(BaseModel):
    payment_status: PaymentStatus

class orderresponse(BaseModel):
    id:int
    table_id: int
    total_amount: float
    payment_mode: str
    payment_status: str
    order_status: str
    customer_note: Optional[str]
    order_items: list[orderitemresponse]
    created_at: datetime

    class Config:
        from_attributes = True


class billitemresponse(BaseModel):
    item_name: str
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True

class billresponse(BaseModel):
    order_id: int
    table_id : int
    created_at: datetime
    items: list[billitemresponse]
    subtotal: float
    gst_rate_parcent: float = 5.0
    gst_amount: float
    service_charge: float = 0.0
    grand_total: float
    payment_status: str
    payment_mode: str | None = None



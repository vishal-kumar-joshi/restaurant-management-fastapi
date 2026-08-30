# models.py
from sqlalchemy import (Column,Integer,String,Text,DECIMAL,Boolean,ForeignKey,TIMESTAMP,Enum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from decimal import Decimal

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship
    menu_items = relationship("MenuItem", back_populates="category")



class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    name = Column(String(150), nullable=False)

    description = Column(Text)

    price = Column(DECIMAL(10,2), nullable=False)

    image = Column(String(255))

    is_veg = Column(Boolean, default=True)

    available = Column(Boolean, default=True)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
    category = relationship(
        "Category",
        back_populates="menu_items"
    )

    order_items = relationship(
        "orderitem",
        back_populates="menu_item"
    )


class restauranttable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True,index=True)

    table_number = Column(Integer,unique=True,nullable=False)

    qr_code = Column(String(255))
    is_active = Column(Boolean,default=True)

    orders = relationship("order", back_populates="table")

class admin(Base):
    __tablename__ = "admins"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True,index=True)
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"))

    total_amount = Column(DECIMAL(10,2), default=0)

    payment_mode = Column(Enum("cash","online", name = "payment_mode"))

    payment_status = Column(Enum("pending","paid","failed","refunded",name="payment_status"),default="pending")

    order_status = Column(Enum("pending","preparing","served","cancelled",name="order_status"),default="pending")

    customer_note = Column(Text)

    created_at = Column(TIMESTAMP,server_default=func.now())

    updated_at = Column(TIMESTAMP,server_default=func.now(),onupdate=func.now())

    table = relationship("restauranttable",back_populates="orders")

    order_items = relationship("orderitem",back_populates="order",cascade="all, delete-orphan")

class orderitem(Base):
    __tablename__ = "order_items"
    id = Column(Integer,primary_key=True,index=True)

    order_id = Column(Integer,ForeignKey("orders.id"))
    menu_item_id = Column(Integer,ForeignKey("menu_items.id"))

    quantity = Column(Integer,nullable=False)

    price = Column(DECIMAL(10,2),nullable=False)
    order = relationship("order",back_populates="order_items")
    menu_item = relationship("MenuItem",back_populates="order_items")


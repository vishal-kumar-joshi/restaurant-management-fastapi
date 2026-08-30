# order router
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas,crud,models
from app.services.order_service import orderservice
from utils.auth import get_current_admin
from decimal import Decimal


router = APIRouter(prefix="/orders",tags=["orders"])

@router.post("/",response_model=schemas.orderresponse,status_code=status.HTTP_201_CREATED)
def create_order(order_data: schemas.ordercreate,db: Session = Depends(get_db)):
    return orderservice.create_order(db, order_data)

@router.get("/",response_model=List[schemas.orderresponse])
def get_orders(db: Session = Depends(get_db),current_admin: models.admin = Depends(get_current_admin)):
    return crud.get_orders(db)

@router.get("/{order_id}", response_model=schemas.orderresponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return db_order

@router.patch("/{order_id}/status", response_model=schemas.orderresponse)
def update_order_status(
    order_id: int, 
    status_data: schemas.orderstatusupdate, 
    db: Session = Depends(get_db),
    current_admin: models.admin = Depends(get_current_admin)
):
    return orderservice.update_order_status(db, order_id, status_data)

@router.patch("/{order_id}/payment", response_model=schemas.orderresponse)
def update_payment_status(
    order_id: int, 
    status_data: schemas.paymentstatusupdate, 
    db: Session = Depends(get_db),
    current_admin: models.admin = Depends(get_current_admin)
):
    return orderservice.update_payment_status(db, order_id, status_data)

@router.delete("/{order_id}")
def delete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_admin: models.admin = Depends(get_current_admin)
):
    deleted_order = crud.delete_order(db, order_id)
    if not deleted_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return {"message": f"Order #{order_id} deleted successfully"}

gst_percentage = Decimal("5.0")

@router.get("/{order_id}/bill",response_model=schemas.billresponse)
def generate_order_bill(order_id: int,db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if  not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    bill_items = []
    subtotal = Decimal("0.00")

    for order_item in db_order.order_items:
        menu_item = crud.get_menu_item_by_id(db, order_item.menu_item_id)
        item_name = menu_item.name if menu_item else f"item #{order_item.menu_item_id}"

        item_total = order_item.price * order_item.quantity
        subtotal += item_total

        bill_items.append(schemas.billitemresponse(item_name=item_name,quantity=order_item.quantity,unit_price=float(order_item.price),total_price=float(item_total)))

    gst_amount = (subtotal * gst_percentage) / Decimal("100.00")
    grand_total = subtotal + gst_amount

    return schemas.billresponse(order_id=db_order.id,table_id=db_order.table_id,created_at=db_order.created_at,items=bill_items,subtotal=float(subtotal),gst_rate_parcent=float(gst_percentage),gst_amount=float(round(gst_amount, 2)),service_charge=0.0,grand_total=float(round(grand_total, 2)),payment_status=db_order.payment_status,payment_mode=db_order.payment_mode)


@router.post("/{order_id}/pay")
def process_order_payment(order_id: int,payment_mode: str,db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="order not found")
    if db_order.payment_status.lower() == "paid":
        raise HTTPException(status_code=400,detail="this order is already paid!")
    db_order.payment_status = "paid"
    db_order.payment_mode = payment_mode
    db_order.order_status = "served"

    table = crud.get_restaurant_tables_by_id(db, db_order.table_id)
    if table:
        table.is_active = True
    db.commit()

    return{
        "message" : "payment successful and order served!",
        "order_id" : order_id,
        "payment_mode" : payment_mode,
        "status" : "paid"
    }
       
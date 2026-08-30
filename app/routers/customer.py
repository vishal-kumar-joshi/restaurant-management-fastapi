# customer router
from datetime import datetime,timezone
from decimal import Decimal
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import crud,models,schemas
from app.database import get_db
from app.services.order_service import orderservice
from app.routers.websocket import manager

router = APIRouter(prefix="/customer", tags=["customer (scan & order)"])

@router.get("/menu",response_model=list[schemas.menuitemresponse])
def get_customer_menu(db: Session = Depends(get_db)):
    all_items = crud.get_menu_items(db)
    return [item for item in all_items if item.available]

@router.post("/order", response_model=schemas.orderresponse, status_code=status.HTTP_201_CREATED)
async def place_quick_order(order_data: schemas.ordercreate, db: Session = Depends(get_db)):
    new_order = orderservice.create_order(db, order_data)
    await manager.broadcast_new_order({
        "order_id" : new_order.id,"table_id" : new_order.table_id,"total_amount" : float(new_order.total_amount),"status": new_order.order_status})
    return new_order

@router.get("/order/{order_id}/status")
def track_order_live_status(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    return{
        "order_id": db_order.id,
        "table_id": db_order.table_id,
        "status": db_order.order_status,
        "payment_status": db_order.payment_status,
        "total_amount": db_order.total_amount,
        "created_at": db_order.created_at
    }


@router.delete("/order/{order_id}")
def cancel_order_by_customer(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )


    if str(db_order.order_status).lower() != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kitchen has already started preparing your order. Cannot cancel now!"
        )


    current_time = datetime.now(timezone.utc)
    order_time = db_order.created_at
    if order_time.tzinfo is None:
        order_time = order_time.replace(tzinfo=timezone.utc)

    time_diff = (current_time - order_time).total_seconds() / 60.0
    if time_diff > 5.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="5-minute cancellation window has expired."
        )

    
    db_order.order_status = "cancelled"
    db.commit()
    return {"message": "Order cancelled successfully", "order_id": order_id}


@router.put("/order/{order_id}", response_model=schemas.orderresponse)
def update_order_by_customer(
    order_id: int, 
    new_items: list[schemas.orderitemcreate], 
    db: Session = Depends(get_db)
):
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    if str(db_order.order_status).lower() != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already being prepared. Cannot modify items!"
        )

    current_time = datetime.now(timezone.utc)
    order_time = db_order.created_at
    if order_time.tzinfo is None:
        order_time = order_time.replace(tzinfo=timezone.utc)

    time_diff = (current_time - order_time).total_seconds() / 60.0
    if time_diff > 5.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="5-minute modification window has expired."
        )

    db.query(models.orderitem).filter(models.orderitem.order_id == order_id).delete()

    total_amount = Decimal("0.00")
    new_db_items = []

    for item in new_items:
        menu_item = crud.get_menu_item_by_id(db, item.menu_item_id)
        if not menu_item or not menu_item.available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Menu Item ID {item.menu_item_id} is unavailable or invalid"
            )

        item_price = Decimal(str(menu_item.price))
        total_amount += item_price * item.quantity

        new_db_items.append(
            models.orderitem(
                order_id=order_id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price=item_price
            )
        )

    db_order.total_amount = total_amount
    db.add_all(new_db_items)
    db.commit()
    db.refresh(db_order)

    return db_order



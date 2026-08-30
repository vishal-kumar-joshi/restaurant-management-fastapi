from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app import crud, models,schemas
from decimal import Decimal

class orderservice:
    @staticmethod
    
    def create_order(db: Session, order_data: schemas.ordercreate) -> models.order:
        table = crud.get_restaurant_tables_by_id(db, order_data.table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"table id {order_data.table_id} not found",)
        if not table.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this table is currently inactive",)

        total_amount = Decimal("0.00")
        db_order_items = []  

        if not order_data.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="order must contain at least one item",)
    
        
    
        for item in order_data.items:
            menu_item = crud.get_menu_item_by_id(db, item.menu_item_id)
            if not menu_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"menu item id {item.menu_item_id} not found",)
            if not menu_item.available:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"menu item '{menu_item.name}' is currently unavailable",)
            if menu_item.price is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Price for '{menu_item.name}' (ID: {menu_item.id}) is not set in the database."
                )
    
            item_price = Decimal(str(menu_item.price))
            total_amount += item_price * item.quantity
    
        # ✅ Dhyan dein: models.orderitem(...) directly object append hoga
            order_item = models.orderitem(menu_item_id=item.menu_item_id, quantity=item.quantity,price = item_price)
            db_order_items.append(order_item)
    
      # ✅ BOHOT IMPORTANT:
      # Check karein ki 'new_order = ...' FOR LOOP KE BAAHAR (unindented) hai
        new_order = models.order(
          table_id=order_data.table_id,
          total_amount=total_amount,
          payment_mode=order_data.payment_mode,
          customer_note=order_data.customer_note,
          order_items=db_order_items,
      )
    
        return crud.create_order(db, new_order)

    @staticmethod
    def update_order_status(db: Session, order_id: int, status_data: schemas.orderstatusupdate):
        allowed_statuses = ["pending", "preparing", "served", "cancelled"]
        if status_data.order_status not in allowed_statuses:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"invalid status. allowed values: {allowed_statuses}")
        updated_order = crud.update_order_status(db, order_id, status_data.order_status)
        if not updated_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
        return updated_order
    
    @staticmethod
    def update_payment_status(db: Session, order_id: int, status_data: schemas.paymentstatusupdate):
        allowed_statuses = ["pending", "paid", "failed", "refunded"]
        if status_data.payment_status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"invalid status. allowed values: {allowed_statuses}"
            )
        updated_order = crud.update_payment_status(db, order_id,status_data.payment_status)
        if not updated_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
        return updated_order
        
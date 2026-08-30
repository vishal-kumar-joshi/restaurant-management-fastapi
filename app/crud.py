# crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from utils.security import hash_password,verify_password

def create_category(db: Session, category: schemas.categorycreate):
    db_category = models.Category(name=category.name)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category_by_id(db: Session, category_id: int):
    return(
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )

def update_category(db: Session, category_id: int,category:schemas.categoryupdate):
    db_category = get_category_by_id(db,category_id)
    if not db_category:
        return None
    
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session,category_id: int):
    db_category = get_category_by_id(db,category_id)
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category


# menu module

def create_menu_item(db: Session, item: schemas.menuitemcreate):
    db_item = models.MenuItem(
category_id=item.category_id,
        name = item.name,

description=item.description,
        price=item.price,
        image=item.image,
        is_veg = item.is_veg,
        available=item.available

    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def get_menu_items(db: Session):
    return db.query(models.MenuItem).all()


def get_menu_item_by_id(db: Session,menu_item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()

def update_menu_item(db: Session,menu_item_id: int,item: schemas.menuitemupdate):
    db_item = get_menu_item_by_id(db, menu_item_id)
    if db_item is None:
        return None
    
    db_item.category_id = item.category_id
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.image = item.image
    db_item.is_veg = item.is_veg
    db_item.available = item.available

    db.commit()
    db.refresh(db_item)
    return db_item



def delete_menu_item(db: Session,menu_item_id: int):
    db_item = get_menu_item_by_id(db,menu_item_id)

    if db_item is None:
        return None
    db.delete(db_item)
    db.commit()

    return db_item

def toggle_menu_availability(db: Session, menu_item_id: int):
    db_item = get_menu_item_by_id(db,menu_item_id)
    if db_item is None:
        return None
    db_item.available = not db_item.available
    db.commit()
    db.refresh(db_item)
    return db_item


# restorent table crud

def create_restaurant_table(db: Session,table: schemas.restauranttablecreate):
    db_table = models.restauranttable(table_number=table.table_number)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)

    return db_table

def get_restaurant_tables(db: Session):
    return db.query(models.restauranttable).all()

def get_restaurant_tables_by_id(db: Session, table_id: int):
    return(
        db.query(models.restauranttable).filter(models.restauranttable.id == table_id).first()
    )

def update_restaurant_table(db: Session, table_id: int, table: schemas.restauranttableupdate):
    db_table = get_restaurant_tables_by_id(db,table_id)

    if db_table is None:
        return None
    db_table.table_number = table.table_number
    db_table.is_active = table.is_active
    db.commit()
    db.refresh(db_table)

    return db_table

def delete_restaurant_table(db: Session, table_id: int):
    db_table = get_restaurant_tables_by_id(db,table_id)
    if db_table is None:
        return None
    
    db.delete(db_table)
    db.commit()

    return db_table

def toggle_table_stutas(db: Session, table_id: int):
    db_table = get_restaurant_tables_by_id(db,table_id)
    if db_table is None:
        return None
    db_table.is_active = not db_table.is_active
    db.commit()
    db.refresh(db_table)
    return db_table



# admin crud
def create_admin(db: Session, username: str, password: str):
    db_admin = models.admin(username=username,password=hash_password(password))
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return db_admin

def get_admins(db: Session):
    return db.query(models.admin).all()

def get_admin_by_id(db: Session, admin_id: int):
    return(db.query(models.admin).filter(models.admin.id == admin_id).first())

def get_admin_by_username(db: Session,username: str):
    return(db.query(models.admin).filter(models.admin.username == username).first())

def update_admin(db: Session,admin_id: int,admin: schemas.adminupdate):
    db_admin = get_admin_by_id(db,admin_id)
    if db_admin is None:
        return None
    db_admin.username = admin.username
    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session,admin_id: int):
    db_admin = get_admin_by_id(db,admin_id)
    if db_admin is None:
        return None
    db.delete(db_admin)
    db.commit()

    return db_admin

def authenticate_admin(db: Session,username: str,password: str):
    admin = get_admin_by_username(db,username)
    if not admin:
        return None
    if not verify_password(password,admin.password):
        return None
    return admin


# order crud

def create_order(db: Session,order: models.order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session):
    return db.query(models.order).all()

def get_order_by_id(db: Session,order_id: int):
    return(db.query(models.order).filter(models.order.id == order_id).first())

def update_order(db: Session,order_id: int,order: schemas.ordercreate):
    db_order = get_order_by_id(db,order_id)
    if db_order is None:
        return None
    
    db_order.table_id = order.table_id
    db_order.payment_mode = order.payment_mode
    db_order.customer_note = order.customer_note
    db.commit()
    db.refresh(db_order)

    return db_order


def update_order_status(db: Session,order_id: int,status: str):
    db_order = get_order_by_id(db,order_id)
    if db_order is None:
        return None
    
    db_order.order_status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def update_payment_status(db: Session, order_id: int,status: str):
    db_order = get_order_by_id(db,order_id)
    if db_order is None:
        return None
    db_order.payment_status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session,order_id: int):
    db_order = get_order_by_id(db,order_id)
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order
    
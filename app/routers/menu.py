# menu router
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/menu",tags=["menu"])


@router.post("/",response_model=schemas.menuitemresponse,status_code=status.HTTP_201_CREATED)
def create_menu_item(item: schemas.menuitemcreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db, item)

@router.get("/", response_model=list[schemas.menuitemresponse])
def get_menu_items(db: Session = Depends(get_db)):
    return crud.get_menu_items(db)

@router.get("/{menu_item_id}",response_model=schemas.menuitemresponse)
def get_menu_item(menu_item_id: int,db: Session = Depends(get_db)):
    item = crud.get_menu_item_by_id(db,menu_item_id)
    if item is None:
        raise HTTPException(status_code=404,detail="menu item not found")
    return item

@router.put("/{menu_item_id}",response_model=schemas.menuitemresponse)
def update_menu_item(menu_item_id: int,item: schemas.menuitemupdate,db: Session = Depends(get_db)):
    updated = crud.update_menu_item(db,menu_item_id,item)
    if updated is None:
        raise HTTPException(status_code=404,detail="menu item not found")
    return updated

@router.delete("/{menu_item_id}")
def delete_menu_item(menu_item_id: int,db: Session = Depends(get_db)):
    deleted = crud.delete_menu_item(db, menu_item_id)
    if deleted is None:
        raise HTTPException(status_code=404,detail="menu item not found")
    return{
        "message": "menu item deleted successfully"
    }

@router.patch("/{menu_item_id}/availability")
def toggle_menu_availability(menu_item_id: int, db: Session = Depends(get_db)):
    item = crud.toggle_menu_availability(db,menu_item_id)
    if item is None:
        raise HTTPException(
            status_code=404,detail="menu item not found"
        )
    return{"message" : "availability updated successfully","available" : item.available}

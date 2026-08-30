# restorent table
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/restaurant-table",tags=["restaurant table"])

@router.post("/", response_model=schemas.restauranttableresponse)
def create_restaurant_table( table: schemas.restauranttablecreate, db:Session = Depends(get_db)):
    return crud.create_restaurant_table(db, table)

@router.get("/",response_model=list[schemas.restauranttableresponse])
def get_restaurant_tables(db: Session = Depends(get_db)):
    return crud.get_restaurant_tables(db)

@router.get("/{table_id}",response_model=schemas.restauranttableresponse)
def get_restaurant_table(table_id: int,db: Session = Depends(get_db)):
    table = crud.get_restaurant_tables_by_id(db,table_id)

    if not table:
        raise HTTPException(status_code=404,detail="table not found")
    return table

@router.put("/{table_id}",response_model=schemas.restauranttableresponse)
def update_restaurant_table(table_id: int,table: schemas.restauranttableupdate, db: Session = Depends(get_db)):
    update_table = crud.update_restaurant_table(db,table_id,table)

    if not update_table:
        raise HTTPException(status_code=404,detail="restaurant table not found")
    return update_table

@router.delete("/{table_id}")
def delete_restaurant_table(table_id: int,db: Session = Depends(get_db)):
    deleted_table = crud.delete_restaurant_table(db,table_id)
    if not deleted_table:
        raise HTTPException(status_code=404, detail="restaurant table not found")
    return{
        "message":"restaurant table deleted successfully"
    }


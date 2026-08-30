# category router
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from fastapi import status

router = APIRouter(prefix="/categories",tags=["Categories"])

@router.post("/",response_model=schemas.categoryresponse,status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.categorycreate, db: Session = Depends(get_db)
):
    return crud.create_category(db,category)


@router.get("/",response_model=list[schemas.categoryresponse])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@router.get("/{category_id}",response_model=schemas.categoryresponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(status_code=404,detail="category not found")
    return category

@router.put("/{category_id}", response_model=schemas.categoryresponse)
def update_category(category_id: int, category: schemas.categoryupdate,db: Session = Depends(get_db)):
    updated = crud.update_category(db,category_id,category)
    if updated is None:
        raise HTTPException(status_code=404,detail="Category not found")

    return updated

@router.delete("/{category_id}")
def delete_category(category_id: int,db: Session = Depends(get_db)):
    deleted = crud.delete_category(db,category_id)
    if deleted is None:
        raise HTTPException(status_code=404,detail="Category not found")
    return {
        "message": "Category deleted successfully"
    }
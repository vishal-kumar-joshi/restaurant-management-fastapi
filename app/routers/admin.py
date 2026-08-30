# admin router
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, models
from utils.auth import get_current_admin

router = APIRouter(prefix="/admin",tags=["admin"])

@router.post("/",response_model=schemas.adminresponse, status_code=status.HTTP_201_CREATED)
def create_admin(admin: schemas.admincreate, db: Session = Depends(get_db)):
   existing_admin = crud.get_admin_by_username(db,admin.username)

   if existing_admin:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username already exists")
   return crud.create_admin(db,admin.username,admin.password)


@router.get("/",response_model=list[schemas.adminresponse])
def get_admins(db: Session = Depends(get_db),current_admin = Depends(get_current_admin)):
   return crud.get_admins(db)

@router.get("/{admin_id}",response_model=schemas.adminresponse)
def get_admin_by_id(admin_id: int,db: Session = Depends(get_db),current_admin: models.admin = Depends(get_current_admin)):
   db_admin = crud.get_admin_by_id(db,admin_id)

   if db_admin is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="admin not found")
   return db_admin

@router.put("/{admin_id}",response_model=schemas.adminresponse)
def update_admin(admin_id: int,admin: schemas.adminupdate,db: Session = Depends(get_db),current_admin: models.admin = Depends(get_current_admin)):

   db_admin = crud.update_admin(db,admin_id,admin)

   if db_admin is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="admin not found")
   return db_admin


@router.delete("/{admin_id}")
def delete_admin(admin_id : int,db: Session = Depends(get_db),current_admin: models.admin = Depends(get_current_admin)):
   db_admin = crud.delete_admin(db,admin_id)
   if db_admin is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="admin not found")
   return{
      "message": "admin deleted successfully"
   }


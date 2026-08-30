from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from utils.security import create_access_token,verify_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login",response_model=schemas.token)
def login(from_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    admin = crud.authenticate_admin(db,from_data.username,from_data.password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect username or password",headers={"www-authenticate" : "Bearer"},)
    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token" : access_token, "token_type": "Bearer"}

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid or expired token",headers={"www-authenticate" : "Bearer"},)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token payload")
    admin = crud.get_admin_by_username(db, username = username)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="admin not found")
    return admin
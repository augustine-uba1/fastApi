from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
import app.models, app.schemas, app.utils

from sqlalchemy.orm import Session
from app.database import get_db, engine

router = APIRouter(
    prefix="/users",
    tags=['users']
) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=app.schemas.UserOut)
def create_user(user : app.schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash user password in user.password
    harshed_password = app.utils.hash(user.password)
    user.password = harshed_password
    new_user = app.models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{id}", response_model=app.schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(app.models.Users).filter(app.models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} not found")
    return user
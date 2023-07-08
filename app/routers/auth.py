from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

import models, schemas, database, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials : schemas.UserLogin, db: Session = Depends(database.get_db) ):
    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    # CREATE TOKEN AND RETURN TOKEN
    return {"teken": "user token"}
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

import models, schemas, database, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
# def login(user_credentials : schemas.UserLogin, db: Session = Depends(database.get_db) ):
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , 
          db: Session = Depends(database.get_db) ):
    
    user = db.query(models.Users).filter(
        models.Users.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    # CREATE TOKEN AND RETURN TOKEN
    return {"access token": access_token, "token_type": "bearer"}
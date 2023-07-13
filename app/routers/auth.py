from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

import app.models, app.schemas, app.database, app.utils, app.oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model= app.schemas.Token)
# def login(user_credentials : app.schemas.UserLogin, db: Session = Depends(app.database.get_db) ):
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , 
          db: Session = Depends(app.database.get_db) ):
    
    user = db.query(app.models.Users).filter(
        app.models.Users.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    if not app.utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    access_token = app.oauth2.create_access_token(data= {"user_id": user.id})
    
    # CREATE TOKEN AND RETURN TOKEN
    return {"access_token": access_token, "token_type": "bearer"}
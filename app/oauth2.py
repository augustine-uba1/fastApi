from datetime import datetime, timedelta
from jose import JWSError, jwt
import app.schemas, app.database, app.models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# Expiration Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_data

def veriy_access_token(token : str, credentials_exception):
    
    try: 
        
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = app.schemas.TokenData(id= id)
    
    except JWSError: 
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(app.database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Unable to validate credentials",
                                          headers= {"WWW-Authenticate": "Bearer"})
    
    
    token = veriy_access_token(token, credentials_exception)
    user = db.query(app.models.Users).filter(app.models.Users.id == token.id).first()
    print(user)
    return user
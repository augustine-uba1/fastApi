from datetime import datetime, timedelta
from jose import JWSError, jwt
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# Expiration Time

SECRET_KEY = "b7b2818a7445e55c44569eb9c777d9ba18a219e66b2eee71175f10dcf20f6221"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_data

def veriy_access_token(token : str, credentials_exception):
    
    try: 
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id= id)
    
    except JWSError: 
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Unable to validate credentials",
                                          headers= {"WWW-Authenticate": "Bearer"})
    
    return veriy_access_token(token, credentials_exception)
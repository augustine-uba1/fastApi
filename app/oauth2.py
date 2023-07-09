from datetime import datetime, timedelta
from jose import JWSError, jwt

# SECRET_KEY
# Algorithm
# Expiration Time

SECRET_KEY = "b7b2818a7445e55c44569eb9c777d9ba18a219e66b2eee71175f10dcf20f6221"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_data
# import bcrypt

# def hash_password(password: str) -> str:
#     pwd_bytes = password.encode('utf-8')
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(pwd_bytes,salt)

#     return hashed.decode('utf-8')

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     pwd_bytes = plain_password.encode('utf-8')
#     hashed_bytes = hashed_password.encode('utf-8')
#     return bcrypt.checkpw(pwd_bytes, hashed_bytes)



from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt

from app.config import secret_key, algorithm, access_token_expire_minitues

#  JWT Access Token Create Karne Ke Liye
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minitues)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

#  JWT Token Decode/Verify Karne Ke Liye 
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None

#  Password Hashing 
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)
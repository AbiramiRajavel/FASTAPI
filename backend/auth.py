from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .table_schemas import User
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def authenticate_user(request, db):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return False
    if not verify_password(request.password, user.password):
        return False

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except Exception as e:
        raise credentials_exception
    
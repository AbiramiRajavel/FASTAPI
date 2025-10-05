from fastapi import APIRouter, Depends, status, HTTPException

from backend.dbalchemy import get_db
from backend.schemas import LoginSchema
from backend.auth import authenticate_user

router = APIRouter(prefix="", tags=["User Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginSchema, db=Depends(get_db)):
    token = authenticate_user(request, db)
    if token:
        return token
    if not authenticate_user(request, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"message": "Login failed"}

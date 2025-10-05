from fastapi import APIRouter, Depends, status, HTTPException, Response

from backend.dbalchemy import get_db
from backend.schemas import LoginSchema
from backend.auth import authenticate_user

router = APIRouter(prefix="", tags=["User Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginSchema, response: Response, db=Depends(get_db)):
    token = authenticate_user(request, db)
    if token:
        return token
    if not authenticate_user(request, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Set HttpOnly cookies
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     httponly=True,  # Prevents JavaScript access
    #     secure=True,    # HTTPS only (set to False for local development)
    #     samesite="strict",  # CSRF protection
    #     max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    # )

    return {"message": "Login failed"}

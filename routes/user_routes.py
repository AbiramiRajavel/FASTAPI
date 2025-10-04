from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from backend.schemas import UserCore
from backend.dbalchemy import get_db
from backend.user_curd import (
    get_all_user,
    create_user,
    get_user_id,
    update_user_id,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["User Operations"])


@router.get(
    "/allusers",
    response_model=List[UserCore],
)
def get_all_users(db=Depends(get_db)):
    users = get_all_user(db)
    return users


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user_endpoint(request_body: UserCore, db=Depends(get_db)):
    user = create_user(request_body, db)
    return user


@router.post("/get_user/{id}", status_code=status.HTTP_201_CREATED)
def get_user_endpoint(id: int, db=Depends(get_db)):
    user = get_user_id(id, db)
    return user


@router.put("/update_user/{id}", response_model=UserCore)
def update_user_endpoint(id: int, request_body: UserCore, db=Depends(get_db)):
    user = update_user_id(id, request_body, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/delete_user/{id}", response_model=UserCore)
def delete_user_endpoint(id: int, db=Depends(get_db)):
    user = delete_user(id, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

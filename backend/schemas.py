from pydantic import BaseModel, EmailStr, constr

class UserName(BaseModel):
    name: str
    
class UserCore(BaseModel):
    name: str
    age: int
    # Limit password length to 72 bytes (bcrypt's limit) and minimum 8 characters
    password: constr(min_length=8, max_length=72)
    email: str
    
class UserORM(BaseModel):
    name: str
    email: str
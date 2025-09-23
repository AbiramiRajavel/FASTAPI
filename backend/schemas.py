from pydantic import BaseModel

class UserName(BaseModel):
    name: str
    
class UserCore(BaseModel):
    name: str
    age: int
    
class UserORM(BaseModel):
    name: str
    email: str
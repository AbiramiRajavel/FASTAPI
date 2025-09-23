from fastapi import FastAPI, Body, Depends, status, HTTPException
from middleware import add_cors
from backend.core_vs_orm import get_user_core, get_user_orm
from backend.schemas import UserName
from typing import List
from backend.dbalchemy import create_connection_pool, User2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

app= FastAPI()
add_cors(app)

@app.get("/")
def read_root():
    dictn={"name":"abi","fut":"alien"}
    return dictn


@app.get('/id/{id}')
def getid(id:int):
    return {'id':id}

@app.get('/blog')
def getblog(limit,flag:bool):
    print(limit,'limittt',type(flag),flag)
    if flag==True:
        return {'data':f'blog limit to {limit}'}
    else:
        return {'data':'all blogs'}


@app.post('/blog')
def postblog(data:dict=Body(...)): 
    print(type(data))
    return {"updated name":data}

def user_validation(): 
    return {'name':'abi','age':22}

@app.put('/user')
def update_user(data:dict=Depends(user_validation)):
     print(data)
     return data 
 
@app.get('/user',status_code=status.HTTP_202_ACCEPTED, response_model=List[UserName])
def get_user(data:dict=Depends(user_validation)):
    users=get_user_orm()
    for user in users:
        user_dict = {key: value for key, value in user.__dict__.items() 
                    if not key.startswith('_')}
        print(user_dict)
    return users

@app.post('/user/core', status_code=status.HTTP_201_CREATED)
def create_user_core(name: str, age: int):
    try:
        engine = create_connection_pool()
        with engine.connect() as conn:
            insert_stmt = text("INSERT INTO users (name, age) VALUES (:name, :age)")
            conn.execute(insert_stmt, {"name": name, "age": age})
            conn.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/user/orm', status_code=status.HTTP_201_CREATED)
def create_user_orm(name: str, email: str):
    try:
        engine = create_connection_pool()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        user = User2(name=name, email=email)
        session.add(user)
        session.commit()
        session.close()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
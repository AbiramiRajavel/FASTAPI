from fastapi import FastAPI, Body, Depends, status, HTTPException, Response
from middleware import add_cors
from backend.core_vs_orm import get_user_core, get_user_orm
from backend.schemas import UserName
from typing import List
from backend.dbalchemy import create_connection_pool, User2,get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from backend.user_curd import get_all_user, create_user, get_user_id,update_user_id, delete_user
from backend.schemas import UserCore

app = FastAPI()
add_cors(app)

# Create tables on startup
from backend.dbalchemy import create_tables
create_tables()

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
 
@app.get('/user',status_code=status.HTTP_202_ACCEPTED)
def get_user(response: Response, data:dict=Depends(user_validation)):
    users=get_user_orm()
    for user in users:
        user_dict = {key: value for key, value in user.__dict__.items() 
                    if not key.startswith('_')}
    response.status_code=status.HTTP_200_OK
    print(response,'rsponse')
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
    
# ----user curd operations---    

@app.get('/allusers', response_model=List[UserCore])
def get_all_users(db=Depends(get_db)):
    users = get_all_user(db)
    return users

@app.post('/create_user', status_code=status.HTTP_201_CREATED)   
def create_user_endpoint(request_body: UserCore, db=Depends(get_db)):
    user = create_user(request_body, db)
    return user

@app.post('/get_user/{id}', status_code=status.HTTP_201_CREATED)   
def get_user_endpoint(id: int, db=Depends(get_db)):
    user = get_user_id(id, db)
    return user

@app.put('/update_user/{id}', response_model=UserCore)
def update_user_endpoint(id: int, request_body: UserCore, db=Depends(get_db )):
    user = update_user_id(id, request_body, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")   

@app.delete('/delete_user/{id}', response_model=UserCore)
def delete_user_endpoint(id: int, db=Depends(get_db)):
    user = delete_user(id, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
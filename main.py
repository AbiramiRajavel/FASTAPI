from fastapi import FastAPI, Body
from middleware import add_cors
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


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=9000)
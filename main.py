from fastapi import FastAPI
from middleware import add_cors
app= FastAPI()
add_cors(app)

@app.get("/")
def read_root():
    dictn={"name":"abi","fut":"alien"}
    return dictn



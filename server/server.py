from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
users = {} 

class RegisterRequest(BaseModel):
    username: str
    public_key: str

@app.post("/register")
def register_user(data: RegisterRequest):
    if data.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[data.username] = data.public_key
    return {"status": "registered"}

@app.get("/key/{username}")
def get_public_key(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"public_key": users[username]}

@app.get("/users")
def list_users():
    return {"users": list(users.keys())}

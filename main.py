from fastapi import FastAPI, Header, HTTPException
from models import PostSchema

import secrets
import database as db

app = FastAPI()

@app.get("/")
async def hello():
    return "hello"

@app.post("/everything/")
async def get_body(item:PostSchema, auth:str=Header(None)):
    everything = {
        "body":item,
        "headers": auth
    }
    return everything

@app.post("/signup")
async def add_new_user(user_details:PostSchema):
    db.insert_new_user(user_details)
 
@app.get("/user")
async def user_details(sessionToken:str=Header(None)):
    if sessionToken is None:
        raise HTTPException(status_code=400, detail='session_token not found in request header')
    return db.get_user_details(sessionToken).model_dump()

@app.get("/login")
async def login(uid:str=Header(None)):
    if uid is None:
        raise HTTPException(status_code=400, detail='uid not found in request header')
    if len(uid.strip()) != 4:
        raise HTTPException(status_code=400, detail=f'Invalid uid: {uid}')
    session_token = secrets.token_urlsafe(16)
    db.insert_session_token(uid=uid.strip().lower(), session_token=session_token)
    
    return {'sessionToken': session_token}


import json
from fastapi import FastAPI, Header, HTTPException, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from models import PostSchema

import secrets
import database as db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
async def hello():
    return "hello"

@app.post("/signup")
async def add_new_user(user_details:PostSchema):
    db.insert_new_user(user_details)
    db.insert_skills(user_details.skills)

@app.get("/user")
async def user_details(ment2b_session:str=Cookie(None)):
    if ment2b_session is None:
        raise HTTPException(status_code=400, detail='session_token not found in request header')
    return db.get_user_details(ment2b_session).model_dump()

@app.get("/login")
async def login(uid:str=Header(None)):
    if uid is None:
        raise HTTPException(status_code=400, detail='uid not found in request header')
    if len(uid.strip()) != 4:
        raise HTTPException(status_code=400, detail=f'Invalid uid: {uid}')
    session_token = secrets.token_urlsafe(16)
    db.insert_session_token(uid=uid.strip().lower(), session_token=session_token)
    
    res = Response(status_code=200, content='Successfully logged in')
    res.set_cookie('ment2b_session', session_token)
    return res

@app.get("/skills")
async def get_matching_skills(skillSubstring:str):
    return db.match_skills(skillSubstring)
    
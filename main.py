import json
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import PostSchema

import secrets
import database as db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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

@app.get("/skills")
async def get_matching_skills(skillSubstring:str):
    return db.match_skills(skillSubstring)
    
@app.get("/match")
async def match_mentors(sessionToken:str=Header(None)):
    if sessionToken is None:
        raise HTTPException(status_code=400, detail='session_token not found in request header')
    
    # Get relevant details needed to match on 
    curr_user_data = db.get_user_details(session_token=sessionToken)
    potential_match_data = db.get_user_match_data(desired_grades=curr_user_data.desired_grades)
    
    # TODO send off to matching engine
    # potential_match_data format:
    # [
    #    {'uid': 'dddd', 'skills': [...]}, 
    #    {'uid': 'iiii', 'skills': [...]}
    #  ]

    return 'hey'

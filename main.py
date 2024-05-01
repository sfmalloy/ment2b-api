from fastapi import FastAPI, Header, HTTPException, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from models import PostSchema
import logging
from ment2matcher import ment2b

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

logger = logging.getLogger('uvicorn')

@app.get("/")
async def hello():
    return "hello"

@app.post("/signup")
async def add_new_user(user_details:PostSchema):
    db.insert_new_user(user_details)
    db.insert_skills(user_details.skills)

@app.put("/update")
async def update_user_details(user_details:PostSchema):
    db.update_user_details(user_details)
    
@app.get("/user")
async def user_details(ment2b_session:str=Cookie(None)):
    if ment2b_session is None:
        raise HTTPException(status_code=400, detail='session_token not found in cookie')
    return db.get_user_details(ment2b_session).model_dump()

@app.get("/login")
async def login(uid:str=Header(None)):
    logger.info('Validating UID')
    if uid is None:
        raise HTTPException(status_code=400, detail='uid not found in request header')
    if len(uid.strip()) != 4:
        raise HTTPException(status_code=400, detail=f'Invalid uid: {uid}')
    
    try:
        logger.info('Generating session')
        session_token = secrets.token_urlsafe(16)
        db.insert_session_token(uid=uid.strip().lower(), session_token=session_token)
        logger.info('Grabbing user information')
        db.get_user_details(session_token)

    except HTTPException as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail='User not found')
    except Exception as e:
        logger.error(e)

    logger.info('Generating login response')
    res = Response(status_code=200, content='Successfully logged in')
    res.set_cookie('ment2b_session', session_token, max_age=1800, httponly=True, secure=True)
    return res

@app.get("/logout")
async def logout(ment2b_session:str=Cookie(None)):
    db.delete_session_token(ment2b_session)
    res = Response(status_code=200, content='Successfully logged out')
    res.delete_cookie('ment2b_session')
    return res

@app.get('/auth')
async def check_cookie(ment2b_session:str=Cookie(None)):
    if not ment2b_session:
        return Response(status_code=401)
    return Response(status_code=200)

@app.get("/skills")
async def get_matching_skills(skillSubstring:str):
    return db.match_skills(skillSubstring)
    
@app.get("/match")
async def match_mentors(ment2b_session:str=Cookie(None)):
    if not ment2b_session:
        raise HTTPException(status_code=400, detail='session_token not found in cookie')
    
    # Get relevant details needed to match on 
    curr_user_data = db.get_user_details(session_token=ment2b_session)
    potential_match_data = db.get_user_match_data(desired_grades=curr_user_data.desired_grades)
    ment2matches = ment2b(ment2b_session, curr_user_data, potential_match_data)

    return ment2matches

@app.get("/questions")
async def get_mentor_questions(ment2b_session:str=Cookie(None), mentorUid:str=Header(None)):
    if not ment2b_session:
        raise HTTPException(status_code=400, detail='session_token not found in cookie')
    if not mentorUid:
        raise HTTPException(status_code=400, detail='mentorUid not found in header')

    curr_user_data = db.get_user_details(session_token=ment2b_session)
    mentors_user_data = db.get_user_details(session_token=ment2b_session, uid=mentorUid)

    return {
        'questions': None
    }
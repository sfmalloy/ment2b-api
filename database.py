import sqlite3
import logging
from typing import List
from models import PostSchema
from fastapi import HTTPException

connection = sqlite3.connect('ment2b.db')
logger = logging.getLogger('uvicorn')

def insert_session_token(uid:str, session_token:str):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sessions(
                session_token string PRIMARY KEY,
                uid string
            )
        ''')
        cursor.execute(f"INSERT INTO Sessions VALUES (?,?)", (session_token, uid))
        connection.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'DB Exception occurred: {e}')

def delete_session_token(session_token:str):
    try:
        cursor = connection.cursor()
        cursor.execute(f'''
            DELETE FROM Sessions
            WHERE session_token = "{session_token}"
        ''')
        connection.commit()
        cursor.close()
    except:
        logger.error('Could not find session token to delete')
        pass

def get_uid_from_session_token(session_token:str):
    try:
        cursor = connection.cursor()
        result = cursor.execute(f"SELECT uid FROM Sessions WHERE session_token='{session_token}'")
        row = result.fetchone()
        cursor.close()
        return row[0]
    except TypeError:
        raise HTTPException(status_code=400, detail='Session Token not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'DB Exception occurred: {e}')

def insert_new_user(user_details:PostSchema):
    user_dict = user_details.model_dump()
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
                uid string PRIMARY KEY,
                first_name string,
                last_name string,
                email string, 
                grade string, 
                position string,
                sub_division string, 
                skills string,
                desired_skills string,
                desired_grades string,
                open_to_mentor string,
                open_to_be_mentored string
            )
        ''')
        cursor.execute(
            "INSERT INTO Users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                user_dict.get('uid', "").strip().lower(),
                user_dict.get('first_name', "").strip(),
                user_dict.get('last_name', "").strip(),
                user_dict.get('email', "").strip(),
                user_dict.get('grade', "").strip(),
                user_dict.get('position', "").strip(),
                user_dict.get('sub_division', "").strip(),
                user_dict.get('profile_description', "").strip(),
                ','.join(user_dict.get('skills', [])),
                ','.join(user_dict.get('desired_skills', [])),
                ','.join(user_dict.get('desired_grades', [])),
                user_dict.get('open_to_mentor'),
                user_dict.get('open_to_be_mentored'),
            )
        )
        
        connection.commit()
        cursor.close()
    except sqlite3.IntegrityError as e:
        if e.sqlite_errorname == 'SQLITE_CONSTRAINT_PRIMARYKEY':
            raise HTTPException(status_code=400, detail=f'User already exists')    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'DB Exception occurred: {e}')

def get_user_details(session_token:str) -> PostSchema:
    uid = get_uid_from_session_token(session_token)
    try:
        cursor = connection.cursor()
        result = cursor.execute(f"SELECT * FROM Users WHERE uid='{uid}'")
        row = result.fetchone()
        cursor.close()
        user_details = PostSchema(
            uid=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            grade=row[4],
            position=row[5],
            sub_division=row[6],
            profile_description=row[7],
            skills=row[8].split(','),
            desired_skills=row[9].split(','),
            desired_grades=row[10].split(','),
            open_to_mentor=row[11],
            open_to_be_mentored=row[12]
        )
        return user_details

    except TypeError:
        raise HTTPException(status_code=400, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'DB Exception occurred: {e}')

def update_user_details(user_details:PostSchema):
    try:
        user_dict = user_details.model_dump()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM Users")
        print(result.fetchall())
        cursor.execute(f'''
            UPDATE Users
            SET skills = ?, open_to_mentor = ?
            WHERE uid = ?                   
        ''', (','.join(user_dict.get('skills')), user_dict.get('open_to_mentor'), user_dict.get('uid').strip().lower()))
        connection.commit()
        print('User has been updated successfully!')
        result = cursor.execute("SELECT * FROM Users")
        print(result.fetchall())
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'DB Exception occurred: {e}')
    
def insert_skills(skills:List[str]):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Skills(
                skill UNIQUE
            )
        ''')
        for i in skills:
            try:
                cursor.execute(f"INSERT INTO Skills (skill) VALUES ('{i}')")
            except sqlite3.IntegrityError as e:
                if e.sqlite_errorname != 'SQLITE_CONSTRAINT_UNIQUE':
                    raise
        connection.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'DB Exception occurred: {e}')

def match_skills(skill_substring:str) -> List[str]:
        cursor = connection.cursor()
        matching_skills = []
    
        result = cursor.execute(f'''
            SELECT skill from Skills WHERE skill LIKE '%{skill_substring}%'
        ''')
        for i in result.fetchall():
            matching_skills.append(i[0])
         
        cursor.close()
        return matching_skills

def get_user_match_data(desired_grades):
    '''
    Pulls back all mentors in desired grades
    '''
    cursor = connection.cursor()

    potential_match_data = []

    for grade in desired_grades:
        result = cursor.execute(f'''
            SELECT uid, desired_skills
            FROM Users
            WHERE open_to_mentor = 1
            AND grade = "{grade}" 
        ''')

        for i in result.fetchall():
            potential_match_data.append({
                'uid': i[0],   
                'skills': i[1].split(',')
            })
        
    cursor.close()
    return potential_match_data

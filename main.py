from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Header

app = FastAPI()

class Item(BaseModel):
    uid: str
    first_name: str
    last_name: str
    email: str
    grade: str
    postion: str
    sub_division: str

    skills: List[str]
    desired_skills: List[str]
    desired_grades: List[str]

    open_to_mentor: bool

@app.post("/everything/")
async def get_body(item:Item, auth:str=Header(None)):
    everything = {
        "body":item,
        "headers": auth
    }
    return everything
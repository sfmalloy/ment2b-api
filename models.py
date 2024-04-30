from pydantic import BaseModel 
from typing import List, Optional

class PostSchema(BaseModel):
    uid: str
    first_name: str
    last_name: str
    email: Optional[str]
    grade: str
    position: str
    sub_division: Optional[str]

    skills: List[str]
    desired_skills: Optional[List[str]]
    desired_grades: Optional[List[str]]

    open_to_mentor: bool
    open_to_be_mentored: bool

test_json = '''{
    "uid": "____",
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnny_smit@example.com",
    "grade": "A+",
    "position": "Developer",
    "sub_division": "BRO",
    "skills": [
        "chillin",
        "click clackin on the keyboard",
        "ghouls"
    ],
    "desired_skills": [
        "big data",
        "gen AI"
    ],
    "desired_grades": [
        "B+",
        "A-"
    ],
    "open_to_mentor": false,
    "open_to_be_mentored": false
}'''
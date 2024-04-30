import sqlite3
from typing import List
from models import PostSchema
from fastapi import HTTPException
import database as db
from models import PostSchema

'''
NOTE: All data on this page is synthetic data produced by chat gpt
'''


connection = sqlite3.connect('ment2b.db')

USERS_TABLE = 'Users'
SKILLS_TABLE = 'Skills'

def query(query):
    cursor = connection.cursor()
    results = cursor.execute(query)
    print(results.fetchall())
    cursor.close()


def drop_table(table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f'''
            DROP TABLE {table_name}
        ''')
        connection.commit()
        cursor.close()
    except: 
        pass

def drop_all_tables():
    drop_table(USERS_TABLE)
    drop_table(SKILLS_TABLE)


def load_db_mock_data():

    connection.execute('''
            CREATE TABLE IF NOT EXISTS Skills(
                skill UNIQUE
            )
    ''')
        
    connection.execute('''
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
    connection.commit()
    

    # load in mock skills
    skills = [
        # Programming Languages
        "Java", "Python", "JavaScript", "C#", "C++", "Ruby", "Swift", "Kotlin", "PHP", "TypeScript",
        
        # Web Development
        "HTML5", "CSS3", "Bootstrap", "React.js", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        
        # Database Management
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQLite", "Firebase", "Redis", "Cassandra", "DynamoDB",
        
        # Cloud Computing
        "Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Docker", "Kubernetes", 
        "Terraform", "Serverless Framework", "CloudFormation", "Ansible", "Chef",
        
        # DevOps
        "Continuous Integration/Continuous Deployment (CI/CD)", "Jenkins", "Git", "GitHub", "GitLab", 
        "Bitbucket", "Travis CI", "CircleCI", "Docker Compose", "SonarQube",
        
        # Cybersecurity
        "Ethical Hacking", "Penetration Testing", "Network Security", "Cryptography", "Firewalls", 
        "Intrusion Detection Systems (IDS)", "Security Information and Event Management (SIEM)", 
        "Vulnerability Assessment", "Identity and Access Management (IAM)", "Incident Response",
        
        # Software Engineering
        "Agile Methodologies", "Scrum", "Test-Driven Development (TDD)", "Behavior-Driven Development (BDD)", 
        "Object-Oriented Programming (OOP)", "Functional Programming", "Design Patterns", "Software Architecture", 
        "Microservices", "RESTful APIs"
    ]
    db.insert_skills(skills)


    # Load in mock users
    test_json = '''{
        "uid": "aaaa",
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
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    
    test_json = '''
    {
        "uid": "bbbb",
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "grade": "B",
        "position": "Software Engineer",
        "sub_division": "CIO",
        "skills": [
            "coding",
            "problem-solving",
            "team collaboration"
        ],
        "desired_skills": [
            "machine learning",
            "cloud computing"
        ],
        "desired_grades": [
            "A",
            "B-"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": true
    }'''
    db.insert_new_user(PostSchema.model_validate_json(test_json))

    test_json = '''
    {
        "uid": "cccc",
        "first_name": "Emily",
        "last_name": "Nguyen",
        "email": "emily.nguyen@example.com",
        "grade": "A-",
        "position": "Data Scientist",
        "sub_division": "Analytics",
        "skills": [
            "data analysis",
            "machine learning",
            "Python programming"
        ],
        "desired_skills": [
            "natural language processing",
            "deep learning"
        ],
        "desired_grades": [
            "A",
            "A-"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": false
    }

    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))

    test_json = '''
    {
        "uid": "dddd",
        "first_name": "Michael",
        "last_name": "Garcia",
        "email": "michael.garcia@example.com",
        "grade": "B+",
        "position": "UX Designer",
        "sub_division": "Design",
        "skills": [
            "UI design",
            "prototyping",
            "user research"
        ],
        "desired_skills": [
            "interaction design",
            "design thinking"
        ],
        "desired_grades": [
            "B+",
            "A-"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": true
    }

    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    test_json = '''
        {
            "uid": "eeee",
            "first_name": "Samantha",
            "last_name": "Chen",
            "email": "samantha.chen@example.com",
            "grade": "A",
            "position": "Project Manager",
            "sub_division": "Management",
            "skills": [
                "project planning",
                "team leadership",
                "communication"
            ],
            "desired_skills": [
                "agile methodologies",
                "risk management"
            ],
            "desired_grades": [
                "A",
                "A-"
            ],
            "open_to_mentor": false,
            "open_to_be_mentored": true
        }

    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    test_json = '''
    {
        "uid": "ffff",
        "first_name": "Daniel",
        "last_name": "Martinez",
        "email": "daniel.martinez@example.com",
        "grade": "B",
        "position": "Marketing Specialist",
        "sub_division": "Marketing",
        "skills": [
            "social media marketing",
            "content creation",
            "analytics"
        ],
        "desired_skills": [
            "SEO",
            "email marketing"
        ],
        "desired_grades": [
            "B+",
            "B"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": true
    }

    '''
    # Has similar skills to Alice Johnson 
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    test_json = '''
    {
        "uid": "iiii",
        "first_name": "David",
        "last_name": "Liu",
        "email": "david.liu@example.com",
        "grade": "B+",
        "position": "Software Engineer",
        "sub_division": "Tech",
        "skills": [
            "coding",
            "problem-solving",
            "team collaboration"
        ],
        "desired_skills": [
            "machine learning",
            "cloud computing"
        ],
        "desired_grades": [
            "A",
            "B-"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": false
    }

    '''
    # Similar skills to 
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    test_json = '''
    {
        "uid": "jjjj",
        "first_name": "Alex",
        "last_name": "Gonzalez",
        "email": "alex.gonzalez@example.com",
        "grade": "A-",
        "position": "Data Scientist",
        "sub_division": "Analytics",
        "skills": [
            "data analysis",
            "machine learning",
            "Python programming"
        ],
        "desired_skills": [
            "deep learning",
            "natural language processing"
        ],
        "desired_grades": [
            "A",
            "A-"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": false
    }

    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    test_json = '''
    {
        "uid": "kkkk",
        "first_name": "Sophia",
        "last_name": "Chang",
        "email": "sophia.chang@example.com",
        "grade": "A",
        "position": "Machine Learning Engineer",
        "sub_division": "AI Research",
        "skills": [
            "machine learning",
            "deep learning",
            "natural language processing"
        ],
        "desired_skills": [
            "deep learning",
            "natural language processing"
        ],
        "desired_grades": [
            "A",
            "A-"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": false
    }

    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    test_json = '''
    {
        "uid": "llll",
        "first_name": "Ryan",
        "last_name": "Lee",
        "email": "ryan.lee@example.com",
        "grade": "A-",
        "position": "Data Engineer",
        "sub_division": "Data",
        "skills": [
            "data analysis",
            "SQL",
            "data modeling"
        ],
        "desired_skills": [
            "data analysis",
            "SQL"
        ],
        "desired_grades": [
            "A-",
            "B+"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": false
    }

    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))
    
    test_json = '''
    {
        "uid": "mmmm",
        "first_name": "Laura",
        "last_name": "Rodriguez",
        "email": "laura.rodriguez@example.com",
        "grade": "B+",
        "position": "UX Designer",
        "sub_division": "Design",
        "skills": [
            "user research",
            "prototyping",
            "UI design"
        ],
        "desired_skills": [
            "prototyping",
            "UI design"
        ],
        "desired_grades": [
            "A",
            "B+"
        ],
        "open_to_mentor": true,
        "open_to_be_mentored": false
    }
    '''
    db.insert_new_user(PostSchema.model_validate_json(test_json))

    query('SELECT * FROM USERS')
    query('SELECT * FROM SKILLS')

def reset_mock_db_data():
    drop_all_tables()
    load_db_mock_data()

reset_mock_db_data()
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from os import path
from chat_gpt import extract_skills_from_profile, extract_wants_from_profile
from database import get_user_details


# Load a pre-trained BERT model
model_path =  path.abspath(path.join(path.dirname(__file__), "model"))
# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# model.save(model_path)
model = SentenceTransformer(model_path)


def model_encoder(mentee_desired_skills: str, mentors: dict):
    mentee_wants = " ".join(mentee_desired_skills)
    mentee_embeddings = model.encode(mentee_wants)
    mentor_embeddings = model.encode([mentor["skills"] for mentor in mentors])
    return mentee_embeddings, mentor_embeddings


def ment2b(session_token, mentee: dict, mentors: dict):
    mentee_wants = extract_wants_from_profile(mentee.profile_description)
    
    mentee_desired_skills = mentee.desired_skills + mentee_wants
    for mentor in mentors:
        mentor_skills = extract_skills_from_profile(mentor["profile_description"])
        mentor["skills"] = mentor["skills"] + mentor_skills

    mentee_embeddings, mentor_embeddings = model_encoder(mentee_desired_skills, mentors)
    # Calculate cosine similarity between mentee embedding and each mentors embedding
    similarities = cosine_similarity([mentee_embeddings], mentor_embeddings)[0]
 
    # Pair users with their similarity scores
    similar_users = list(zip([user["uid"] for user in mentors], similarities))

    # Sort users by similarity score in descending order
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:3]
    
    mentors = {mentor['uid']: mentor['profile_description'] for mentor in mentors}

    # user[0] = uid, user[1] = match % from model
    return [get_user_details(session_token, user[0]) for user in similar_users]


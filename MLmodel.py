from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from os import path


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


def ment2b(mentee_desired_skills: list, mentors: dict):
    mentee_embeddings, mentor_embeddings = model_encoder(mentee_desired_skills, mentors)
    # Calculate cosine similarity between mentee embedding and each mentors embedding
    similarities = cosine_similarity([mentee_embeddings], mentor_embeddings)[0]

    # Pair users with their similarity scores
    similar_users = list(zip([user["uid"] for user in mentors], similarities[1:]))
    
    # Sort users by similarity score in descending order
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:3]
    
    print("Similar users to Alice based on interests:")
    for user, similarity in similar_users:
        print(f"{user}: {similarity}")


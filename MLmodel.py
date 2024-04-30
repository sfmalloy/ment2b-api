from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from os import path


# Load a pre-trained BERT model
model_path =  path.abspath(path.join(path.dirname(__file__), "model"))
# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# model.save(model_path)
model = SentenceTransformer(model_path)

# User data
users = [
    {"id": 1, "name": "Alice", "age": 25, "gender": "Female", "interests": ["Programming", "Data Science", "Machine Learning"]},
    {"id": 2, "name": "Bob", "age": 30, "gender": "Male", "interests": ["Writing", "Music", "Art"]},
    {"id": 3, "name": "Charlie", "age": 22, "gender": "Male", "interests": ["Entrepreneurship", "Marketing", "Product Management"]},
    {"id": 4, "name": "Diana", "age": 28, "gender": "Female", "interests": ["Photography", "Graphic Design", "Video Editing"]},
    {"id": 5, "name": "Emma", "age": 26, "gender": "Female", "interests": ["Fitness", "Nutrition", "Yoga"]},
    {"id": 6, "name": "Frank", "age": 35, "gender": "Male", "interests": ["Cooking", "Food Critique", "Travel"]},
    {"id": 7, "name": "Grace", "age": 24, "gender": "Female", "interests": ["Fashion Design", "Styling", "Beauty"]},
    {"id": 8, "name": "Henry", "age": 29, "gender": "Male", "interests": ["Gardening", "DIY", "Woodworking"]},
    {"id": 9, "name": "Ivy", "age": 27, "gender": "Female", "interests": ["Environmental Conservation", "Sustainability", "Renewable Energy"]},
    {"id": 10, "name": "Jack", "age": 31, "gender": "Male", "interests": ["Film Making", "Screenwriting", "Directing"]},
    {"id": 11, "name": "Allen", "age": 23, "gender": "Male", "interests": ["Machine Learning", "Data Science", "Python"]},
]

def get_user_skills(uid: str) -> list:
    #api call to get user from database
    return " ".join(users[0]["interests"]) #tmp

def model_encoder(uid: str, mentors: dict):
    mentee_skills = get_user_skills("alice")
    mentee_embeddings = model.encode(mentee_skills)

    #api call to get all mentors from database
    mentor_embeddings = model.encode([mentor["interests"] for mentor in users])

    return mentee_embeddings, mentor_embeddings

def ment2b(mentee_embeddings, mentor_embeddings, mentors: dict):
    # Calculate cosine similarity between Alice's embedding and each user's embedding
    similarities = cosine_similarity([mentee_embeddings], mentor_embeddings)[0]

    # Pair users with their similarity scores
    similar_users = list(zip([user["name"] for user in users[1:]], similarities[1:]))
    
    # Sort users by similarity score in descending order
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:3]
    
    print("Similar users to Alice based on interests:")
    for user, similarity in similar_users:
        print(f"{user}: {similarity}")

x, y = model_encoder("uid")
ment2b(x, y)

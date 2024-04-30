from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from os import path

# Load a pre-trained BERT model
model_path =  path.abspath(path.join(path.dirname(__file__), "model"))
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

# Get Alice's interests
alice_interests = " ".join(users[0]["interests"])

# Encode interests using BERT model
user_embeddings = model.encode([user["interests"] for user in users])

# Encode Alice's interests
alice_embedding = model.encode([alice_interests])[0]

# Calculate cosine similarity between Alice's embedding and each user's embedding
similarities = cosine_similarity([alice_embedding], user_embeddings)[0]

# Pair users with their similarity scores
similar_users = list(zip([user["name"] for user in users[1:]], similarities[1:]))

# Sort users by similarity score in descending order
similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)

print("Similar users to Alice based on interests:")
for user, similarity in similar_users:
    print(f"{user}: {similarity}")

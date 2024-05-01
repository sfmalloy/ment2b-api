import json
import openai
from config import OPENAI_API_KEY

# Set up your OpenAI API key
openai.api_key = OPENAI_API_KEY

def extract_wants_from_profile(description):
    # Define a prompt
    prompt = f"Extract relevant wants from the description:\n{description}\nWants:"

    # Generate completions
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5,
        stop=None
    )

    response_text = response.choices[0].text.strip()
    wants_text = [line.lstrip("1234567890.- ") for line in response_text.split("\n")]
    
    return wants_text

def suggest_mentorship_questions(mentor_description, mentee_description):
    # Define a prompt
    prompt = f"Given their user descriptions, suggest 2 lists of 3 questions for the mentor and mentee to ask each other and get to know each other better.\nMentor Description:{mentor_description}\nMentee Description:{mentee_description}."

    # Generate completions
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5,
        stop=None
    )

    # Extract mentor and mentee questions
    generated_text = response.choices[0].text.strip()
    questions = [line.lstrip("1234567890.- ") for line in generated_text.split("\n") if line[-1:] == "?"]

    questions_json = {
        "Questions for the mentor": questions[:3],
        "Questions for the mentee": questions[-3:]
    }

    # Convert to JSON
    json_data = json.dumps(questions_json)

    return json_data

if __name__ == '__main__':
    # Example profile description
    mentee_profile_description = "I am a proactive developer seeking mentorship from seasoned professionals who have successfully navigated complex projects and technologies. My goal is to gain insights from individuals who possess extensive experience in software development, particularly in Python, Java, and other advanced programming languages. I am eager to learn from those who have tackled challenges similar to those I anticipate encountering in my career. Located in Pennsylvania, I am open to remote mentorship opportunities or local connections within the tech community."

    mentor_profile_description = "Hello, I'm an experienced and empathetic developer with over 15 years of industry expertise. I'm known for my supportive and collaborative approach to mentorship. I offer guidance in career development, technical expertise, leadership, and personal growth. My extensive programming skills include proficiency in Python, Java, JavaScript, and C++. I value integrity, empathy, and continuous learning, aiming to make a positive impact on your life and career. Whether it's in-person or virtual, I'm available for sessions and I encourage you to embrace growth opportunities and strive for excellence together."
    
    # Extract relevant wants from the description
    # wants = extract_wants_from_profile(mentee_profile_description)
    # print("\nExtracted Wants:")
    # print(wants)

    # Generate suggested questions
    questions_json = suggest_mentorship_questions(mentor_profile_description, mentee_profile_description)
    print("\nSuggested Questions:")
    print(questions_json)

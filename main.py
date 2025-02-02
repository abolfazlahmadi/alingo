from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json

import os

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Initialize FastAPI app
app = FastAPI()


# Define input model
class InputData(BaseModel):
    text: str  # GERMAN TEXT
    num_questions: int = 10
#   type_of_questions: str  # grammar , vocab , writing , listening , speaking


# Function to generate German learning questions
def generate_german_questions(text, num_questions):
    prompt = f"""
    Generate {num_questions} different types of German language learning questions based on this text: "{text}".
    The questions should be related to practice the grammar explained in the text or vocabularies used in the text.
    Start with easy questions with difficulty 1 and end with hard questions with difficulty 9.
    Try to have the same number of questions in different difficulties and types.  
    The response should be a JSON array with elements formatted as follows:
    [
      {{
        "type": "fill_in_the_blank",
        "question": "Ich gehe morgen ___ die Stadt, falls das Wetter gut ist.",
        "answer": "in",
        "difficulty": 7,
        "topics": ["prepositions", "conditionals", "accusative"]
      }},
      {{
        "type": "fill_in_the_blank_multiple_choice",
        "question": "Wir fahren nächste Woche ___ Frankreich, weil wir dort Freunde besuchen möchten.",
        "options": ["in", "nach"],
        "answer": "nach",
        "difficulty": 8,
        "topics": ["prepositions", "subordinating conjunctions"]
      }}
    ]
    Only return the JSON array, without any additional text.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates structured JSON output for German language learning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        questions_json = response.choices[0].message.content.strip()

        return json.loads(questions_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


def generate_german_questions2(text, num_questions):
    prompt = f"""
    Generate {num_questions} different types of German language learning questions based on content of the germany language book:"{text}".
    The questions should be related to practice the grammar explained  or vocabularies used in the exact lesson of the book.
    Start with easy questions with difficulty 1 and end with hard questions with difficulty 9.
    Try to have the same number of questions in different difficulties and types.  
    The response should be a JSON array with elements formatted as follows:
    [
      {{
        "type": "fill_in_the_blank",
        "question": "Ich gehe morgen ___ die Stadt, falls das Wetter gut ist.",
        "answer": "in",
        "difficulty": 7,
        "topics": ["prepositions", "conditionals", "accusative"]
      }},
      {{
        "type": "fill_in_the_blank_multiple_choice",
        "question": "Wir fahren nächste Woche ___ Frankreich, weil wir dort Freunde besuchen möchten.",
        "options": ["in", "nach"],
        "answer": "nach",
        "difficulty": 8,
        "topics": ["prepositions", "subordinating conjunctions"]
      }}
    ]
    Only return the JSON array, without any additional text.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates structured JSON output for German language learning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        questions_json = response.choices[0].message.content.strip()

        return json.loads(questions_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


# API Endpoint
@app.post("/generate_questions")
async def generate_questions(data: InputData):
    questions = generate_german_questions(data.text, data.num_questions)
    return {"questions": questions}


# API Endpoint
@app.post("/generate_questions2")
async def generate_questions2(data: InputData):
    questions = generate_german_questions2(data.text, data.num_questions)
    return {"questions": questions}


# Health check
@app.get("/")
async def root():
    return {"message": "Server2 is running!"}

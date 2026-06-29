import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """
You are an AI content attribution assistant.

Determine whether the following text appears AI-generated or human-written.

Return ONLY FLOAT NUMBER BETWEEN 0 AND 1.

Do not include markdown.
Do not include explanations.

A score of:
- 0.00 = definitely human
- 1.00 = definitely AI

Format:

[Score as float]

Text:
"""


def llm_score(text):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": PROMPT + text
            }
        ],
        temperature=0
    )

    response = completion.choices[0].message.content

    return float(response)
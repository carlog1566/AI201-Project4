import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """
You are an AI content attribution assistant.

Determine whether the following text appears AI-generated or human-written.

Return ONLY valid JSON.

Do not include markdown.
Do not include explanations.
Do not wrap the JSON in ```.

A score of:
- 0.0 = definitely human
- 1.0 = definitely AI

Format:

{
    "attribution": "likely_ai" or "likely_human",
    "score": number between 0 and 1
}

Text:
"""


def detect_with_llm(text):

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

    print("\n===== GROQ RESPONSE =====")
    print(response)
    print("=========================\n")


    return json.loads(response)
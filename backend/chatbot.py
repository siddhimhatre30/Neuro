import os
from dotenv import load_dotenv
from openai import OpenAI

from backend.command import (
    ask_open_image,
    ask_open_pdf,
    handle_drive_choice,
    handle_confirmation,
)
from backend.session import check_timeout

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chatbot_response(user_text):
    query = user_text.lower().strip()
    query = query.replace("a i", "ai")

    check_timeout()

    if any(d in query for d in ["c drive", "d drive", "e drive"]):
        handle_drive_choice(query)
        return ""

    if "yes" in query or "no" in query:
        handle_confirmation(query)
        return ""

    if "open image" in query:
        parts = query.replace("open image", "").split(" from ")
        name = parts[0].strip()
        location = parts[1].strip() if len(parts) > 1 else None
        ask_open_image(name, location)
        return ""

    if "open pdf" in query:
        parts = query.replace("open pdf", "").split(" from ")
        name = parts[0].strip()
        location = parts[1].strip() if len(parts) > 1 else None
        ask_open_pdf(name, location)
        return ""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant named Neuro."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, I am having trouble connecting to my brain."
print("API KEY LOADED:", bool(os.getenv("OPENAI_API_KEY")))

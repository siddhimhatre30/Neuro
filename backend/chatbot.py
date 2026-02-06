# ================= IMPORTS =================
import os
from dotenv import load_dotenv
from openai import OpenAI

# Optional session timeout (safe import)
try:
    from backend.session import check_timeout
except:
    def check_timeout():
        pass


# ================= LOAD ENV =================
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=API_KEY)


# ================= CHATBOT FUNCTION =================
def chatbot_response(user_text: str) -> str:
    """
    Handles online chatbot response using OpenAI
    """

    if not user_text:
        return "Please say something."

    try:
        # Optional session timeout check
        check_timeout()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are Neuro, a friendly and helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            max_tokens=200,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        return reply

    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, I am having trouble connecting to the internet."

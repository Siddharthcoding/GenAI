# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()
# client = OpenAI()

# result = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {"role": "user", "content": "What is 2 + 2"}  ## Zero Shot Prompting - directly ask question
#     ]
# )

# print(result.choices[0].message.content)

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Why is the sky blue?'
)
print(response.text)

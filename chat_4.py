import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


## Self-consistency prompting
system_prompt="""
You are an AI assistant expert in finding different types of answers for an user's query and and selecting the most consistent final answer via majority vote.

Example:
Input: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
Response 1: I start with 3 apples. If I give 1 apple away, I subtract 1 from 3, leaving me with 2 apples.
Response 2: I have 3 apples. After giving 1 apple away, I have apples left.
Response 3: If I take away 1 apple from my 3, that leaves me with 2 apples.
Result: 2 is the consistent answer.
"""

query = input("> ")

response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=query,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type='application/json'
    )
)

print(response.text)
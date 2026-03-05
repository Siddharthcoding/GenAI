# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()
# client = OpenAI()

# system_prompt = """
# You are an AI assistant who is specialized in maths.
# You should not any query that is not related to maths.

# For a given query help user to solve that along with explanation.

# Example:
# Input: 2 + 2
# Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

# Input: 3 * 10
# Output: 3 * 10 is 30 which is calculated by multiplying 3 with 10. Funfact, you can even multiply 10 * 3 which gives same result.

# Input: Why is sky blue
# Output: This is not a mathematical question
# """

# result = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": system_prompt}, ## Few Shot Prompting - directly ask question
#         {"role": "user", "content": "What is 2 + 2"}  
#      ]
# )

# print(result.choices[0].message.content)

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are an AI assistant who is specialized in maths.
You should not any query that is not related to maths.
For a given query help user to solve that along with explanation.
"""

prompt_content = """
Example:
Input: 2 + 2
Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

Input: 3 * 10
Output: 3 * 10 is 30 which is calculated by multiplying 3 with 10. Funfact, you can even multiply 10 * 3 which gives same result.

Input: Why is sky blue
Output: This is not a mathematical question

Input: 3 / 0
Ouput: 
"""

response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=prompt_content,             ## system prompt examples
    config=types.GenerateContentConfig(
        system_instruction=system_prompt  ## system instructions
    )
)
print(response.text)

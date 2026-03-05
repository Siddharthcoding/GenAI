# from dotenv import load_dotenv
# from openai import OpenAI
# import json

# load_dotenv()
# client = OpenAI()

# system_prompt = """
# You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.
# For the given user input, analyze the input and break down the problem step by step.
# Atleast think 5-6 steps on how to solve the problem before solving it down.

# The steps are you get a user input, you analyse, you think, you again think for several times and return an output with explanation and finally you validate the output as well before giving final result.

# Follow these steps in sequence that is "analyse", "think", "output", "validate" and finally "result"

# Rules:
# 1. Follow the strict JSON output as per the Output schema.
# 2. Always perform one step at a time and wait for next input.
# 3. Carefully analyze the user query.

# Output Format:
# {{step: "string", content: "string"}}


# Example:
# Input: What is 2+2
# Output: {{step: "analyse", content: "Alright, the user is interested in maths query and he is asking a basic arithmetic operation"}}
# Output: {{step: "think", content: "To perform the addition I must go from left from right and add all operands"}}
# Output: {{step: "output", content: "4"}}
# Output: {{step: "validate", content: "seems like 4 is correct answer for 2+2"}}
# Output: {{step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers"}}
# """

# messages = [
#     {"role": "system", "content":system_prompt},
# ]

# query = input("> ")
# messages.append({"role" : "user", "content": query})

# while True:
#     response = client.chat.completions.create(
#         model="gpt-4",
#         response_format={"type": "json_object"},
#         messages=messages
#     )

#     parsed_response = json.load(response.choices[0].message.content)
#     messages.append({"role": "assistant", "content": json.dumps(parsed_response)})  ## Chain of thought
    
#     if parsed_response.get("step") != "output":
#         print(f"🧠: {parsed_response.get("content")}")
#         continue

#     print(f"🤖: {parsed_response.get("content")}")
#     break


# result = client.chat.completions.create(
#     model="gpt-4",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content":system_prompt},
#         {"role":"user", "content": "what is 3+10-4*2"},
#         # {"role": "assistant", "content": json.dumps()} ## Chain of thought- step by step responses are added to break down problems and solve them
#     ]
# )

# print(result.choices[0].message.content)


import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = """
You are an AI assistant expert in breaking down complex problems.
Follow these steps in sequence: "analyse", "think", "output", "validate", "result".
Rules:
1. Return ONLY a JSON object following the Output Format.
2. Perform exactly ONE step per turn.
3. Wait for the user to say "next" or provide more input before proceeding to the next step.

Output Format:
{"step": "string", "content": "string"}

Example:
Input: What is 2+2
Output: {{step: "analyse", content: "Alright, the user is interested in maths query and he is asking a basic arithmetic operation"}}
Output: {{step: "think", content: "To perform the addition I must go from left from right and add all operands"}}
Output: {{step: "output", content: "4"}}
Output: {{step: "validate", content: "seems like 4 is correct answer for 2+2"}}
Output: {{step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers"}}
"""

messages = []

user_query = input("> ")

messages.append(types.Content(
    role="user", 
    parts=[types.Part(text=user_query)]
))

while True:
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type='application/json'
        )
    )

    raw_text = response.text
    parsed_response = json.loads(raw_text)

    step = parsed_response.get("step")
    content = parsed_response.get("content")

    messages.append(types.Content(
        role="model", 
        parts=[types.Part(text=raw_text)]
    ))
    
    if step != "result":
        print(f"🧠: {parsed_response.get("content")}")
        continue

    print(f"🤖: {parsed_response.get("content")}")
    break
# from dotenv import load_dotenv
# from openai import OpenAI
# import json
# import requests

# load_dotenv()
# client = OpenAI()

# def get_weather(city: str):
#     print("🔨 Tool called: get_weather", city)
#     url = f"https://wttr.in/{city}?format=%C+%t"

#     response = requests.get(url)

#     if response.status_code == 200:
#         return f"The weather in {city} is {response.text}"
    
#     return "Something went wrong"

# available_tools = {
#     "get_waeather": {
#         "fn": get_weather,
#         "description": "Takes a city name as input and returns the current weather for the city"
#     },
# }

# system_prompt = f"""
# You are a helpful AI assistant who is specialized in resolving user query.
# You work on start, plan, action, observe mode.
# For the given user query and available tools plan the step by step execution, based on the planning,
# select the relevant tool from the available tool, and based on the tool selection you perform an action to call the tool.
# Wait for the observation and based on the observation from the tool call resolve the user query.

# Rules:
# - Follow the Output JSON format.
# - Always perform one step at a time and wait for next input.
# - Carefully analyze the user query.

# Output JSON format:
# {{
#     "step": "string",
#     "content": "string",
#     "function": "The name of function if the step is action",
#     "input": "The input parameter of the function"
# }}

# Available Tools:
# - get_weather: Takes a city name as input and returns the current weather for the city

# Example:
# User Query: What is the weather of New York ?
# Output: {{"step": "plan", "content": "The user is interested in weather data of New York"}}
# Output: {{"step": "plan", "content": "From the available tools, I should call get_weather"}}
# Output: {{"step": "action", "function": "get_weather", "input": "New York"}}
# Output: {{"step": "observe", "output": "12 degree cel"}}
# Output: {{"step": "output", "content": "The weather for New York seems to be 12 degrees."}}
# """
# messages = [
#     {"role": "system", "content": system_prompt}
# ]

# query = input("> ")
# messages.append({"role": "user", "content": query})

# while True:
#     response = client.chat.completions.create(
#         model = "gpt-4o",
#         response_format={"type": "json_object"},
#         messages = messages
#     )

#     parsed_output = json.loads(response.choices[0].message.content)
#     messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

#     if parsed_output.get("step") == "plan":
#         print(f"🧠: {parsed_output.get("content")}")
#         continue

#     if parsed_output.get("step") == "action":
#         tool_name = parsed_output.get("function")
#         tool_input = parsed_output.get("input")

#         if available_tools.get(tool_input, False) != False:
#             output = available_tools[tool_name].get("fn")(tool_input)
#             messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
#             continue

#     if parsed_output.get("step") == "output":
#         print(f"🤖: {parsed_output.get("content")}")
#         break



# response = client.chat.completions.create(
#     model = "gpt-4o",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": "What is the current weather of Bhubaneshwar ?"}
#     ]
# )

# print(response.choices[0].message.content)

import os
import json
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_weather(city: str):
    print("🔨 Tool called: get_weather", city)

    url = f"https://wttr.in/{city}?format=%C+%t"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"

        return "Weather API returned an error"

    except Exception as e:
        return f"Weather service failed: {str(e)}"

def run_command(command):
    result = os.system(command=command)
    return result

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as input and returns the current weather"
    }, 
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    }
}

system_prompt = """
You are a helpful AI assistant who is specialized in resolving user queries.

You work using the following steps:
plan -> action -> observe -> output

Rules:
- Always return ONLY JSON.
- Perform only ONE step at a time.
- Wait for the observation before continuing.
- Carefully analyse the user query.

Output JSON format:
{{
    "step": "string",
    "content": "string",
    "function": "function name if step is action",
    "input": "input parameter"
}}

Available Tools:
get_weather -> Takes a city name and returns the weather
run_command -> Takes a command as input to execute on system and returns output

Example:

User: What is the weather of New York?

Output:
{{"step": "plan", "content": "User wants weather information for New York"}}
Output:
{{"step": "plan", "content": "I should call get_weather tool"}}
Output:
{{"step": "action", "function": "get_weather", "input": "New York"}}
Output:
{{"step": "observe", "output": "12 degree cel"}}
Output:
{{"step": "output", "content": "The weather in New York is 12°C"}}
"""

messages = []

while True:
    query = input("> ")

    messages.append(
        types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
    )

    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )

        raw_text = response.text
        parsed_output = json.loads(raw_text)

        messages.append(
            types.Content(
                role="model",
                parts=[types.Part(text=raw_text)]
            )
        )

        step = parsed_output.get("step")

        if step == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue

        if step == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if tool_name in available_tools:
                output = available_tools[tool_name]["fn"](tool_input)
                observation = {
                    "step": "observe",
                    "output": output
                }

                messages.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=json.dumps(observation))]
                    )
                )

            continue

        if step == "output":
            print(f"🤖: {parsed_output.get('content')}")
            break
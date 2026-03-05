# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()  ## To load env files
# client = OpenAI()  ## To make api calls to openAI

# text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

# ## Specify the input and the model used to generate the embeddings
# response = client.embeddings.create(
#     input = text,
#     model="text-embedding-3-small"
# )


# print("Vector embeddings", response.data[0].embedding)

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

response = client.models.embed_content(
    model="models/gemini-embedding-001",  
    contents=text,
    config={
        'task_type': 'RETRIEVAL_DOCUMENT' 
    }
)

print("Vectore embeddings", response.embeddings[0].values)


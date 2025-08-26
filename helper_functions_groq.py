# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# # Load credentials from the environment file
# load_dotenv(dotenv_path=".env")

# # Initialize the Groq client with the API key
# try:
#     client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# except Exception as e:
#     print(f"Error initializing Groq client: {e}\n" \
#           "Please verify that your GROQ_API_KEY is correctly set in the env file.")
#     client = None

# def groq_chat(messages, model="llama3-8b-8192"):
#     """
#     Sends a chat request to the Groq API.
#     This serves as a direct replacement for the original chatgpt_chat function.
#     """
#     if client is None:
#         return "Groq client is not initialized. Please check your API key."
    
#     try:
#         # Create a chat completion request
#         response = client.chat.completions.create(
#             model=model,
#             messages=messages
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print(f"An error occurred while communicating with the Groq API: {e}")
#         return f"Error: Could not get a valid response from Groq. Details: {e}"

import os
from groq import Groq
from dotenv import load_dotenv

# Load credentials from your .env file
load_dotenv(dotenv_path=".env")

# Initialize the Groq client
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print(f"Error initializing Groq client: {e}\n" \
          "Please check your GROQ_API_KEY in the .env file.")
    client = None

def groq_chat(messages, model="llama3-8b-8192"):
    """
    Sends a chat request to the Groq API. This is the direct replacement
    for your original chatgpt_chat function.
    """
    if client is None:
        return "Groq client is not initialized. Check your API key."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred calling the Groq API: {e}")
        return f"Error: Could not get a response from Groq. {e}"


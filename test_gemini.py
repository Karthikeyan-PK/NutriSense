import os
from dotenv import load_dotenv
from google import genai


# Load environment variables from .env
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Check whether key exists
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit()


# Create Gemini client
client = genai.Client(api_key=api_key)


try:
    # Test Gemini API
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Hello! Briefly explain what a protein recommendation system does."
    )

    print("\nGEMINI API WORKING SUCCESSFULLY!\n")
    print(response.text)

except Exception as e:
    print("\nERROR CONNECTING TO GEMINI:\n")
    print(e)
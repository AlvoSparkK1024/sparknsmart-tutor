import asyncio
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API Key")
        return

    print("Configuring genai...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    print("Generating content...")
    try:
        response = await model.generate_content_async("Hello, are you there?")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

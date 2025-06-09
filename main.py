import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys 
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    parser = argparse.ArgumentParser(
        description="This is a cli tool to chat with Gemini, through the terminal!",
        epilog="Thanks for chatting!"
    ) 

    parser.add_argument(
    'user_prompt',
    help='Please provide a prompt for Gemini'
    )

    parser.add_argument(
    '--verbose','-v',
    action='store_true',
    help='Specify the verbosity'
    )

    args = parser.parse_args()
    
    if not args.user_prompt:
        print("Error: no prompt provided")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    messages = [
    types.Content(role="user",parts=[types.Part(text=args.user_prompt)])
    ]
    
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages
    )

    print(response.text)
    usage = str(response.usage_metadata).split(" ")

    if args.verbose:
        prompt = usage[6].split("=")[1]
        candidate = usage[2].split("=")[1]
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt}")
        print(f"Response tokens: {candidate}")

if __name__ == "__main__":
    main()

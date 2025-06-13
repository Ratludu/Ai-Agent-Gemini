import os
from subprocess import run
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys 
import argparse
from functions.get_files_info import get_files_info, get_file_content
from functions.run_file import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="This will get the file content in a specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that you want to get content from"
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="This function will run a specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file that you to run.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="This function will write to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The contents you want to write to the file."
            )
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

my_functions = {
    'get_files_info':get_files_info,
    'get_file_content':get_file_content,
    'run_python_file':run_python_file,
    'write_file':write_file
}

def call_function(function_call_part, verbose=False):
    
    function_name = function_call_part.name
    function_args= function_call_part.args
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else: 
        print(f"Calling function: {function_name}")
    try:
        function_to_call = my_functions[function_name]
    except:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
    result = function_to_call(working_directory = './calculator',**function_args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": result},
        )
    ],
)





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
    
    for i in range(20):
        response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        usage = str(response.usage_metadata).split(" ")


        if response.function_calls:
            for function_call in response.function_calls:
                function_result = call_function(function_call,verbose=args.verbose)

                if function_result.parts[0].function_response.response:
                    messages.append(function_result)
                    if args.verbose:
                        print(f"-> {function_result.parts[0].function_response.response}")
                else:
                    raise Exception(f"This is a fatal exception!!")
        else:
            print(response.text)
            break

    if args.verbose:
        prompt = usage[6].split("=")[1]
        candidate = usage[2].split("=")[1]
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt}")
        print(f"Response tokens: {candidate}")

if __name__ == "__main__":
    main()

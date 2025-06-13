from .get_files_info import is_within
import os
import subprocess
import sys
def run_python_file(working_directory, file_path):
    
    name = file_path
    file_path = os.path.join(os.path.abspath(working_directory),file_path)

    if not is_within(working_directory, file_path):
        return f'Error: Cannot execute "{name}" as it is outside the permitted working directory'

    if not os.path.exists(file_path):
        return f'Error: File "{name}" not found'

    if file_path[-2:] == ".py":
        return f'Error: "{name}" is not a Python file.'

    try:
        result = subprocess.run([
       sys.executable,file_path 
    ],
                            timeout=30,
                            capture_output=True,
                            text=True,
                            check=False
                                )
        print(f"STDOUT:{result.stdout}")
        print(f"STDERR:{result.stderr}")

        if result.returncode != 0:
            print(f"Process exited with code {result.returncode}")
        if result.stdout == '':
            return "No output produced"

    except Exception as e:
        return f"Error: executing Python file: {e}"

        
     



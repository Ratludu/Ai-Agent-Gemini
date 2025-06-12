import os 
from functions.get_files_info import is_within

def write_file(working_directory, file_path, content):

    new_directory = os.path.join(os.path.abspath(working_directory),file_path)

    if not is_within(working_directory, new_directory):
        return f"Error: cannot list {new_directory} as it is outside the permitted working directory"
    
    target_directory = os.path.dirname(new_directory)

    if target_directory:

        try:
            os.makedirs(target_directory, exist_ok=True)
        except Exception as e:
            return f"Error: {e}"

    try:
        with open(new_directory, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

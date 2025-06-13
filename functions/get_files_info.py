import os 

def is_within(parent, child):

    abs_parent = os.path.abspath(parent) 
    abs_child = os.path.abspath(child) 
    return abs_child.startswith(abs_parent)


def get_files_info(working_directory,directory=None):

    # check if the working directory exists 
    if directory is None:
        directory = "."

    new_directory = os.path.join(os.path.abspath(working_directory),directory)

    if not os.path.isdir(new_directory):
        return f'Error: "{new_directory}" is not a directory'


    if not is_within(working_directory, new_directory):
        return f"Error: cannot list {new_directory} as it is outside the permitted working directory"

    try:
        files = os.listdir(new_directory)
        
        result = ""
        for file in files: 
            file_path = os.path.join(new_directory,file)
            result += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)} \n"
        return result
    except:
        return f'Error: "{new_directory}" is not a directory'



def get_file_content(working_directory, file_path):

    # if the file path is outside the working directory then return a string error
    full_file_path = os.path.join(working_directory,file_path)

    if not os.path.isfile(full_file_path):
        return f'Error: "{full_file_path}" is not a file'

    if not is_within(working_directory, full_file_path):
        return f"Error: cannot get contents of {full_file_path} as it is outside the permitted working directory"

    try: 
        # if there is a file read it in and return the contents as a string
        with open(full_file_path, "r") as f:
            result = f.read(10000)

        if len(result) == 10000:
            result += f' File "{file_path}" truncated at 10000 characters'
        return result
    except Exception as e:
        return f"Error: {e}" 





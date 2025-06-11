import os 

def is_within(parent, child):

    abs_parent = os.path.abspath(parent) 
    abs_child = os.path.abspath(child) 
    return abs_child.startswith(abs_parent)


def get_files_info(working_directory,directory=None):

    # check if the working directory exists 
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







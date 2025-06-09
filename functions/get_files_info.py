import os 

def is_within(parent, child):

    abs_parent = os.path.abspath(parent) 
    abs_child = os.path.abspath(child) 
    print(abs_parent, abs_child)
    return os.path.commonpath([abs_parent, abs_child]) == abs_parent 

def get_files_info(working_directory,directory=None):

    # check if the working directory exists 
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'


    if not is_within(working_directory, directory):
        return f"Error: Cannot list {directory} as it is outside the permitted working directoy"




    #loop through the files in the directory
    try:
        files_info = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_dict = {
                    "name": file,
                    "file_size": os.path.getsize(file_path),
                    "is_dir": os.path.isdir(file_path),
                }
        result = ""
        for item in files_info:
            result += f"- {item['name']}: file_size={item['file_size']} bytes, is_dir={item['is_dir']}\n"

        return result 
    except Exception as e:
        return f"Error: {str(e)} while processing the directory {directory}."





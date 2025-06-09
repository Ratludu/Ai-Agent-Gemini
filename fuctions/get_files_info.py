import os 


def get_files_info(working_directory,directory=None):

    # check if the working directory exists 
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'


    # check if the directory is a subdirectory of the working directory 
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(directory)
    if not os.path.commonpath([abs_working_dir, abs_directory]) == abs_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 

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





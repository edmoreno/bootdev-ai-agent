import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        wkdir_abspath: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(
            os.path.join(wkdir_abspath, directory)
        )

        valid_target_dir: bool = os.path.commonpath([wkdir_abspath, target_dir]) == wkdir_abspath
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        target_dir_contents = os.listdir(target_dir)
    except Exception as e:
        return f"Error: {e}"

    return_str: str = f"Result for {format_current_directory_name(directory)} directory:\n"
    for item in target_dir_contents:
        return_str += get_dir_item_details(item, target_dir)
    return return_str

def get_dir_item_details(item: str, target_directory: str) -> str:
    try:
        item_path: str = os.path.join(target_directory, item)
        item_size: str = str(os.path.getsize(item_path))
        item_is_dir: bool = os.path.isdir(item_path)
    except Exception as e:
        return f"Error: {e}"

    return f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}\n"

def format_current_directory_name(directory: str) -> str:
    if directory == ".":
        return "current"
    return f'"{directory}"'

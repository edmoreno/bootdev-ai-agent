import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        wkdir_abspath: str = os.path.abspath(working_directory)
        target_filepath: str = os.path.normpath(
            os.path.join(wkdir_abspath, file_path)
        )

        valid_target_filepath: bool = os.path.commonpath([wkdir_abspath, target_filepath]) == wkdir_abspath
        if not valid_target_filepath:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_filepath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_filepath, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"

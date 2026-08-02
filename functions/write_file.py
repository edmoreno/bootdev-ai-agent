import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        wkdir_abspath: str = os.path.abspath(working_directory)
        target_filepath: str = os.path.normpath(
            os.path.join(wkdir_abspath, file_path)
        )

        valid_target_filepath: bool = os.path.commonpath([wkdir_abspath, target_filepath]) == wkdir_abspath
        if not valid_target_filepath:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_filepath):
            return f'Error: "{target_filepath}" is a directory'

        os.makedirs(os.path.dirname(target_filepath), exist_ok=True)

        with open(target_filepath, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

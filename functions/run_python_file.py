import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        wkdir_abspath: str = os.path.abspath(working_directory)
        target_filepath: str = os.path.normpath(
            os.path.join(wkdir_abspath, file_path)
        )

        valid_target_filepath: bool = os.path.commonpath([wkdir_abspath, target_filepath]) == wkdir_abspath
        if not valid_target_filepath:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_filepath):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_filepath.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_filepath]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=wkdir_abspath,
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )

        output_string = ""
        if result.check_returncode():
            output_string += f"Process exited with code {result.returncode}"
        if result.stdout is None and result.stderr is None:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT:{result.stdout}"
            output_string += f"STDERR:{result.stderr}"
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

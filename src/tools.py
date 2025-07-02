import os
from typing import List,Optional
from datetime import datetime

def create_test_file_from_code(url: str, code: str, code_type: str) -> str:
    """
    Replaces 'src' with 'test' in the given file path, creates a new file with 'Test'
    and the current date/time appended to the original file name (before extension),
    and writes the code to it.

    Args:
        url (str): The original file path.
        code (str): The code to write into the new file.
        code_type (str): The code type/extension (e.g., 'py', 'js').

    Returns:
        str: The path to the newly created test file.
    """
    # Replace 'src' with 'test' in the path
    new_path = url.replace(os.sep + 'src' + os.sep, os.sep + 'test' + os.sep)
    dir_name, file_name = os.path.split(new_path)
    name, ext = os.path.splitext(file_name)

    # Use code_type as extension if provided, else keep original
    ext = f'.{code_type}' if code_type else ext

    # Get current date and time
    now_str = datetime.now().strftime('%H%M%S_%Y%m%d')

    # Create new file name with 'Test' and date/time appended
    new_file_name = f"{name}Test_{now_str}{ext}"
    new_file_path = os.path.join(dir_name, new_file_name)

    # Ensure the directory exists
    os.makedirs(dir_name, exist_ok=True)

    # Write the code to the new file
    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    return new_file_path

def read_file_as_text(file_path: str) -> str:
    """
    Reads the content of a file as text.

    Args:
        file_path (str): The full path to the file.

    Returns:
        str: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def list_files_recursive(
    url: str,
    file_types: Optional[List[str]] = None,
    exclude_texts: Optional[List[str]] = None,
    include_texts: Optional[List[str]] = None
) -> List[str]:
    """
    Recursively traverses all subfolders of the given directory path (url)
    and returns a list of full file paths for each file found.
    - If file_types is provided, only files with those extensions are returned.
    - If exclude_texts is provided, files whose names contain any of the texts are excluded.
    - If include_texts is provided, only files whose names contain any of the texts are included.

    Args:
        url (str): The root directory path.
        file_types (List[str], optional): List of file extensions to filter by (e.g., ['.csv', '.txt']).
        exclude_texts (List[str], optional): List of text snippets; files containing any of these in their name are excluded.
        include_texts (List[str], optional): List of text snippets; only files containing any of these in their name are included.

    Returns:
        List[str]: List of full file paths.
    """
    file_paths = []
    for root, _, files in os.walk(url):
        for file in files:
            # Exclude files containing any of the exclude_texts
            if exclude_texts and any(ex_text in file for ex_text in exclude_texts):
                continue
            # Include only files containing any of the include_texts (if provided)
            if include_texts and not any(inc_text in file for inc_text in include_texts):
                continue
            # Filter by file_types if provided
            if file_types and len(file_types) > 0:
                if any(file.lower().endswith(ext.lower()) for ext in file_types):
                    file_paths.append(os.path.join(root, file))
            else:
                file_paths.append(os.path.join(root, file))
    return file_paths

def remove_texts(source_text: str, texts_to_remove: list) -> str:
    """
    Removes all occurrences of each text in texts_to_remove from source_text.

    Args:
        source_text (str): The original text.
        texts_to_remove (list): List of text strings to remove from the original text.

    Returns:
        str: The modified text with all specified texts removed.
    """
    for text in texts_to_remove:
        source_text = source_text.replace(text, "")
    return source_text

def remove_texts_with_line(source_text: str, texts_to_remove: list) -> str:
    """
    Removes all lines from source_text that contain any of the texts in texts_to_remove.

    Args:
        source_text (str): The original text.
        texts_to_remove (list): List of text strings; lines containing any of these will be removed.

    Returns:
        str: The modified text with specified lines removed.
    """
    lines = source_text.splitlines()
    filtered_lines = [
        line for line in lines
        if not any(text in line for text in texts_to_remove)
    ]
    return "\n".join(filtered_lines)
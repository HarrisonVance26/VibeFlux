import os
import re
import shutil

# Set a global variable to control logging
enable_logging = True


def log(message):
    if enable_logging:
        print(message)


def copy_file_folder(src, dst, create_dst_dir=True, overwrite=False):
    """
    Copies a file or folder to a specified path.

    Args:
        src (str): The path of the source file or folder.
        dst (str): The destination path.
        create_dst_dir (bool): Whether to create the destination directory if it does not exist. Defaults to True.
        overwrite (bool): Whether to overwrite if a file or folder with the same name exists at the destination. Defaults to False.

    Returns:
        None
    """
    if not os.path.exists(src):
        log(f"Source path does not exist: {src}")
        return

    # Determine the final destination path
    if os.path.isdir(dst):
        final_dst = os.path.join(dst, os.path.basename(src))
    else:
        final_dst = dst

    # Check the destination path
    if os.path.exists(final_dst):
        if overwrite:
            if os.path.isdir(final_dst):
                shutil.rmtree(final_dst)
            else:
                os.remove(final_dst)
            log(f"Destination path already exists, will overwrite: {final_dst}")
        else:
            log(f"Destination path already exists, operation ignored: {final_dst}")
            return
    elif not os.path.exists(os.path.dirname(dst)) and create_dst_dir:
        os.makedirs(os.path.dirname(dst))
        log(f"Destination directory created: {os.path.dirname(dst)}")

    # Copy the file or folder
    if os.path.isdir(src):
        shutil.copytree(src, final_dst)
    else:
        shutil.copy2(src, final_dst)
    log(f"Copied from '{src}' to '{final_dst}'")


def delete_file(file_path):
    """
    Deletes a file at a specified path.

    Args:
        file_path (str): The path of the file to be deleted.

    Returns:
        None
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        log(f"File deleted: {file_path}")
    else:
        log(f"File does not exist: {file_path}")


def delete_files_pattern(directory, pattern):
    """
    Deletes all files in a specified directory that match a given regular expression pattern and logs the names of deleted files.

    Args:
        directory (str): The path of the directory.
        pattern (str): The regular expression pattern to match file names.

    Returns:
        None

    Example:
        # Delete all files ending with ".txt" in the directory "/path/to/directory"
        delete_files_with_pattern("/path/to/directory", r'.*\.txt$')
    """
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            log(f"File deleted: {file_path}")  # Log the name of the deleted file


def get_subfolders(directory):
    """
    Gets the absolute paths and names of all subfolders within a given directory.

    Args:
        directory (str): The path to the parent directory.

    Returns:
        subfolder_paths (list): A list of absolute paths to the subfolders.
        subfolder_names (list): A list of names of the subfolders.
    """
    if not os.path.exists(directory):
        log(f"Specified path does not exist: {directory}")
        return [], []
    if not os.path.isdir(directory):
        log(f"Specified path is not a directory: {directory}")
        return [], []

    subfolder_paths = []  # Store absolute paths to subfolders
    subfolder_names = []  # Store names of subfolders

    for f in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, f)):
            subfolder_paths.append(os.path.join(directory, f))
            subfolder_names.append(f)

    return subfolder_paths, subfolder_names


def get_subfiles(directory):
    """
    Gets the absolute paths and names of all subfiles within a specified directory.

    Args:
        directory (str): The path to the specified directory.

    Returns:
        file_paths (list): A list containing the absolute paths of all subfiles.
        file_names (list): A list containing the names of all subfiles.
    """
    if not os.path.exists(directory):
        log(f"Specified path does not exist: {directory}")
        return [], []
    if not os.path.isdir(directory):
        log(f"Specified path is not a directory: {directory}")
        return [], []

    file_paths = []  # Store file paths
    file_names = []  # Store file names

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)  # Get the absolute file path
        if os.path.isfile(file_path):
            file_paths.append(file_path)
            file_names.append(file)

    return file_paths, file_names


def count_images(folder, img_extensions=None):
    """
    Counts the number of image files in a specified folder.

    Args:
        folder (str): The path to the folder containing image files.
        img_extensions (list[str]): A list of image file extensions to look for. Defaults to common image formats if None.

    Returns:
        int: The count of image files in the folder.
    """
    # Default image file extensions
    if not img_extensions:
        img_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    return sum(any(f.endswith(ext) for ext in img_extensions) for f in os.listdir(folder))


def modify_content(file_path, old_string, new_string):
    """
    Modifies specific strings within a given file.

    Args:
        file_path (str): The path to the file.
        old_string (str): The string to be replaced.
        new_string (str): The new string to replace the old one.

    Returns:
        None: The file content is modified in-place; no return value.
    """
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Modify lines containing the specified string
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if old_string in line:
                line = line.replace(old_string, new_string)
                log(f"Modified '{old_string}' to '{new_string}'")
            file.write(line)


def modify_multi_contents(file_path, old_strings, new_strings):
    """
    Modifies multiple specific strings within a given file and logs the details of replacements.

    Args:
        file_path (str): The path to the file.
        old_strings (list): The list of strings to be replaced.
        new_strings (list): The list of new strings to replace the old ones.

    Returns:
        None: The content of the file is modified in-place; no return value.

    Example:
        file_path = '__init__.py'  # Specify the file path
        old_strings = ['old', 'OldString']  # List of old strings
        new_strings = ['new', 'NewString']    # List of new strings
        modify_multiple_contents(file_path, old_strings, new_strings)
    """
    # Check if the lengths of both lists are equal
    if len(old_strings) != len(new_strings):
        raise ValueError("The lists of old and new strings must have the same length.")

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Modify lines containing specified strings
    with open(file_path, 'w', encoding='utf-8') as file:
        for line_number, line in enumerate(lines, 1):
            for old_string, new_string in zip(old_strings, new_strings):
                if old_string in line:
                    updated_line = line.replace(old_string, new_string)
                    log(f"Replaced at line {line_number}: '{old_string}' -> '{new_string}'")
                    line = updated_line
            file.write(line)


def modify_multi_patterns(file_path, old_patterns, new_strings):
    """
    Modifies multiple specific patterns within a given file, supporting multi-line patterns, and logs the details of replacements.

    Args:
        file_path (str): The path to the file.
        old_patterns (list): The list of regular expression patterns to be replaced.
        new_strings (list): The list of new strings to replace the old ones.

    Returns:
        None: The content of the file is modified in-place; no return value.

    Example:
        file_path = '__init__.py'  # Specify the file path
        old_patterns = ['old_pattern', r'OldString\s+next_line']  # List of old patterns
        new_strings = ['new', 'NewString']  # List of new strings
        modify_multi_contents(file_path, old_patterns, new_strings)
    """
    # Check if the lengths of both lists are equal
    if len(old_patterns) != len(new_strings):
        raise ValueError("The lists of old patterns and new strings must have the same length.")

    # Read the entire file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace each pattern with the corresponding new string
    for old_pattern, new_string in zip(old_patterns, new_strings):
        content, num_replacements = re.subn(old_pattern, new_string, content, flags=re.MULTILINE)
        if num_replacements > 0:
            log(f"Replaced {num_replacements} occurrence(s) of pattern '{old_pattern}' with '{new_string}'")

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def extract_text_pattern(file_path, pattern):
    """
    Extracts text matching a specific pattern using regular expressions from a file.

    Args:
        file_path (str): The path to the file.
        pattern (str): The regular expression pattern.

    Returns:
        list[str]: A list of texts matching the pattern.

    Example:
        file_path = '__init__.py'  # Specify the file path
        pattern = r'AUTHOR_INFO = \("(.+?)"v1\.0\\n'
        extracted_texts = extract_text_with_pattern(file_path, pattern)
        log(extracted_texts)
    """
    extracted_texts = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            matches = re.findall(pattern, line)
            extracted_texts.extend(matches)

    return extracted_texts


def contains_text(file_path, pattern):
    """
    Checks if the file contains text that matches a specific regular expression pattern.

    Args:
        file_path (str): The path to the file.
        pattern (str): The regular expression pattern to search for.

    Returns:
        bool: Returns True if matching text is found, False otherwise.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if re.search(pattern, line):
                return True
    return False


def copy_subfiles_filter(src_folder, dst_folder, exclude_files=None, include_files=None):
    """
    Copies files within a folder to another folder, with options to exclude or include only specific files.

    Args:
        src_folder (str): The path to the source folder.
        dst_folder (str): The path to the destination folder.
        exclude_files (list, optional): A list of filenames to exclude from copying. Defaults to None.
        include_files (list, optional): A list of filenames to include for copying. Defaults to None.

    Returns:
        None: Files are copied with no return value.

    Example:
        src_folder = 'your/source/folder/path'
        dst_folder = 'your/destination/folder/path'
        exclude_files = ['file1.jpg', 'file2.txt']  # List of files to exclude
        include_files = ['file3.jpg', 'file4.txt']  # List of files to include
        copy_subfiles_filter(src_folder, dst_folder, exclude_files, include_files)
    """
    # Create the destination folder if it doesn't exist
    os.makedirs(dst_folder, exist_ok=True)

    # Get all files in the source folder
    files_to_copy, files_to_copy_name = get_subfiles(src_folder)

    for file_path, file_name in zip(files_to_copy, files_to_copy_name):
        # Check if the file is in the exclude list or not in the include list
        if (exclude_files and file_name in exclude_files) or (include_files and file_name not in include_files):
            continue

        # Copy the file
        dst_file_path = os.path.join(dst_folder, file_name)
        if os.path.exists(file_path):
            shutil.copy(file_path, dst_file_path)
            log(f"Copied file: {file_path} to {dst_file_path}")
        else:
            log(f"File not copied: {file_path}")


def copy_subfolders_filter(src_folder, dst_folder, exclude_folders=None, include_folders=None):
    """
    Copies subfolders within a parent folder to another folder, with options to exclude or include only specific subfolders.

    Args:
        src_folder (str): The path to the source folder.
        dst_folder (str): The path to the destination folder.
        exclude_folders (list, optional): A list of subfolder names to exclude from copying. Defaults to None.
        include_folders (list, optional): A list of subfolder names to include for copying. Defaults to None.

    Returns:
        None: Subfolders are copied with no return value.

    Example:
        src_folder = 'your/source/folder/path'
        dst_folder = 'your/destination/folder/path'
        exclude_folders = ['subfolder1', 'subfolder2']  # List of subfolders to exclude
        include_folders = ['subfolder3', 'subfolder4']  # List of subfolders to include
        copy_subfolders_filter(src_folder, dst_folder, exclude_folders, include_folders)
    """
    # Create the destination folder if it doesn't exist
    os.makedirs(dst_folder, exist_ok=True)

    # Get all subfolders in the source folder
    subfolders = [f for f in os.listdir(src_folder) if os.path.isdir(os.path.join(src_folder, f))]

    for folder in subfolders:
        src_subfolder_path = os.path.join(src_folder, folder)
        dst_subfolder_path = os.path.join(dst_folder, folder)

        # Check if the folder is in the exclude list or not in the include list
        if (exclude_folders and folder in exclude_folders) or (include_folders and folder not in include_folders):
            log(f"Subfolder not copied: {src_subfolder_path}")
            continue

        # Copy the subfolder
        if os.path.exists(src_subfolder_path):
            if not os.path.exists(dst_subfolder_path):
                shutil.copytree(src_subfolder_path, dst_subfolder_path)
                log(f"Copied subfolder: {src_subfolder_path} to {dst_subfolder_path}")
            else:
                log(f"Warning: {dst_subfolder_path} already exists, ignored")
        else:
            log(f"Subfolder not copied: {src_subfolder_path}")

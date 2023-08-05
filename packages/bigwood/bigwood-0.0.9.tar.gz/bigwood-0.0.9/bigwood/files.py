"""Collection of useful functions 
regarding manipulating the file system"""
from pathlib import Path



def trim_path_to_folder(path: Path, folder: str) -> Path:
    # get position of desired folder
    try:
        folder_index = path.parts.index(folder)
    except ValueError as e:
        raise e
    return Path(*path.parts[: folder_index + 1])

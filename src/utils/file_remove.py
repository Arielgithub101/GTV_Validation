import os
from typing import List
from src.logs import Log


def delete_local_files(files_path: List) -> None:
    """
    Delete multiple local files.

    Args:
        *args: Variable number of file paths to be deleted.

    Returns:
        None
        :param files_path:
    """
    Log.info(f'validation delete_local_files started ')
    for file_path in files_path:
        try:
            os.remove(file_path)
        except OSError as e:
            error_message: str = "An error occurred while deleting local file : " + str(e)
            Log.error(f'validation delete_local_files failed : {error_message}')
            raise ValueError(error_message)

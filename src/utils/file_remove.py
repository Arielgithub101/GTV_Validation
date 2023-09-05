import os
from src.logs.logs import Log


def delete_local_files(*args) -> None:
    """
    Delete multiple local files.

    Args:
        *args: Variable number of file paths to be deleted.

    Returns:
        None
    """
    Log.info(f'triggered delete_local_files started ')
    for file_path in args:
        try:
            os.remove(file_path)
        except OSError as e:
            Log.error(f'triggered delete_local_files failed : {e}')
            error_message: str = "An error occurred while deleting local file : " + str(e)
            raise ValueError(error_message)

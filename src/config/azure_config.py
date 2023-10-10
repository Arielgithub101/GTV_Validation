import os
from typing import Optional

from src.logs import Log


class ConfigConnection:

    @staticmethod
    def get_azure_connection_string(account_name) -> Optional[str]:
        try:
            Log.info('validation get_azure_connection_string started')
            return os.environ.get(f'{account_name}_connection_string')
        except (ConnectionError, Exception) as e:
            error_message: str = "error occurred while getting connection_string, check account param: " + str(e)
            Log.error(f'validation get_azure_connection_string failed: {error_message}')
            raise ValueError(error_message)


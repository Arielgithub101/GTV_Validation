import os
from typing import Optional

from src.logs.logs import Log


class ConfigConnection:

    @staticmethod
    def get_azure_connection_string(account_name) -> Optional[str]:
        try:
            Log.info('triggered get_azure_connection_string started')
            return os.environ.get(f'{account_name}_connection_string')
        except (ConnectionError, Exception) as e:
            Log.error(f'triggered get_azure_connection_string failed: {str(e)}')
            error_message: str = "An error occurred while connecting azure: " + str(e)
            raise ValueError(error_message)


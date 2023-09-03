import os
from typing import Optional


class ConfigConnection:

    @staticmethod
    def get_azure_connection_string(account_name) -> Optional[str]:
        try:
            return os.environ.get(f'{account_name}_connection_string')
        except (ConnectionError, Exception) as e:
            error_message: str = "An error occurred while connecting azure: " + str(e)
            raise ValueError(error_message)


import os

from starlette.responses import JSONResponse


class ConfigConnection:

    @staticmethod
    def get_azure_connection_string(account_name):
        try:
            return os.environ.get(f'{account_name}_connection_string')
        except Exception:
            return None

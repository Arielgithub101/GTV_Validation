import os


class ConfigConnection:
    @staticmethod
    def get_azure_connection_string(account_name):
        print('in config')

        return os.environ.get(f'{account_name}_connection_string')

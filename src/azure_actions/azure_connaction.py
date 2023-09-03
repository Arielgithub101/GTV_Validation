from src.config.azure_config import ConfigConnection

from azure.storage.blob import BlobServiceClient
from src.logs.logs import Log


def azure_connection(account_name: str, container_name: str):
    try:
        Log.info('triggered azure_connection started')
        print('in azure_connection')

        connection_string: str = ConfigConnection.get_azure_connection_string(account_name)

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)
        print('in azure_connection 2')

        return container_client
    except ConnectionError as e:
        Log.error('triggered azure_connection failed:', str(e))
        error_message: str = "An error occurred while connecting azure: " + str(e)
        raise ValueError(error_message)

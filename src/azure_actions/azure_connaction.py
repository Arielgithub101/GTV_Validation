from azure.storage.blob import BlobServiceClient, ContainerClient

from src.config import ConfigConnection
from src.logs import Log


def azure_connection(account_name: str, container_name: str) -> ContainerClient:
    try:
        Log.info('validation azure_connection started')

        connection_string: str = ConfigConnection.get_azure_connection_string(account_name)

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)

        return container_client
    except ConnectionError as e:
        Log.error(f'validation azure_connection failed:{str(e)}')
        error_message: str = "An error occurred while connecting azure: " + str(e)
        raise ValueError(error_message)

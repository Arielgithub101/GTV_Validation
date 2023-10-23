from azure.storage.blob import BlobServiceClient, ContainerClient

from src.config import ConfigConnection
from src.logs import Log


def azure_connection(account_name: str, container_name: str) -> ContainerClient:
    try:
        Log.info('validation azure_connection started')

        connection_string: str = ConfigConnection.get_azure_connection_string(account_name)
        if connection_string is None:
            raise ValueError("connection_string not found")

        blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(connection_string)
        container_client: ContainerClient = blob_service_client.get_container_client(container_name)

        Log.info('done activate - validation azure_connection')

        return container_client
    except Exception as e:
        error_message: str = "error while connecting azure account: " + str(e)
        Log.error(f'validation azure_connection failed:{error_message}')
        raise ValueError(error_message)

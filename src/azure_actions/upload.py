from azure.storage.blob import ContainerClient, BlobClient

from src.azure_actions.azure_connaction import azure_connection
from src.logs.logs import Log


def upload_to_azure(account_name: str, container_name: str, folder_name: str, local_file_path: str):
    try:
        Log.info('triggered upload_to_azure started')

        container_client: ContainerClient = azure_connection(account_name, container_name)

        destination_blob_name: str = f"{folder_name}/input/{local_file_path}"
        blob_client: BlobClient = container_client.get_blob_client(destination_blob_name)

        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data)

    except (IOError, Exception) as e:
        Log.error(f'triggered upload_to_azure failed : {str(e)}')

        error_message = "An error occurred while trying to upload to azure: " + str(e)
        print(error_message)
        raise ValueError(error_message)

from typing import List

from azure.storage.blob import ContainerClient, BlobClient

from src.azure_actions.azure_connaction import azure_connection
from src.logs import Log


def upload_files_to_azure_blob(account_name: str, container_name: str, blob_name: str, local_file_paths: List[str]):
    Log.info('Validation upload_to_azure started')
    try:

        container_client: ContainerClient = azure_connection(account_name, container_name)

        for local_file_path in local_file_paths:
            destination_blob_name: str = f"{blob_name}/input/{local_file_path}"
            blob_client: BlobClient = container_client.get_blob_client(destination_blob_name)

            with open(local_file_path, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
        Log.info('done activate - Validation upload_to_azure ')

    except (IOError, Exception) as e:
        error_message = "An error occurred while trying to upload to Azure: " + str(e)
        Log.error(f'Validation upload_to_azure failed: {error_message}')
        raise ValueError(error_message)

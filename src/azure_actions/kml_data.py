import os

from azure.core.paging import ItemPaged
from azure.storage.blob import BlobProperties

from src.azure_actions.azure_connaction import azure_connection
from src.logs import Log


def get_kml_data(account_name: str, container_name: str, folder_name: str) -> str:
    try:
        Log.info('validation get_kml_data started')

        container_client = azure_connection(account_name, container_name)

        subdirectory_path: str = f"{folder_name}/mission planning"

        # List blobs in the specified subdirectory
        blobs: ItemPaged[BlobProperties] = container_client.list_blobs(name_starts_with=subdirectory_path)

        # Iterate over blobs and print those with the specified extension
        target_extension: str = ".kml"
        for blob in blobs:
            if blob.name.lower().endswith(target_extension):
                blob_client = container_client.get_blob_client(blob.name)
                blob_name: str = os.path.basename(blob.name)
                with open(blob_name, "wb") as local_file:
                    blob_data = blob_client.download_blob()
                    blob_data.readinto(local_file)
                return blob_name
    except Exception as e:
        Log.error(f'validation get_kml_data failed: {str(e)}')
        error_message = "An error occurred while trying to get mission planning kml data: " + str(e)
        raise ValueError(error_message)

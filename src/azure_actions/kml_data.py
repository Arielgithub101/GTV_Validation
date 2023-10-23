import os

from azure.core.paging import ItemPaged
from azure.storage.blob import BlobProperties, ContainerClient

from src.config import Const
from src.azure_actions.azure_connaction import azure_connection
from src.logs import Log


def get_kml_data(account_name: str, container_name: str, folder_name: str) -> str:
    Log.info('validation get_kml_data started')
    try:

        container_client: ContainerClient = azure_connection(account_name, container_name)

        subdirectory_path: str = f"{folder_name}/{Const.MISSION_PLANNING}"

        # List blobs in the specified subdirectory
        blobs: ItemPaged[BlobProperties] = container_client.list_blobs(name_starts_with=subdirectory_path)

        # Iterate over blobs and print those with the specified extension
        for blob in blobs:
            if blob.name.lower().endswith(Const.KML_EXTENSION):
                blob_client = container_client.get_blob_client(blob.name)
                blob_name: str = os.path.basename(blob.name)
                with open(blob_name, "wb") as local_file:
                    blob_data = blob_client.download_blob()
                    blob_data.readinto(local_file)
                Log.info('done activate - validation get_kml_data ')
                return blob_name
        raise ValueError(
            f'error occurred while trying to get kml blob file from subdirectory_path : [{container_name}/{subdirectory_path}] '
            f' --> file not found')

    except Exception as e:
        error_message = "An error occurred while trying to get mission planning kml file data: " + str(e)
        Log.error(f'validation get_kml_data failed: {error_message}')
        raise ValueError(error_message)

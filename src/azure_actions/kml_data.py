import os

from src.azure_actions.azure_connaction import azure_connection
from src.azure_actions.blob_exist import does_blob_exist
from src.logs.logs import Log


def get_kml_data(account_name: str, container_name: str, folder_name: str) -> str:
    try:
        Log.info('triggered get_kml_data started')

        container_client = azure_connection(account_name, container_name)

        subdirectory_path: str = f"{folder_name}/mission planning"

        # List blobs in the specified subdirectory
        blobs = container_client.list_blobs(name_starts_with=subdirectory_path)

        # Iterate over blobs and print those with the specified extension
        target_extension = ".kml"
        for blob in blobs:
            if blob.name.lower().endswith(target_extension):

                # check for existing file in destination folder to prevent double copy
                if does_blob_exist(account_name, container_name, blob.name):
                    raise Exception(f"File {os.path.basename(blob.name)} already exists in folder 'input',cannot "
                                    f"create another one")

                blob_client = container_client.get_blob_client(blob.name)
                blob_name: str = os.path.basename(blob.name)
                with open(blob_name, "wb") as local_file:
                    blob_data = blob_client.download_blob()
                    blob_data.readinto(local_file)
                return blob_name
    except Exception as e:
        Log.error(f'triggered get_kml_data failed: {str(e)}')
        error_message = "An error occurred while trying to get mission planning kml data: " + str(e)
        raise ValueError(error_message)

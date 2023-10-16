from typing import Tuple
from azure.storage.blob import ContainerClient

from src.config import Const
from src.utils import tgv_to_csv
from src.azure_actions.azure_connaction import azure_connection
from src.logs import Log


def get_tgv_data(account_name: str, container_name: str, blob_name: str) -> Tuple[str, str]:
    Log.info('validation get_blob_data started')
    try:

        container_client: ContainerClient = azure_connection(account_name, container_name)
        subdirectory_path: str = f"{blob_name}/{Const.STATIC_FOLDER_MISC}"

        # List blobs in the specified subdirectory
        blobs = container_client.list_blobs(name_starts_with=subdirectory_path)

        # Iterate over the blobs to find those with the specified extension
        target_extension = Const.TGV_EXTENSION

        for blob in blobs:
            if blob.name.lower().endswith(target_extension):
                blob_client = container_client.get_blob_client(blob.name)
                blob_data = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
                blob_content = blob_data.readall()  # Assuming it's a text-based file
                output_file: str = tgv_to_csv(blob_content)

                Log.info('done activate - validation get_blob_data ')
                return output_file, blob.name
        raise ValueError(f'error occurred while trying to get blob data from subdirectory_path : {subdirectory_path}'
                         f' ,no file found')

    except TypeError as e:
        error_message = "An error occurred while trying to get blob data, check param info: " + str(e)
        Log.error(f'validation get_blob_data failed: {error_message}')
        raise ValueError(error_message)

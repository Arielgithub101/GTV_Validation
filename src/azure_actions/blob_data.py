from typing import Tuple

from azure.core.paging import ItemPaged
from azure.storage.blob import ContainerClient, StorageStreamDownloader, BlobClient, BlobProperties

from src.config import Const
from src.utils import tgv_to_csv
from src.azure_actions.azure_connaction import azure_connection
from src.logs import Log


def get_tgv_data(account_name: str, container_name: str, blob_name: str) -> Tuple[str, str]:
    Log.info('validation get_blob_data started')
    try:
        container_client: ContainerClient = azure_connection(account_name, container_name)

        subdirectory_path: str = f"{blob_name}/{Const.MISC}"

        # List blobs in the specified subdirectory
        blobs: ItemPaged[BlobProperties] = container_client.list_blobs(name_starts_with=subdirectory_path)

        # Iterate over the blobs to find those with the specified extension
        for blob in blobs:
            if blob.name.lower().endswith(Const.TGV_EXTENSION):
                blob_client: BlobClient = container_client.get_blob_client(blob.name)
                blob_data: StorageStreamDownloader = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
                blob_content = blob_data.readall()  # Assuming it's a text-based file

                output_file: str = tgv_to_csv(blob_content)

                Log.info('done activate - validation get_blob_data ')
                return output_file, blob.name
        raise ValueError(
            f'error occurred while trying to get tgv blob data from subdirectory_path : [{container_name}/{subdirectory_path}]'
            f' --> file not found')

    except Exception as e:
        error_message = "An error occurred while trying to get blob data : " + str(e)
        Log.error(f'validation get_blob_data failed: {error_message}')
        raise ValueError(error_message)

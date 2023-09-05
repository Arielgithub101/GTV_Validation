import os

from src.azure_actions.azure_connaction import azure_connection
from src.logs.logs import Log


def does_blob_exist(account_name: str, container_name: str, blob_name: str):
    Log.info('triggered does_blob_exist started')
    try:
        container_client = azure_connection(account_name, container_name)

        if os.path.basename(blob_name).endswith('tgv'):
            blob_name = blob_name.replace('misc', 'input')
        elif os.path.basename(blob_name).endswith('kml'):
            blob_name = blob_name.replace('mission planning', 'input')

        blob_client = container_client.get_blob_client(blob_name)
        # Check if the blob exists
        blob_exists = blob_client.exists()
        return blob_exists
    except Exception as e:
        Log.error(f'triggered does_blob_exist failed: {str(e)}')
        raise ValueError(str(e))

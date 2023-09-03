from src.azure_actions.azure_connaction import azure_connection
from src.logs.logs import Log


def upload_to_azure(account_name: str, container_name, folder_name, local_file_path):
    try:
        Log.info('triggered upload_to_azure started')

        print('in upload_to_azure')

        container_client = azure_connection(account_name, container_name)

        destination_blob_name = f"{folder_name}/input/{local_file_path}"
        blob_client = container_client.get_blob_client(destination_blob_name)

        with open(local_file_path, 'rb') as data:
            print('in upload_to_azure 2')
            blob_client.upload_blob(data)

    except (IOError, Exception) as e:
        Log.error('triggered upload_to_azure failed :', str(e))
        error_message = "An error occurred while trying to upload to azure: " + str(e)
        print(error_message)
        raise ValueError(error_message)

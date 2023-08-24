from starlette.responses import JSONResponse

from app.utils.Help_function import blob_convert_to_csv
from app.config.azure_config import ConfigConnection

from azure.storage.blob import BlobServiceClient


def azure_connection(account_name: str, container_name: str):
    connection_string = ConfigConnection.get_azure_connection_string(account_name)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service_client.get_container_client(container_name)
    return container_client


def get_blob_data(account_name: str, container_name: str, folder_name: str):
    try:

        container_client = azure_connection(account_name, container_name)
        subdirectory_path = f"{folder_name}/misc"

        # List blobs in the specified subdirectory
        blobs = container_client.list_blobs(name_starts_with=subdirectory_path)

        # Iterate over blobs and print those with the specified extension
        target_extension = ".tgv"
        for blob in blobs:
            if blob.name.lower().endswith(target_extension):
                blob_client = container_client.get_blob_client(blob.name)
                blob_data = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
                blob_content = blob_data.readall()  # Assuming it's a text-based file
                output_file = blob_convert_to_csv(blob_content)

                return blob.name, output_file
    except Exception as e:
        error_message = "An error occurred while connecting azure: " + str(e)
        print(error_message)
        raise ValueError(error_message)


# def get_kml_data(account_name: str, container_name: str, folder_name: str):
#     try:
#
#         container_client = azure_connection(account_name, container_name)
#
#         subdirectory_path = f"{folder_name}/mission planning"
#
#         # List blobs in the specified subdirectory
#         blobs = container_client.list_blobs(name_starts_with=subdirectory_path)
#
#         # Iterate over blobs and print those with the specified extension
#         target_extension = ".kml"
#         for blob in blobs:
#             if blob.name.lower().endswith(target_extension):
#                 blob_client = container_client.get_blob_client(blob.name)
#                 # blob_data = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
#                 # blob_content = blob_data.readall()  # Assuming it's a text-based file
#                 # output_file = blob_convert_to_csv(blob_content)
#                 blob_data = blob_client.download_blob()
#                 content = blob_data.readall()
#                 return content
#
#     except Exception as e:
#         error_message = "An error occurred while connecting azure: " + str(e)
#         print(error_message)
#         raise ValueError(error_message)


def upload_blob_to_azure(account_name: str, container_name, folder_name, local_file_path):
    try:

        container_client = azure_connection(account_name, container_name)

        destantion_blob_name = f"{folder_name}/input/{local_file_path}"
        blob_client = container_client.get_blob_client(destantion_blob_name)

        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data)
    except Exception as e:
        error_respose = {"error": str(e), 'message': 'blob my be alredy exist'}
        return JSONResponse(content=error_respose, status_code=500)

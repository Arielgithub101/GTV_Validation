import os

from starlette.responses import JSONResponse

from app.Help_function import blob_convert_to_csv

from azure.storage.blob import BlobServiceClient


def get_blob_data(container_name: str, folder_name: str):
    try:

        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)

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
        return 0, 0


def upload_blob_to_azure(container_name, folder_name, local_file_path):
    try:
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        full_blob_name = f"{folder_name}/input/{local_file_path}"
        blob_client = container_client.get_blob_client(full_blob_name)

        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data)
    except Exception as e:
        error_respose = {"error": str(e), 'message': 'blob my be alredy exist'}
        return JSONResponse(content=error_respose, status_code=500)


def azure_blob_exist(container_name, blob_name):
    # Define your connection string
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a reference to the container and blob
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Check if the blob exists
    blob_exists = blob_client.exists()
    print(blob_exists)
    return blob_exists

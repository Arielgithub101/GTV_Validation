import re
from azure.storage.blob import ContainerClient

from starlette.responses import JSONResponse

from src.config import Const
from src.logs import Log

from src.azure_actions.azure_connaction import azure_connection


def validation_files_directory(account_name: str, container_name: str, blob_name: str) -> JSONResponse:
    Log.info(f'validation_files_directory func started')
    try:
        container_client: ContainerClient = azure_connection(account_name, container_name)

        # List blobs in the specified subdirectory
        misc_blobs = container_client.list_blobs(name_starts_with=f"{blob_name}/{Const.MISC}")
        kml_blobs = container_client.list_blobs(name_starts_with=f"{blob_name}/{Const.MISSION_PLANNING}")

        errors = {
            "misc_error": f'tgv blob file not found in directory_path : [{container_name}/{f"{blob_name}/{Const.MISC}"}]'
                          f' --> file not found',
            "kml_error": f'kml blob file not found in directory_path  : [{container_name}/{f"{blob_name}/{Const.MISSION_PLANNING}"}]'
                         f' --> file not found'}

        for blob in misc_blobs:
            if blob.name.lower().endswith(Const.TGV_EXTENSION):
                errors.pop("misc_error")
                break

        for blob in kml_blobs:
            if blob.name.lower().endswith(Const.KML_EXTENSION):
                errors.pop("kml_error")
                break

        Log.info('done activate - validation_files_directory ')
        if not errors:
            return JSONResponse(content={"message": f"All files exist - {blob_name}"}, status_code=200)
        return JSONResponse(content={"error": errors}, status_code=404)

    except Exception as error_message:
        Log.error(f'validation_files_directory failed: {str(error_message)}')
        if "The specified container does not exist." in str(error_message):
            error_message = re.search("The specified container does not exist.", str(error_message))
            raise ValueError(error_message.group())
        raise ValueError(error_message)

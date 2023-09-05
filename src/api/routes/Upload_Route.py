import os
from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.azure_actions.blob_data import get_blob_data
from src.azure_actions.kml_data import get_kml_data
from src.azure_actions.upload import upload_to_azure
from src.logs.logs import Log
from src.utils.validation import df_validation
from src.utils.file_remove import delete_local_files
from src.models.input_model import FileInfo

router = APIRouter(
    prefix="/tgv_process"
)


@router.post("/")
def process_file(excel: FileInfo) -> JSONResponse:
    # validation that work on the blob data
    try:
        Log.info(f'triggered upload rout process_file started')
        try:
            local_blob_csv_data, blob_name = get_blob_data(excel.accunt_name, excel.container_name, excel.folder_name)
            local_kml_file = get_kml_data(excel.accunt_name, excel.container_name, excel.folder_name)
        except Exception as e:
            raise ValueError(str(e))

        # creat csv file for DataFrame to work with
        new_csv_file = df_validation(local_blob_csv_data, blob_name)

        # change extinction xlsx to tgv for uploading to azure
        local_tgv_file: str = new_csv_file.rsplit(".", 1)[0] + ".tgv"
        os.rename(new_csv_file, local_tgv_file)

        # uploading data to azure
        upload_to_azure(excel.accunt_name, excel.container_name, excel.folder_name, local_tgv_file)

        upload_to_azure(excel.accunt_name, excel.container_name, excel.folder_name, local_kml_file)

        # deleting the local files after uploading it to the azure
        delete_local_files(local_blob_csv_data, local_tgv_file, local_kml_file)

        return JSONResponse(content={"message": "new file created successfully and was upload to the azure storage",
                                     "azure_account": f'{excel.accunt_name}',
                                     "azure_container": f"{excel.container_name}",
                                     "azure_folder": f"{excel.folder_name}",
                                     "tgv file_name in azure folder": f'{local_tgv_file}',
                                     "kml file_name in azure folder": f'{local_kml_file}'},
                            status_code=200)
    except ValueError as e:
        Log.error(f'triggered upload rout process_file failed : {str(e)}')
        error_response = {"error": str(e)}
        return JSONResponse(content=error_response, status_code=400)

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.azure_actions import get_tgv_data, get_kml_data, upload_files_to_azure_blob
from src.config import Const
from src.logs import Log
from src.utils import df_tail_validation, delete_local_files, csv_to_tgv
from src.models import FileInfo
from src.validations import validation_files_directory

router = APIRouter(
    prefix="/tgv_process"
)


@router.post("/")
def process_file(file_data: FileInfo):
    Log.info(f'validation route process_file func started')
    # validation that work on the blob data
    try:
        files_directory_error: JSONResponse = validation_files_directory(file_data.account_name,
                                                                         file_data.container_name,
                                                                         file_data.blob_name)
        if files_directory_error.status_code != 200:
            return files_directory_error

        tgv_as_csv_data_file: str
        tgv_file_name: str
        tgv_as_csv_data_file, tgv_file_name = get_tgv_data(file_data.account_name, file_data.container_name,
                                                           file_data.blob_name)

        kml_data_file: str = get_kml_data(file_data.account_name, file_data.container_name, file_data.blob_name)

        # create csv file for DataFrame to work with
        new_csv_file: str = df_tail_validation(tgv_as_csv_data_file, tgv_file_name)

        # change extinction to tgv for uploading to azure
        tgv_data_file: str = new_csv_file.rsplit(".", 1)[0] + Const.TGV_EXTENSION

        csv_to_tgv(new_csv_file, tgv_data_file)

        # uploading data to azure
        upload_files_to_azure_blob(file_data.account_name, file_data.container_name, file_data.blob_name,
                                   [tgv_data_file, kml_data_file])

        # deleting the local files after uploading it to the azure
        delete_local_files([new_csv_file, tgv_as_csv_data_file, tgv_data_file, kml_data_file])

        Log.info(f'done activate validation route process_file ')

        return JSONResponse(content={"message": "new file created successfully and was upload to the azure storage",
                                     "azure_account": f'{file_data.account_name}',
                                     "azure_container": f"{file_data.container_name}",
                                     "azure_folder": f"{file_data.blob_name}",
                                     "tgv file_name in azure folder": f'{tgv_data_file}',
                                     "kml file_name in azure folder": f'{kml_data_file}'},
                            status_code=200)
    except (Exception, ValueError) as e:
        error_response = {"error": str(e)}
        Log.error(f'validation upload rout process_file func failed : {error_response}')
        return JSONResponse(content=error_response, status_code=400)

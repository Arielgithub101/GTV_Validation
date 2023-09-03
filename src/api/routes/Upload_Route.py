import os

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.azure_actions.blob_data import get_blob_data
from src.azure_actions.kml_data import get_kml_data
from src.azure_actions.upload import upload_to_azure

from src.logs.logs import Log

from src.utils.validation import df_validation
from src.models.input_model import FileInfo

router = APIRouter(
    prefix="/tgv_process"
)


@router.post("/")
def process_file(excel: FileInfo) -> JSONResponse:
    # validation that work on the blob data
    try:
        Log.info('triggered upload rout process_file started')
        try:
            local_blob_csv_data, blob_name = get_blob_data(excel.accunt_name, excel.container_name, excel.folder_name)
            local_kml_file = get_kml_data(excel.accunt_name, excel.container_name, excel.folder_name)
        except Exception as e:
            error_message = "An error occurred while connecting azure, check connection info : " + str(e)
            return JSONResponse(content=error_message, status_code=400)

        new_csv_file = df_validation(local_blob_csv_data, blob_name)

        # change extantion xlsx to tgv
        local_tgv_file = new_csv_file.rsplit(".", 1)[0] + ".tgv"
        os.rename(new_csv_file, local_tgv_file)

        print('befor upload')
        # breakpoint()
        # upload_to_azure(excel.accunt_name, excel.container_name, excel.folder_name, local_tgv_file)
        #
        # upload_to_azure(excel.accunt_name, excel.container_name, excel.folder_name, local_kml_file)
        print('after upload ')

        os.remove(local_blob_csv_data)
        os.remove(local_tgv_file)
        os.remove(local_kml_file)

        return JSONResponse(content={"message": "new file created successfully and was upload to the azure storage",
                                     "azure_account": f'{excel.accunt_name}',
                                     "azure_container": f"{excel.container_name}",
                                     "azure_folder": f"{excel.folder_name}",
                                     "tgv file_name in azure folder": f'{local_tgv_file}',
                                     "kml file_name in azure folder": f'{local_kml_file}'},
                            status_code=200)
    except ValueError as e:
        Log.error('triggered upload rout process_file failed :', str(e))
        error_response = {"error": str(e)}
        return JSONResponse(content=error_response, status_code=400)

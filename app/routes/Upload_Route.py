import os

import pandas as pd
from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.utils.Azure_connaction import get_blob_data, upload_blob_to_azure
from app.utils.Help_function import df_validation, tgv_2_xlsx
from app.Validation.BM_validation import FileInfo

router = APIRouter(
    prefix="/tgv_process"
)


@router.post("/")
def process_file(excel: FileInfo):
    # validation that work on the blob data
    try:

        try:
            blob_name, local_blob_csv_data = get_blob_data(excel.accunt_name, excel.container_name, excel.folder_name)
        except Exception as e:
            error_message = "An error occurred while connecting azure, check connection info : " + str(e)
            return JSONResponse(content=error_message, status_code=400)

        new_file_name = df_validation(local_blob_csv_data, blob_name)

        directory, filename = os.path.split(new_file_name)
        new_filename = os.path.splitext(filename)[0] + ".tgv"
        new_tgv_path = os.path.join(directory, new_filename)
        os.rename(new_file_name, new_tgv_path)

        upload_blob_to_azure(excel.accunt_name, excel.container_name, excel.folder_name, new_tgv_path)
        os.remove(local_blob_csv_data)
        os.remove(new_tgv_path)

        return JSONResponse(content={"message": "new file created successfully and was upload to the azure storage",
                                     "azure_account": f'{excel.accunt_name}',
                                     "azure_container": f"{excel.container_name}",
                                     "azure_folder": f"{excel.folder_name}",
                                     "file_name in a": f'{new_tgv_path}'},
                            status_code=200)

    except ValueError as e:
        error_respose = {"error": str(e)}
        return JSONResponse(content=error_respose, status_code=400)

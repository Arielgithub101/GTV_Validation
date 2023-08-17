import os
import openpyxl
import pandas as pd

from fastapi import APIRouter
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from app.Help_function import tgv_2_xlsx
from app.Validation.BM_validation import ExcelProcessing
from app.Azure_connaction import get_blob_data, upload_blob_to_azure

router = APIRouter(
    prefix="/process_excel"
)


# load_dotenv('.env')
# azure_accunt = os.getenv('AZURE_ACCUNT_NAME')
# azure_key = os.getenv('AZURE_KEY')


@router.post("/")
def process_excel_route(excel: ExcelProcessing):
    try:
        blob_name, local_blob_csv_data = get_blob_data(excel.container_name, excel.folder_name)

        df = pd.read_csv(local_blob_csv_data, header=None)

        # Specify the columns to check (B, C, and D)
        columns_to_check = df.iloc[:, 1:4]

        # Iterate over all rows and columns
        for index, row in df.iterrows():
            for column in columns_to_check:
                cell_value = row[column]
                if -1 <= cell_value <= 1:
                    # If any value in columns B, C, or D is between -1 and 1, set all three cells to 0
                    df.at[index, 1] = 0
                    df.at[index, 2] = 0
                    df.at[index, 3] = 0

        new_file_name = tgv_2_xlsx(blob_name)

        df.to_excel(new_file_name, index=False)

        directory, filename = os.path.split(new_file_name)
        new_filename = os.path.splitext(filename)[0] + ".tgv"
        new_tgv_path = os.path.join(directory, new_filename)
        os.rename(new_file_name, new_tgv_path)

        upload_blob_to_azure(excel.container_name, excel.folder_name, new_tgv_path)

        os.remove(local_blob_csv_data)
        os.remove(new_tgv_path)

        return JSONResponse(content={"message": "new file created successfully and was upload to the azure storage",
                                     "file_name": f'{new_tgv_path}'},
                            status_code=200)
    except ValueError as e:
        error_respose = {"error": str(e)}
        return JSONResponse(content=error_respose, status_code=500)

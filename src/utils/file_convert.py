import io
import csv
import pandas as pd

from src.config import Const
from src.logs import Log


def tgv_to_csv(tgv_blob_content):
    Log.info('validation tgv_to_csv started')
    try:
        output_file = Const.NEW_OUTPUT

        # Create a DataFrame from the TSV content
        df = pd.read_csv(io.StringIO(tgv_blob_content), header=None, delimiter='\t')

        # Save the DataFrame as a CSV file
        df.to_csv(output_file, header=False, index=False)

        Log.info('done activate - validation tgv_to_csv ')
        return output_file
    except Exception as e:
        error_message: str = "An error occurred while converting blob data to csv: " + str(e)
        Log.error(f'validation tgv_to_csv failed : {error_message}')
        raise ValueError(error_message)


def csv_to_tgv(csv_file_path, tgv_file_path):
    Log.info('validation csv_to_tgv started')
    try:
        # Read the edited CSV file and convert it to TGV format
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip the first row (headers)
            next(csv_reader, None)
            tgv_data = '\n'.join(['\t'.join(row) for row in csv_reader])

        # Save the updated TGV data back to the TGV file
        with open(tgv_file_path, 'w', newline='') as tgv_file:
            tgv_file.write(tgv_data)
        Log.info('done activate - validation csv_to_csv ')
    except Exception as e:
        error_message: str = "An error occurred while converting csv_to_tgv data : " + str(e)
        Log.error(f'validation csv_to_tgv failed : {error_message}')
        raise ValueError(error_message)

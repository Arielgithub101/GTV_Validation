import os
from typing import List
import pandas as pd
import numpy as np

from src.config.config import DEVIATION_RANGE
from src.logs.logs import Log
from src.utils.file_remove import delete_local_files


def df_validation(local_blob_csv_data: str, blob_name: str) -> str:
    try:
        Log.info('triggered df_validation started')

        df = pd.read_csv(local_blob_csv_data, header=None)

        values_to_median: List = []
        # Iterate over the DataFrame
        for index, row in df.iterrows():
            if not (-1 <= row[1] <= 1 or -1 <= row[2] <= 1 or -1 <= row[3] <= 1):
                # If none of the values in columns B, C, or D are between -1 and 1, append the value from column D
                values_to_median.append(row[3])

        # Calculate the median of the values in the list
        median_value = np.median(values_to_median)

        # check which should be deleted by checking if the DEVIATION_RANGE is to big/small
        rows_to_delete = df[
            (df.iloc[:, 3] > median_value + DEVIATION_RANGE) | (df.iloc[:, 3] < median_value - DEVIATION_RANGE)]

        # Drop the rows marked for deletion
        df = df.drop(rows_to_delete.index)

        file_name: str = os.path.basename(blob_name)
        new_file_name: str = file_name.rsplit(".", 1)[0] + ".xlsx"

        df.to_excel(new_file_name, index=False)

        return new_file_name
    except Exception as e:
        Log.error(f'triggered df_validation failed : {e}')
        delete_local_files(local_blob_csv_data)
        error_message: str = "An error occurred while reading and validating local_blob_csv_data : " + str(e)
        raise ValueError(error_message)

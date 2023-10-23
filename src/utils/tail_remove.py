import os
from typing import List

import pandas as pd
import numpy as np

from src.config import Config
from src.logs import Log
from src.utils.file_remove import delete_local_files


def df_tail_validation(local_blob_csv_data: str, blob_name: str) -> str:
    Log.info('validation df_validation started')
    try:
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
            (df.iloc[:, 3] > median_value + Config.DEVIATION_RANGE) | (df.iloc[:, 3] < median_value - Config.DEVIATION_RANGE)]

        # Drop the rows marked for deletion
        df = df.drop(rows_to_delete.index)

        file_name: str = os.path.basename(blob_name)

        file_name, old_extension = os.path.splitext(file_name)  # Split into name and extension
        new_file_name = file_name + ".csv"

        df.to_csv(new_file_name, index=False)
        # return new_file_name
        Log.info('done activate - validation df_validation ')
        return new_file_name
    except Exception as e:
        error_message: str = "An error occurred while reading and validating local_blob_csv_data : " + str(e)
        Log.error(f'validation df_validation failed : {error_message}')
        delete_local_files([local_blob_csv_data])
        raise ValueError(error_message)

import os

import pandas as pd
import numpy as np

from src.config.config import DEVIATION_RANGE
from src.logs.logs import Log


def df_validation(local_blob_csv_data: str, blob_name: str) -> str:
    try:
        Log.info('triggered df_validation started')

        df = pd.read_csv(local_blob_csv_data, header=None)
        #
        # # Specify the columns to check (B, C, and D)
        # columns_to_check = df.iloc[:, 1:4]
        #
        # # Iterate over all rows and columns
        # for index, row in df.iterrows():
        #     for column in columns_to_check:
        #         cell_value = row[column]
        #         if -1 <= cell_value <= 1:
        #             # If any value in columns B, C, or D is between -1 and 1, set all three cells to 0
        #             df.at[index, 1] = 0
        #             df.at[index, 2] = 0
        #             df.at[index, 3] = 0
        #
        # # If any value in columns D is above or under 100 (or a givan parameter), delet rows
        # counter_greater_than_0 = (df.iloc[:, 3] > 0).sum()
        # sum_val_height_colm_d = df.iloc[:, 3].sum()
        # height_avg = sum_val_height_colm_d / counter_greater_than_0
        #
        # rows_to_delete = df[(df.iloc[:, 3] > height_avg + DEVIATION_RANGE) | (df.iloc[:, 3] < height_avg - DEVIATION_RANGE)]
        #
        # df = df.drop(rows_to_delete.index)
        mask = (df[3] < -1) | (df[3] > 1)
        filtered_values = df.loc[mask, 3]
        median_value = np.median(filtered_values)

        # Iterate over the rows and mark rows for deletion
        rows_to_delete = []
        for index, row in df.iterrows():
            if abs(row[3] - median_value) > DEVIATION_RANGE:
                rows_to_delete.append(index)

        # Drop the rows marked for deletion
        df = df.drop(rows_to_delete)

        file_name = os.path.basename(blob_name)
        new_file_name = file_name.rsplit(".", 1)[0] + ".xlsx"

        df.to_excel(new_file_name, index=False)

        return new_file_name
    except Exception as e:
        Log.error('triggered df_validation failed :', str(e))
        error_message: str = "An error occurred while reading and validating local_blob_csv_data : " + str(e)
        raise ValueError(error_message)

import csv
import os
import pandas as pd


def blob_convert_to_csv(blob_content):
    # Split the input string into lines
    lines = blob_content.strip().split('\n')

    # Initialize a list to store rows of CSV data
    csv_data = []

    # Split each line into values and append to csv_data
    for line in lines:
        values = line.split()
        csv_data.append(values)

    # Specify the CSV output file path
    output_file = 'new_output.csv'

    # Open the CSV file in write mode
    with open(output_file, mode='w', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)
        # Write each row of CSV data
        csv_writer.writerows(csv_data)

    return output_file


def tgv_2_xlsx(blob_name):
    base_name = os.path.basename(blob_name)
    file_name, old_extension = os.path.splitext(base_name)  # Split into name and extension
    new_extension = '.xlsx'
    new_file_name = file_name + new_extension
    return new_file_name


def df_validation(local_blob_csv_data, blob_name) -> str:
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

    # If any value in columns D is abov or under 100, delet rows

    counter_greater_than_0 = (df.iloc[:, 3] > 0).sum()
    sum_val_height_colm_d = df.iloc[:, 3].sum()
    height_avg = sum_val_height_colm_d / counter_greater_than_0

    rows_to_delete = df[(df.iloc[:, 3] > height_avg + 100) | (df.iloc[:, 3] < height_avg - 100)]

    df = df.drop(rows_to_delete.index)

    new_file_name = tgv_2_xlsx(blob_name)

    df.to_excel(new_file_name, index=False)

    return new_file_name

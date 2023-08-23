import csv
import os


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
    print('in rout1 in func2')

    base_name = os.path.basename(blob_name)
    file_name, old_extension = os.path.splitext(base_name)  # Split into name and extension
    new_extension = '.xlsx'
    new_file_name = file_name + new_extension
    return new_file_name

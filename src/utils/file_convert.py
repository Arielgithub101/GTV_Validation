import csv
from src.logs.logs import Log


def blob_convert_to_csv(blob_content) -> str:
    try:
        Log.info('triggered blob_convert_to_csv started')

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
    except Exception as e:
        Log.error('triggered blob_convert_to_csv failed :', str(e))
        error_message: str = "An error occurred while converting blob data to csv: " + str(e)
        raise ValueError(error_message)

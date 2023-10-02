import os
import unittest
from pathlib import Path

# from fastapi.testclient import TestClient
from src.api.service import app
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from src.azure_actions import azure_connection, get_tgv_data, get_kml_data


# client = TestClient(app)


class TestTGVProcess(unittest.TestCase):
    def test_example(self):
        self.assertTrue(True)

    # def test_connaction_to_azure(self):
    #     container_client = azure_connection('infinity100', "test")
    #     container = type(container_client)
    #     self.assertEqual(container, container_client)

    def test_tgv_data(self):
        csv_file, tgv_file = get_tgv_data('infinity100', "test", '09032023_10_112')
        target_extension = '.tgv'
        file_extension = Path(tgv_file).suffix

        self.assertEqual(type(csv_file), str)
        self.assertEqual(target_extension, file_extension)

        folder_without_tgv_file = '09032023_10_112T'
        with self.assertRaises(Exception):  # Check if the function raises an exception
            csv_file, tgv_file = get_tgv_data('infinity100', 'test', folder_without_tgv_file)

        os.remove('new_output.csv')

    def test_kml_data(self):
        kml_data_file = get_kml_data('infinity100', "test", '09032023_10_112')
        target_extension = '.kml'
        file_extension = Path(kml_data_file).suffix

        self.assertEqual(target_extension, file_extension)

        folder_without_kml_file = '09032023_10_112T'
        with self.assertRaises(Exception):  # Check if the function raises an exception
            kml = get_kml_data('infinity100', 'test', folder_without_kml_file)
        os.remove(kml)











    # def tearDown(self):
    #     # Remove the temporary directory and its contents
    #     os.remove('new_output.csv')

# def test_process_file(self):
#     # Define your test input data (FileInfo)
#     excel_payload = {
#         "accunt_name": "infinity100",
#         "container_name": "test",
#         "folder_name": "09032023_10_112",
#     }
#
#     # Send a POST request to your FastAPI endpoint
#     response = client.post("/tgv_process/", json=excel_payload)
#
#     # Check if the response status code is 200 (success)
#     self.assertEqual(response.status_code, 200)
#
#     # Extract the file names from the response
#     response_data = response.json()
#     tgv_file_name = response_data["tgv file_name in azure folder"]
#
#     # Create Azure BlobServiceClient
#     blob_service_client = BlobServiceClient.from_connection_string(
#         "DefaultEndpointsProtocol=https;AccountName=infinity100;AccountKey=SeGu9dyNWBtg"
#         "/xJI8tG5VsEPGuMkBLEOhqwrRqAnIdYSEJCS6qkQ8qXZ1uFiRlRywCIgp80d+Xs3+AStJH0TWw==;EndpointSuffix=core.windows"
#         ".net")
#
#     # Get a reference to your test container
#     container_client = blob_service_client.get_container_client("test")
#
#     # Download the output file from Azure Blob Storage
#     blob_client = container_client.get_blob_client(f"valid_output/{tgv_file_name}")
#     downloaded_blob = blob_client.download_blob()
#
#     # Read the content of the downloaded blob
#     downloaded_content = downloaded_blob.readall()
#
#     # Perform your comparison tests here
#     # You can compare the 'downloaded_content' with the expected valid output
#
# def test_invalid_input(self):
#     # Define a test with invalid input data (FileInfo)
#     excel_payload = {
#         "accunt_name": "invalid_account_name",
#         "container_name": "your_container_name",
#         "folder_name": "invalid_input",
#     }
#
#     # Send a POST request to your FastAPI endpoint with invalid input
#     response = client.post("/tgv_process/", json=excel_payload)
#
#     # Check if the response status code is 400 (error)
#     self.assertEqual(response.status_code, 400)

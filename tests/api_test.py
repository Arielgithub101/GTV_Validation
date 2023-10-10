import os
from pathlib import Path

import pytest
from src.azure_actions import get_tgv_data, get_kml_data

from fastapi.testclient import TestClient
from src.api.service import app  # Assuming 'main.py' contains your FastAPI application

client = TestClient(app)


def test_process_file_endpoint():
    data_body = {
        "account_name": "infinity100",
        "container_name": "test",
        "blob_name": "09032023_10_112"
    }
    response = client.post("/tgv_process/", json=data_body)
    assert response.status_code == 200
    assert response.json()["message"] == "new file created successfully and was upload to the azure storage"


def test_process_file_invalid_data():
    invalid_data = {
        "account_name": "infinity10",
        "container_name": "test",
        "blob_name": "09032023_10_11"
    }
    response = client.post("/tgv_process/", json=invalid_data)
    assert response.status_code == 400



def test_process_file_exception_handling():
    response = client.post("/tgv_process/", json={})
    assert response.status_code == 422


def test_tgv_data():
    csv_file, tgv_file = get_tgv_data('infinity100', 'test', '09032023_10_112')
    target_extension = '.tgv'
    output_file_extension = Path(tgv_file).suffix
    os.remove('new_output.csv')  # Assuming this file is created during the test

    assert isinstance(csv_file, str)
    assert target_extension == output_file_extension
def test_kml_data():
    kml_data_file = get_kml_data('infinity100', 'test', '09032023_10_112')
    target_extension = '.kml'
    file_extension = Path(kml_data_file).suffix
    os.remove(kml_data_file)  # Assuming this file is created during the test

    assert isinstance(kml_data_file, str)
    assert target_extension == file_extension


def test_exception_kml_data():
    folder_without_kml_file = 'ariel_test_folder'
    with pytest.raises(Exception):
        get_kml_data('infinity100', 'test', folder_without_kml_file)


def test_exception_tgv_data():
    folder_without_tgv_file = 'ariel_test_folder'
    with pytest.raises(Exception):
        get_tgv_data('infinity100', 'test', folder_without_tgv_file)


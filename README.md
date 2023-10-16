# TGV File Validation README

## Table of Contents

- [Overview](#overview)
- [Validation Process](#validation-process)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Additional Notes](#additional-notes)

## Overview

Welcome to the TGV File Validation project! This project focuses on the validation of information coming from TGV files. The validation process is divided into three key parts:

1. **Input Validation**: Ensure that the input data meets the required criteria, filtering out invalid or incomplete data.

2. **Connecting to Azure and Downloading a Specific TGV File**: Establish a connection to Azure and download the TGV file that you want to validate.

3. **Validation on the File and Upload Back to Azure**: Validate the downloaded TGV file based on your specific criteria. Once validated, the file is uploaded back to Azure.

This README will guide you through the project's purpose, the Docker deployment process, and how to configure necessary environment variables.

## Validation Process

The project follows a three-step validation process as mentioned earlier. Each step plays a crucial role in ensuring the quality and accuracy of the data you are working with.

## Docker Deployment

For easy deployment, the TGV File Validation project can be run using Docker. Below are the Docker deployment parameters:

- **Flags** : -d --restart unless-stopped
- **Name (--name)**: tgv_validation
- **Port (-p)**: Map a local port (e.g., 9900) to the VM port (also 9900) to access the service.
- **Environment Variables (-e)**: To run the project with Docker, make sure to set the following environment variables:

    1. **skylinepublic_connection_string**: Azure connection string for the Skylinepublic container.
    2. **infinity100_connection_string**: Azure connection string for the Infinity100 container.
    3. **logs_file_path**: Path for log files generated during the validation process.
    4. **deviation_range**: Specify the deviation range for your validation criteria (e.g., 100).

- **Volume (-v)**: Mount a host log file into the Docker container. This allows for logs to be saved outside the container for easier access and analysis
- -->"/home/azureuser/logs/validation_logs.txt:/home/azureuser/logs/validation_logs.txt:z " .

## Environment Variables

Before running the project, ensure that the required environment variables are correctly configured. These variables are essential for the project's functionality and validation processes.

## Running the Project

To get started with the TGV File Validation project, follow these steps:

1. Set the required environment variables as mentioned in [Environment Variables](#environment-variables).

2. Build and deploy the project using Docker with the provided deployment parameters.

## Additional Notes

- Be sure to replace `IMAGE ID (example -> externalacraction.azurecr.io/infinity/tgv_validation:0.0.8 .
)` with the actual Docker image identifier that corresponds to your project.

- Customize this README to include specific instructions for your project, such as installation details, usage examples, and additional documentation.

"""
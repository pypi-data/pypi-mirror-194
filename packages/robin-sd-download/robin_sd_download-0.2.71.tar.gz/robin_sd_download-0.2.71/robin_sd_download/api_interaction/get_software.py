#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import zipfile
import datetime

from robin_sd_download.api_interaction import get_bearer_token
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger


def get_software():
    config = yaml_parser.parse_config()

    radar_id = config['radar_id']
    request_url = config['api_url']

    current_date = datetime.datetime.now().strftime("%d%m%Y%H%M%S")

    try:
        bearer_token = str(get_bearer_token.get_bearer_token())
    except Exception as e:
        logger.log(message=f"Failed to get bearer token: {str(e)}", log_level="error", to_file=True, to_terminal=True)
        return 1

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_endpoint = '/api/radars/' + radar_id + '/software'

    try:
        response = requests.get(request_url + api_endpoint, allow_redirects=True, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.log(message=f"Failed to get software: {str(e)}", log_level="error", to_file=True, to_terminal=True)
        return 1

    # Get the name of the file
    file_name = response.headers.get("Content-Disposition").split("=")[1]
    file_name = file_name.replace('"', '')
    file_name = file_name.replace('.zip', '')

    # Define the location to save the file
    file_location = config['static']['download_location']

    try:
        # Create the destination folder
        os.makedirs(file_location, exist_ok=True)

        # Write the file to disk
        write_file = os.path.join(file_location, f"{file_name}_{current_date}.zip")

        with open(write_file, 'wb') as f:
            f.write(response.content)
            f.close()

            logger.log(message="Downloaded to " + write_file, log_level="info", to_file=True, to_terminal=True)

        # Extract the file
        try:
            with zipfile.ZipFile(write_file, "r") as zip_ref:
                zip_ref.extractall(os.path.join(file_location, f"{file_name}_{current_date}"))
        except zipfile.BadZipFile:
            logger.log(message="The downloaded file is not a valid zip file", log_level="error", to_file=True, to_terminal=True)
            return 1

        # Remove the zip file
        os.remove(write_file)

    except Exception as e:
        logger.log(message=f"Failed to download software: {str(e)}", log_level="error", to_file=True, to_terminal=True)
        return 1

    return 0

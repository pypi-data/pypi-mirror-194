#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime

from robin_sd_download.api_interaction import get_bearer_token
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger


def get_software_info():
    config = yaml_parser.parse_config()

    radar_id = config['radar_id']
    request_url = config['api_url']

    try:
        bearer_token = str(get_bearer_token.get_bearer_token())
    except Exception as e:
        logger.log(message=f"Failed to get bearer token: {str(e)}", log_level="error", to_file=True, to_terminal=True)
        return None

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_endpoint = '/api/radars/' + radar_id

    try:
        response = requests.get(request_url + api_endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.log(message=f"Failed to get software info: {str(e)}", log_level="error", to_file=True, to_terminal=True)
        return None

    # log full response for debugging
    # logger.log(message=f"Software info response: {response.json()}", log_level="debug", to_file=True, to_terminal=True)

    software_info = response.json()['radar']['software']

    # Extract the relevant information from the software object
    software = {
        'id': software_info['_id'],
        'software_path': software_info['softwarePath'],
        'software_type': software_info['softwareType'],
        'radar_type': software_info['radarType'],
        'version': software_info['version'],
        'recalled': software_info['recalled'],
        'available_for_all': software_info['availableForAll'],
        'created_at': datetime.datetime.strptime(software_info['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        'updated_at': datetime.datetime.strptime(software_info['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    }

    # Format the output
    output = f"Software info for radar {radar_id}\n"
    output += f"Software ID: {software['id']}\n"
    # output += f"Software path: {software['software_path']}\n"
    output += f"Software type: {software['software_type']}\n"
    output += f"Radar type: {', '.join(software['radar_type'])}\n"
    output += f"Version: {software['version']}\n"
    output += f"Recalled: {software['recalled']}\n"
    # output += f"Available for all: {software['available_for_all']}\n"
    output += f"Created at: {software['created_at']}\n"
    output += f"Updated at: {software['updated_at']}\n"

    # logger.log(message=output, log_level="info", to_file=True, to_terminal=True)

    return output

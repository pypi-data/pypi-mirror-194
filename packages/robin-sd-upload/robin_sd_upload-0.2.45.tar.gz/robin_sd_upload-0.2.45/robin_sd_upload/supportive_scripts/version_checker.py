#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pypi_simple import PyPISimple
import sys

from robin_sd_upload.supportive_scripts import logger
from robin_sd_upload.supportive_scripts import yaml_parser
from robin_sd_upload import _version

def check_latest_version():
    """Check if the latest version is installed and document how to update if needed."""
    config = yaml_parser.parse_config()

    package_name = config['static']['app_name']
    # print('package_name is: ' + package_name)

    current_version = _version.__version__
    
    pypi = PyPISimple()
    page = pypi.get_project_page(package_name)
    latest_version = page.packages[-1].version

    # package_url = page.packages[-1].url
    # print('latest_version is: ' + latest_version)
    # print ('package_url is: ' + package_url)
    if current_version == latest_version:
        logger.log(message="Latest version detected, proceeding.", log_level="info", to_file=True, to_terminal=False)
    else:
        logger.log(message="Newer version detected, please update.", log_level="error", to_file=True, to_terminal=True)
        logger.log(message="Current version: " + current_version, log_level="error", to_file=True, to_terminal=True)
        logger.log(message="Latest version: " + latest_version, log_level="error", to_file=True, to_terminal=True)
        logger.log(message="To update, run: pip3 install --upgrade " + package_name, log_level="error", to_file=True, to_terminal=True)
        sys.exit(1)

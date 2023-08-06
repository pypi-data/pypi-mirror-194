#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from robin_sd_upload.supportive_scripts import logger

def check_upload_file(upload_file, version_name):
    # make sure not double / in path
    if upload_file.endswith("/"):
        upload_file = upload_file[:-1]
    # creating path from upload_file and version_name
    upload_file = upload_file + "/" + version_name
    logger.log(message="Checking upload file: " + upload_file, log_level="info", to_file=True, to_terminal=True)
    if os.path.isdir(upload_file):
        logger.log(message="File is valid and exist: " + upload_file, log_level="info", to_file=True, to_terminal=True)
        for root, dirs, files in os.walk(upload_file):
            # logger.log(message="Root: " + root, log_level="info", to_file=True, to_terminal=True)
            for file in files:
                # logger.log(message="File: " + file, log_level="info", to_file=True, to_terminal=True)
                if file == "Packages.gz" or file == "Packages":
                    logger.log(message="Packages file found: " + file + " at " + root, log_level="info", to_file=True, to_terminal=True)
                    return True
        logger.log(message="Packages file not found", log_level="error", to_file=True, to_terminal=True)
        #log path to file
        logger.log(message="Path to file: " + upload_file, log_level="error", to_file=True, to_terminal=True)
        return False
    else:
        logger.log(message="File not exist: " + upload_file, log_level="error", to_file=True, to_terminal=True)
        return False

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile

from robin_sd_upload.supportive_scripts import logger

def create_zip(directory, zipped_file_path, version_name):
# Create a ZipFile object
    zip_file = zipfile.ZipFile(os.path.join(zipped_file_path, version_name + ".zip"), "w")
    
    # Iterate over all the files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the file path
            file_path = os.path.join(root, file)

            # Add the file to the zip file
            zip_file.write(file_path, os.path.join(version_name, os.path.relpath(file_path, directory)))
            
    logger.log(message="ZIP file created: " + os.path.join(zipped_file_path, version_name + ".zip"), log_level="info", to_file=True, to_terminal=True)
    # Close the ZipFile
    zip_file.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from robin_sd_upload.supportive_scripts import logger

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        logger.log(message="Folder created: " + folder, log_level="info", to_file=True, to_terminal=True)
        logger.log(message="try to run script again", log_level="info", to_file=True, to_terminal=True)
        logger.log(message="Exiting script", log_level="info", to_file=True, to_terminal=True)
        exit()
    else:
        logger.log(message="Folder already exist: " + folder, log_level="info", to_file=True, to_terminal=True)
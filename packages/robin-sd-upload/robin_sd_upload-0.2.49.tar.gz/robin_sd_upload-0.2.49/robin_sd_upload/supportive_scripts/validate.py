#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import validators
from robin_sd_upload.supportive_scripts import logger

def validate(radarType, version_name):
    radarTypearray = ["elvira", "iris", "birdradar"]
    if validators.length(radarType, min=1, max=50) == False:
        logger.log(message="Radar type is not valid: " + radarType, log_level="error", to_file=True, to_terminal=True)
        # print("Radar type is not valid: " + radarType)
        exit()
    if radarType not in radarTypearray:
            logger.log(message="Radar type is not valid: " + radarType, log_level="error", to_file=True, to_terminal=True)    
            # print("Radar type is not valid: " + radarType)
            exit()
    else:
        logger.log(message="Radar type is valid: " + radarType, log_level="info", to_file=True, to_terminal=True)
        # print("Radar type is valid: " + radarType)
        
    if validators.length(version_name, min=1, max=20) == False:
        logger.log(message="Version name is not valid: " + version_name, log_level="error", to_file=True, to_terminal=True)
        # print("Version name is not valid: " + version_name)
        exit()
    else:
        logger.log(message="Version name is valid: " + version_name, log_level="info", to_file=True, to_terminal=True)
        # print("Version name is valid: " + version_name)
        return radarType, version_name

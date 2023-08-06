#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import argparse
import sys

from robin_sd_upload import _version
from robin_sd_upload.slack_interaction import slack_handler
from robin_sd_upload.supportive_scripts import yaml_parser
from robin_sd_upload.supportive_scripts import logger
from robin_sd_upload.supportive_scripts import version_checker

from robin_sd_upload.api_interaction import push_software
from robin_sd_upload.supportive_scripts import check_upload_file
from robin_sd_upload.supportive_scripts import validate
from robin_sd_upload.supportive_scripts import create_zip
from robin_sd_upload.supportive_scripts import remove_zip

def arg_parser():
    parser = argparse.ArgumentParser(
        description='Robin Radar Systems - Software Uploader',
        usage='robin-sd-upload [options]',
        prog='Robin Radar Systems Software Uploader',
        epilog='To report any bugs or issues, please visit: \
        https://support.robinradar.systems or run: robin-sd-upload --slack'
    )

    parser.add_argument('-c', '--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('-u', '--upload', action='store_true', help='upload software: robin-sd-upload --upload --type=radar_type --number=version_number --path=upload_folder_path')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=_version.__version__))
    parser.add_argument('-s', '--slack', action='store_true', help='Send the logs to IT/DevOps Slack channel')

    # arguments for upload
    parser.add_argument('-t', "--type", type=str, help="radar type")
    parser.add_argument('-n', "--number", type=str, help="version number of the software")
    parser.add_argument('-p', "--path", type=str, help="upload file absolute path")

    args = parser.parse_args()
    config = yaml_parser.parse_config()
    # logger.log(message="Config file path: " + file_path, log_level="info", to_file=True, to_terminal=True)
    logger.log(message="Starting Robin Radar Systems Software Uploader", log_level="info", to_file=True, to_terminal=True)
    logger.log(message="Version: " + _version.__version__, log_level="info", to_file=True, to_terminal=True)
    logger.log(message="Username: " + config['robin_email'], log_level="info", to_file=True, to_terminal=True)

    version_checker.check_latest_version()

    radarType = args.type
    version_name = args.number
    upload_file_path = args.path

    if args.check:
        yaml_parser.parse_config()
        logger.log(message="All prerequisites met.", log_level="info", to_file=True, to_terminal=True)
        sys.exit(0)
    elif args.upload:
        if radarType is None or version_name is None or upload_file_path is None:
            print('Please provide all the arguments: --type, --version, --path')
            sys.exit(1)

        # check if the radar type is valid
        validate.validate(radarType, version_name)
        if check_upload_file.check_upload_file(upload_file_path, version_name) is False:
            sys.exit(1)
        
        # create a temp folder and zip the file
        temp_dir = tempfile.mkdtemp()
        zipped_file_path = temp_dir + '/' + version_name + '.zip'

        create_zip.create_zip(upload_file_path + '/' + version_name, temp_dir, version_name)
        push_software.push_software(zipped_file_path, radarType, version_name)
        remove_zip.remove_zip(zipped_file_path)
        sys.exit(0)

    elif args.slack:
        slack_handler.send_slack_entrypoint()
        logger.log(message="Slack message sent successfully.", log_level="info", to_file=True, to_terminal=True)
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(1)

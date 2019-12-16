#!/usr/bin/env python3

""" Download a survey from Qualtrics, as CSV.

Getting your IDs are documented here:
https://api.qualtrics.com/docs/finding-your-qualtrics-ids

And your Qualtrics domain will be every domain before qualtrics.com; something
like:

yourorg
or
yourorg.co1
"""


import argparse
from argparse import RawDescriptionHelpFormatter

from time import sleep
import zipfile
import io

import requests
from requests.exceptions import HTTPError

import logging
log_format = '%(message)s'
logging.basicConfig(format=log_format)
logging.getLogger().setLevel(logging.WARN)  # Stop ipython debug logging bs
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


POLL_INTERVAL_SEC = 0.5


def make_arg_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        'qualtrics_domain',
        help='Qualtrics domain (everything before qualtrics.com)')
    parser.add_argument('api_token', help='API token for your user')
    parser.add_argument('survey_id', help='ID for the survey to download')
    parser.add_argument('-o', '--out-dir',
        help='Directory to save downloaded CSV to',
        default='.')
    parser.add_argument(
        '-v', '--verbose', help='print debugging output', action='store_true')
    return parser


def request_export(base_export_url, headers):
    url = f'{base_export_url}/'
    format_payload = '{"format": "csv"}'
    response = requests.request('POST', url, data=format_payload, headers=headers)
    response_json = response.json()
    logger.debug(response.text)
    return response_json['result']['progressId']


def poll_for_file_id(base_export_url, headers, progress_id):
    url = f'{base_export_url}/{progress_id}'
    response_json = {}
    progress_status = 'inProgress'
    while progress_status == 'inProgress':
        response = requests.request('GET', url, headers=headers)
        response_json = response.json()
        progress_status = response_json['result']['status']
        pct = response_json['result']['percentComplete']
        logger.debug(pct)
        sleep(POLL_INTERVAL_SEC)

    logger.debug(response.text)
    if progress_status == 'failed':
        raise RuntimeError(response.text)
    return response_json['result']['fileId']


def download_file(base_export_url, headers, file_id, out_dir=None):
    url = f'{base_export_url}/{file_id}/file'
    response = requests.request('GET', url, headers=headers)
    zipfile.ZipFile(io.BytesIO(response.content)).extractall(out_dir)
    logger.info("Extracted!")


def main():
    arg_parser = make_arg_parser()
    args = arg_parser.parse_args()
    headers = {
        'content-type': 'application/json',
        'x-api-token': args.api_token
    }
    domain = args.qualtrics_domain
    survey_id = args.survey_id
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    url = f'https://{domain}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses'
    logger.debug(f'Using URL: {url}')

    progress_id = request_export(url, headers)
    file_id = poll_for_file_id(url, headers, progress_id)
    download_file(url, headers, file_id, args.out_dir)


if __name__ == '__main__':
    main()

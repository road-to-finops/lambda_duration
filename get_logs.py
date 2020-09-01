import time
import datetime
import boto3
import json
import logging
# initiate logging
logger = logging.getLogger()


def check_log_group():
    client = boto3.client('logs')

    paginator = client.get_paginator('describe_log_groups')
    response_iterator = paginator.paginate(
    logGroupNamePrefix='string',
    PaginationConfig={
        'MaxItems': 123,
        'PageSize': 123,
        'StartingToken': 'string'
    }
)
import time
import datetime
import boto3
import json
import logging
# initiate logging
logger = logging.getLogger()


def check_log_group(logGroupNamePrefix):
    client = boto3.client('logs')

    response = client.describe_log_groups(
    logGroupNamePrefix=logGroupNamePrefix
    )
    import pdb; pdb.set_trace()

    f = response['logGroups']
    for function in f:
        logGroupName = function['logGroupName']
        if logGroupName == logGroupNamePrefix:
            print(function['arn'])

logGroupNamePrefix = '/aws/lambda/service_dynamo'
check_log_group(logGroupNamePrefix)
import time
import datetime
import boto3
import json
import logging
# initiate logging
logger = logging.getLogger()


def check_log_group(logGroupNamePrefix):
    client = boto3.client('logs')
    try:
        response = client.describe_log_groups(
        logGroupNamePrefix=logGroupNamePrefix
        )

        f = response['logGroups']
        if f != []:
            for function in f:
                logGroupName = function['logGroupName']
                if logGroupName == logGroupNamePrefix:
                    print(function['arn'])
        else:
            print(f"{logGroupNamePrefix} is not a log group")
    except Exception as e:
        print(e)

logGroupNamePrefix = '/aws/lambda/service_dynamo'
check_log_group(logGroupNamePrefix)
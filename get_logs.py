import time
import datetime
import boto3
import json
import logging
# initiate logging
logger = logging.getLogger()


def check_log_group(client, logGroupNamePrefix):
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
                    return function['arn']
        else:
            print(f"{logGroupNamePrefix} is not a log group")
            return None
    except Exception as e:
        print(e)

        
def get_log_stream(client, logGroupNamePrefix):
    response = client.describe_log_streams(
    logGroupName=logGroupNamePrefix,
    orderBy='LastEventTime',
    descending=True
    )
    
    print(response['logStreams'][0]['logStreamName'])

client = boto3.client('logs')
logGroupNamePrefix = '/aws/lambda/service_dynamo'
check = check_log_group(client, logGroupNamePrefix)
if check != None:
    get_log_stream(client, logGroupNamePrefix)
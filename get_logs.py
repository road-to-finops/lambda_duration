import time
from datetime import datetime, timedelta
import boto3
import json
import logging
# initiate logging
log= logging.getLogger()


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
                    log.info(function['arn'])
                    return function['arn']
        else:
            print(f"{logGroupNamePrefix} is not a log group")
            log.error(f"{logGroupNamePrefix} is not a log group")
            return None
    except Exception as e:
        print(e)

        
def get_log_stream(client, logGroupNamePrefix):
    log.info("Getting Log Stream name")
    response = client.describe_log_streams(
    logGroupName=logGroupNamePrefix,
    orderBy='LastEventTime',
    descending=True
    )
    logStreamName = response['logStreams'][0]['logStreamName']
    print(logStreamName)
    return logStreamName


def filter_logs(client, logGroupNamePrefix, logStreamName):
    #log_stream_split = logStreamName.split('/')
    
    response = client.filter_log_events(
    logGroupName=logGroupNamePrefix,
    logStreamNames=[
        logStreamName
    ], 
    filterPattern='REPORT'
    )
    for item in response['events']:
        log.info("finding report with memory info")
        print(item['message'])
    
client = boto3.client('logs')
logGroupNamePrefix = '/aws/lambda/service_dynamo'
check = check_log_group(client, logGroupNamePrefix)
if check != None:
    logStreamName = get_log_stream(client, logGroupNamePrefix)
    filter_logs(client, logGroupNamePrefix, logStreamName)

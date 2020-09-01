import time
from datetime import datetime, timedelta
import boto3
import json
import logging
# initiate logging
log= logging.getLogger()


def check_log_group(client, logGroupNamePrefix):
    #first we check if the log group we have assumed is right from name exists
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
                    log.info(function['arn'])
                    return function['arn']
        else:
            log.error(f"{logGroupNamePrefix} is not a log group")
            return None
    except Exception as e:
        print(e)

        
def get_log_stream(client, logGroupNamePrefix):
    #then we get the most recnet log stream
    log.info("Getting Log Stream name")
    response = client.describe_log_streams(
    logGroupName=logGroupNamePrefix,
    orderBy='LastEventTime',
    descending=True
    )
    try:
        logStreamName = response['logStreams'][0]['logStreamName']
        log.info(logStreamName)
        return logStreamName
    except Exception as e:
        print(e)
        return None


def filter_logs(client, logGroupNamePrefix, logStreamName):
    #Finnally we get the last messege from the logs which has the data of how much memory was used
    response = client.filter_log_events(
    logGroupName=logGroupNamePrefix,
    logStreamNames=[
        logStreamName
    ], 
    filterPattern='REPORT'
    )
    for item in response['events']:
        log.info("finding report with memory info")
        return item['message']
    
def main(name):
    client = boto3.client('logs')
    logGroupNamePrefix = f"/aws/lambda/{name}"
    check = check_log_group(client, logGroupNamePrefix)
    if check != None:
        logStreamName = get_log_stream(client, logGroupNamePrefix)
        if logStreamName!= None:
            log_message = filter_logs(client, logGroupNamePrefix, logStreamName)
            return log_message
        else:
            return None

    else:
        return None

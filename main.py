import time
import datetime
import boto3
import json
import sys
import get_logs
import logging
import os
from datetime import date, timedelta
# initiate logging
logger = logging.getLogger()

def main():
    output=open("LAMBDA_average_usage.txt", "w")
    functions_list = ls_fun_pag()
    
    data_list = []
    
    for name in functions_list:
        metric_data = get_metrics_lambda(name,output)
        
        if metric_data != None: 
            data_list.append(metric_data)
    output.close()

    make_json(data_list)
    s3_upload()

def ls_fun_pag():
    client = boto3.client('lambda')
    function_list = []

    paginator = client.get_paginator('list_functions')
    response_iterator = paginator.paginate()

    for page in response_iterator:
        f = page['Functions']
        for function in f:
            Fdetails = { "FunctionName": function['FunctionName'], 
            "FunctionArn":function['FunctionArn'] }
            function_list.append(Fdetails)
    
    return function_list


def ls_func():
    client = boto3.client('lambda')
    response = client.list_functions()
    return(response)

def get_memory(fName):
    client = boto3.client('lambda')
    response = client.get_function(
         FunctionName=fName)
    MemorySize = response['Configuration']['MemorySize']
    return MemorySize

def make_json(records):
    logger.info("Creating json file")    
    
    try:
        with open(f"lambda.json", "w") as outfile:
            for result in records:
                json.dump(result, outfile)
                outfile.write('\n')
        logger.info('json created')

    except:
        logging.exception("!!!json creation failed!!!")
        raise

def get_metrics_lambda(Function,output):
    fName = Function['FunctionName']
    fArn = Function['FunctionArn']
    MemorySize = get_memory(fName) # Gets memory size data

    log  = get_logs.main(fName) # goes into additional file to get logs

    start_time = datetime.datetime.utcnow() - datetime.timedelta(weeks=2)
    end_time = datetime.datetime.utcnow()
    client = boto3.client('cloudwatch')
    response_invocation = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Invocations',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': fName
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=1209600,
        Statistics=[
        'Minimum','Average','Maximum'
        ],
        Unit='Count'
     )
    for data in response_invocation.get('Datapoints'):
        min = data.get('Minimum')
        av = data.get('Average')
        max = data.get('Maximum')
        #output.write("Function name:" + " " + fName + "\n" + "\n" + "Invocations:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max) + "\n")

    response_duration = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Duration',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': fName
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=1209600,
        Statistics=[
        'Minimum','Average','Maximum'
        ],
        Unit='Milliseconds'
     )
    
    for data in response_duration.get('Datapoints'):
        min = data.get('Minimum')
        av = data.get('Average')
        max = data.get('Maximum')
        
        x = log.split('\t')
        json_data = {"FucntionName": fName, "FucntionArn": fArn, "Minimum": str(min), "Average": str(av), "Maximum": str(max), "MemorySize": str(MemorySize), "Log":log}
        for item in x:
            try:
                key = item.split(':')[0]
                value = item.split(':')[1]
                json_data[key]=value
            except:
                pass
        

        print(json_data)
        return json_data

        #print ("Duration:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max) + "\n" + 'MemorySize:'+ str(MemorySize))
        #output.write("Duration:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max)+ "\n" + 'MemorySize:'+ str(MemorySize))
    #print ("******************************************************************************************************************")
    #output.write("\n******************************************************************************************************************\n")

def s3_upload():
    logger.info("uploading to S3")
    today = date.today()
    year = today.year
    month = today.month
    
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(
        "lambda.json", os.environ["BUCKET_NAME"], f"lambda/year={year}/month={month}/lambda_{year}_{month}.json"
    )
    


if __name__ == '__main__':
    main()
    #export BUCKET_NAME=buisnesspennybucket-455007007237
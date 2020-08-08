import time
import datetime
import boto3

def main():
    output=open("LAMBDA_average_usage.txt", "w")
    ls = ls_func()
    functions_list=[]
    for f_name in ls.get('Functions'):
        functions_list.append(f_name.get('FunctionName'))

    for name in functions_list:
        get_metrics_lambda(name,output)
    output.close()


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


def get_metrics_lambda(fName,output):
    MemorySize = get_memory(fName)
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
        print ("Function name:" + " " + fName + "\n" + "\n" + "Invocations:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max) + "\n")
        output.write("Function name:" + " " + fName + "\n" + "\n" + "Invocations:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max) + "\n")

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
        memory = MemorySize
        print ("Duration:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max) + "\n" + 'MemorySize:'+ str(MemorySize))
        output.write("Duration:" + "\n" + "Minimum:" + str(min) + "\n" + "Average:" + str(av) + "\n" + "Maximum:" + str(max)+ "\n" + 'MemorySize:'+ str(MemorySize))
    print ("******************************************************************************************************************")
    output.write("\n******************************************************************************************************************\n")



if __name__ == '__main__':
    main()

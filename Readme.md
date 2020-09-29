## Lambda functions running for too long with far too much memory


### Description:
Prints list with the minimum, average and maximum number of invocations and duration of each lambda function in the account as well as the memory attached to the lambda.

This exports a easy read txt file as well as a json file which can be read by athena
This then loads to s3 bucket

### Requirments
Access keys setup to account you wish to access lamda data
Python 3
Boto3 
AWS cli

### How to run
```export BUCKET_NAME=<bucketname>```
``` python3 main.py   ```
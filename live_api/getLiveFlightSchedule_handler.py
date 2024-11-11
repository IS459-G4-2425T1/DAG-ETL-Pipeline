import json
import boto3
import urllib3
from constants import AVIATION_EDGE_API_KEY

http = urllib3.PoolManager()

lambda_client = boto3.client('lambda')  # Initialize the Lambda client

def lambda_handler(event, context):
    url = f"https://aviation-edge.com/v2/public/timetable?key={AVIATION_EDGE_API_KEY}"
    response = http.request('GET', url)
    parsed_data = json.loads(response.data.decode('utf-8'))
    data = json.dumps(parsed_data)
    
    
    s3 = boto3.client('s3')
    bucket_name = 'live-flight-schedule-data'
    key = 'live_flight_schedule_data.json'
    
    # Upload data to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data
    )
    
    # Trigger another Lambda function
    lambda_client.invoke(
        FunctionName='invokeScheduleETL', # 'uploadLiveFlightScheduleS3'
        InvocationType='RequestResponse',
    )
    
    return {
        'statusCode': 200,
        'body': "Aviation Edge Data Successfully Retrieved, uploadLiveFlightScheduleS3 lambda triggered",
    }
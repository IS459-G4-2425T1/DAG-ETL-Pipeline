import json
import boto3
import urllib3
import os

http = urllib3.PoolManager()

AVIATION_EDGE_API_KEY = os.getenv(AVIATION_EDGE_API_KEY)

lambda_client = boto3.client('lambda')  # Initialize the Lambda client

def lambda_handler(event, context):
    url = f"https://aviation-edge.com/v2/public/timetable?key={AVIATION_EDGE_API_KEY}"
    response = http.request('GET', url)
    parsed_data = json.loads(response.data.decode('utf-8'))
    
    # Trigger another Lambda function
    lambda_client.invoke(
        FunctionName='uploadLiveFlightScheduleS3',  # Replace with your target Lambda name
        InvocationType='RequestResponse',  # 'Event' for async, 'RequestResponse' for sync
        Payload=json.dumps(parsed_data)  # Send parsed data as payload
    )
    
    return {
        'statusCode': 200,
        'body': "Aviation Edge Data Successfully Retrieved, uploadLiveFlightScheduleS3 lambda triggered",
        # 'body': parsed_data
    }
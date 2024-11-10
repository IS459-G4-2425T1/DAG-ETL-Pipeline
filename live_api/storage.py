import json
import boto3

def lambda_handler(event, context):
    parsed_data = event #data
    
    s3 = boto3.client('s3')
    bucket_name = 'live-flight-schedule-data'  
    key = 'live_flight_schedule_data.json'  # The object key (file name) in S3

    # Convert parsed_data to JSON string format for upload
    data = json.dumps(event)

    # Upload data to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data
    )
    
    
    
    return {
        'statusCode': 200,
        'body': "Data received and processed successfully"
    }

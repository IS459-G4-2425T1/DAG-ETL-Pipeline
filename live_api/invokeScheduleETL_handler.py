import boto3
import json

def lambda_handler(event, context):
    glue_client = boto3.client('glue')

    job_name = 'clean live data'

    try:
        # Start the Glue job without arguments
        response = glue_client.start_job_run(
            JobName=job_name
        )
        
        # Log the response and return the job run ID
        print(f"Glue job started successfully: {response['JobRunId']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Data uploaded to S3 and Glue job started successfully. Job Run ID: {response['JobRunId']}")
        }

    except Exception as e:
        print(f"Error starting Glue job: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error starting Glue job: {str(e)}")
        }
    
    return {
        'statusCode': 200,
        'body': f"Successfully uploaded liveflightdata to S3 Bucket, Glue job started."
    }
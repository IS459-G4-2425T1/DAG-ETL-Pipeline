import requests
import constants
import boto3
import json
import os
AWS_S3_FLIGHT = constants.AWS_S3_FLIGHT.lower()
AVIATION_STACK_API_KEY = constants.AVIATION_STACKS_API_KEY

AWS_S3_FLIGHT = constants.AWS_S3_FLIGHT
AWS_REGION = constants.AWS_REGION
AWS_ACCESS_KEY = constants.AWS_ACCESS_KEY
AWS_SECRET_KEY = constants.AWS_SECRET_KEY

flight_filename = 'flight_schedule.json'

def get_flight_schedule():
    url = f"https://api.aviationstack.com/v1/flights?access_key={AVIATION_STACK_API_KEY}"

    response = requests.get(url)
    with open('flight_schedule.json', 'w') as json_file:
        json.dump(response.json(), json_file)
    return response.json()

def upload_to_s3(flight_filename):
    s3 = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    s3.upload_file(flight_filename, AWS_S3_FLIGHT, flight_filename)

def delete_local_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"The file {filename} does not exist")

def main():
    get_flight_schedule()
    upload_to_s3(flight_filename)
    delete_local_file(flight_filename)

main()
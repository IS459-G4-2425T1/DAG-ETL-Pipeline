import boto3
import json
import joblib
import pandas as pd
from io import BytesIO


# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the S3 bucket and model file
BUCKET_NAME_INPUT= 'live-flight-schedule-data'
MODEL_FILE_KEY = 'models/xgboost_model.pkl'
FEATURE_COLUMNS_FILE_KEY = 'models/feature_columns.pkl'
BUCKET_NAME_MODEL= 'pipeline2-data-storage'

# S3 folder for the input data
INPUT_FOLDER_KEY = 'clean-live-data/'

# Download model once and load it
def load_model_and_columns():
    model_obj = s3_client.get_object(Bucket=BUCKET_NAME_MODEL, Key=MODEL_FILE_KEY)
    model = joblib.load(BytesIO(model_obj['Body'].read()))

    columns_obj = s3_client.get_object(Bucket=BUCKET_NAME_MODEL, Key=FEATURE_COLUMNS_FILE_KEY)
    feature_columns = joblib.load(BytesIO(columns_obj['Body'].read()))

    return model, feature_columns

# Get the latest file from the S3 folder
def get_latest_file_key():
    try:
        # List all objects in the folder
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME_INPUT, Prefix=INPUT_FOLDER_KEY)
        
        # If there are no files, return None
        if 'Contents' not in response:
            raise Exception("No files found in the specified folder.")
        
        # Sort the files based on LastModified to find the latest one
        latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
        
        print("========== Printing the latest file key ========== ")
        print(latest_file['Key'])
        
        return latest_file['Key']
    
    except Exception as e:
        raise Exception(f"Error fetching latest file from S3: {str(e)}")

# Load input data from the latest file
def load_input_data(file_key):
    try:
        s3_object = s3_client.get_object(Bucket=BUCKET_NAME_INPUT, Key=file_key)
        input_data = json.load(s3_object['Body'])  # Load the JSON data from the S3 object
    except Exception as e:
        raise Exception(f"Error loading input data from S3: {str(e)}")
    
    return input_data

# Load model once and cache it
model, feature_columns = load_model_and_columns()

def lambda_handler(event, context):
    # Get the latest input data file key
    try:
        latest_file_key = get_latest_file_key()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error fetching latest input file: {str(e)}'})
        }

    # Load the input data from the latest file
    try:
        input_data = load_input_data(latest_file_key)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error loading input data: {str(e)}'})
        }

    new_data_df = pd.DataFrame(input_data)

    flightnums = new_data_df['flightnum']
    origins = new_data_df['origin']
    dests = new_data_df['dest']
    uniquecarriers = new_data_df['uniquecarrier']
    crsarrivals = new_data_df['crsarrival']

    # input data will have extra fields like flightnum
    new_data_df['deptime'] = new_data_df['deptime'].astype(str).str.zfill(4)
    new_data_df['crsdephour'] = new_data_df['deptime'].str[:2].astype(int)
    new_data_df['crsdepminute'] = new_data_df['deptime'].str[2:].astype(int)
    new_data_df = new_data_df.drop(columns=['deptime', 'flightnum', 'crsarrival'])  # Adjust 'flightnum' column
    new_data_df = pd.get_dummies(new_data_df, columns=['origin', 'dest', 'uniquecarrier'])

    new_data_df = new_data_df.reindex(columns=feature_columns, fill_value=0)

    try:
        predictions = model.predict(new_data_df) 
        result_df = pd.DataFrame({
            'flightnum': flightnums,
            'origin': origins,
            'dests': dests,
            'uniquecarrier':uniquecarriers,
            'crsarrival':crsarrivals,
            'Estimated delay': predictions
        })
        result_json = result_df.to_dict(orient='records')

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error making prediction: {str(e)}'})
        }
    return {
        'statusCode': 200,
        'body': json.dumps(result_json)
    }


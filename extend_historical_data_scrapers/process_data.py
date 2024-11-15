import pandas as pd
import os
import boto3
import logging
import shutil
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()
# Directory containing CSV files
# departure_folder = '/Users/renkee/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/departure_data'
# arrival_folder = '/Users/renkee/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/arrival_data'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

departure_folder="/home/ubuntu/scraper/departure_data"
arrival_folder="/home/ubuntu/scraper/arrival_data"

# Retrieve AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


# Function to read and standardize column names
def read_and_standardize_csv(file_path):
    df = pd.read_csv(file_path, skiprows=7, skipfooter=1, engine='python')
    df.columns = [col.strip().lower() for col in df.columns]  # Convert column names to lowercase
    return df

#upload function
def upload_to_s3(filepath, bucket_name, filename):
    print("Starting to upload file to S3...")
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
    )

    try:
        s3.upload_file(filepath, bucket_name, filename)
        print("Successfully uploaded file to S3")
    except Exception as e:
        logger.error(f"Failed to upload {filename} to S3: {str(e)}")

#delete function
def delete_local_path(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
            print(f"File {path} has been deleted.")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Directory {path} and all its contents have been deleted.")
    else:
        print(f"The path {path} does not exist.")

def main():

    # Read and concatenate CSV files
    departure_df = pd.concat(
        [read_and_standardize_csv(os.path.join(departure_folder, f)) for f in os.listdir(departure_folder) if f.endswith('.csv')],
        ignore_index=True
    )
    print("done reading all departure data")

    arrival_df = pd.concat(
        [read_and_standardize_csv(os.path.join(arrival_folder, f)) for f in os.listdir(arrival_folder) if f.endswith('.csv')],
        ignore_index=True
    )
    print("done reading all arrival data")

    # Remove rows where 'carrier code' is NaN
    departure_df = departure_df[departure_df['carrier code'].notna()]
    arrival_df = arrival_df[arrival_df['carrier code'].notna()]

    # Define the columns to retain in the final DataFrame (all lowercase)
    departure_columns = [
        'carrier code', 'date (mm/dd/yyyy)', 'flight number', 'tail number',
        'destination airport', 'scheduled departure time', 'actual departure time',
        'scheduled elapsed time (minutes)', 'actual elapsed time (minutes)',
        'departure delay (minutes)', 'taxi-out time (minutes)',
        'delay carrier (minutes)', 'delay weather (minutes)',
        'delay national aviation system (minutes)', 'delay security (minutes)',
        'delay late aircraft arrival (minutes)'
    ]

    arrival_columns = [
        'origin airport', 'scheduled arrival time', 'actual arrival time', 'arrival delay (minutes)',
        'taxi-in time (minutes)'
    ]

    # Filter DataFrames to keep only necessary columns
    departure_df = departure_df[departure_columns]
    arrival_df = arrival_df[['carrier code', 'date (mm/dd/yyyy)', 'flight number', 'tail number'] + arrival_columns]

    # Merge DataFrames
    final_df = pd.merge(
        departure_df,
        arrival_df,
        on=['carrier code', 'date (mm/dd/yyyy)', 'flight number', 'tail number'],
        how='inner'
    )

    
    print("Columns before renaming:", final_df.columns)
    # Mapping the current columns to the new column names
    column_mapping = {
        'actual elapsed time (minutes)': 'ActualElapsedTime',
        'arrival delay (minutes)': 'ArrDelay',
        'actual arrival time': 'ArrTime',
        'scheduled arrival time': 'CRSArrTime',
        'scheduled departure time': 'CRSDepTime',
        'scheduled elapsed time (minutes)': 'CRSElapsedTime',
        'delay carrier (minutes)': 'CarrierDelay',
        'departure delay (minutes)': 'DepDelay',
        'actual departure time': 'DepTime',
        'destination airport': 'Dest',
        'flight number': 'FlightNum',
        'delay late aircraft arrival (minutes)': 'LateAircraftDelay',
        'delay national aviation system (minutes)': 'NASDelay',
        'origin airport': 'Origin',
        'delay security (minutes)': 'SecurityDelay',
        'tail number': 'TailNum',
        'taxi-in time (minutes)': 'TaxiIn',
        'taxi-out time (minutes)': 'TaxiOut',
        'carrier code': 'UniqueCarrier',
        'delay weather (minutes)': 'WeatherDelay',
        'date (mm/dd/yyyy)': 'Date'  # Keeping this for new column generation
    }

    # Rename columns in final_df
    final_df = final_df.rename(columns=column_mapping)

    # Generate new columns based on the 'Date' column
    final_df['Date'] = pd.to_datetime(final_df['Date'], format='%m/%d/%Y')  # Ensure the 'Date' column is in datetime format

    # Create the 'Year', 'Month', 'DayofMonth', and 'DayOfWeek' columns
    final_df['Year'] = final_df['Date'].dt.year
    final_df['Month'] = final_df['Date'].dt.month
    final_df['DayofMonth'] = final_df['Date'].dt.day
    final_df['DayOfWeek'] = final_df['Date'].dt.isocalendar().day  # Monday=1, Sunday=7

    # Drop the original 'Date' column if not needed
    final_df = final_df.drop(columns=['Date'])

    # Add the missing columns with NULL values
    final_df['AirTime'] = pd.NA
    final_df['CancellationCode'] = pd.NA
    final_df['Cancelled'] = pd.NA
    final_df['Distance'] = pd.NA
    final_df['Diverted'] = pd.NA


    # Reorder the columns to match the required order
    final_columns = [
        'ActualElapsedTime', 'AirTime', 'ArrDelay', 'ArrTime', 'CRSArrTime',
        'CRSDepTime', 'CRSElapsedTime', 'CancellationCode', 'Cancelled', 'CarrierDelay',
        'DayOfWeek', 'DayofMonth', 'DepDelay', 'DepTime', 'Dest', 'Distance', 'Diverted',
        'FlightNum', 'LateAircraftDelay', 'Month', 'NASDelay', 'Origin', 'SecurityDelay',
        'TailNum', 'TaxiIn', 'TaxiOut', 'UniqueCarrier', 'WeatherDelay', 'Year'
    ]

    final_df = final_df[final_columns]


    time_columns = ['ArrTime', 'CRSArrTime', 'CRSDepTime', 'DepTime']
    
    for col in time_columns:
        if col in final_df.columns:
            # Remove colons and convert to integer
            final_df[col] = final_df[col].astype(str).str.replace(':', '').replace('nan', '')  # Remove ':' and handle NaNs

    # Print the final DataFrame to verify
    print(final_df.head())

    print(final_df.head())
    # Display the number of rows
    print("Number of rows in the departure DataFrame:", departure_df.shape[0])
    print("Number of rows in the arrival DataFrame:", arrival_df.shape[0])
    print("Number of rows in the final combined DataFrame:", final_df.shape[0])

    print("Duplicates in departure DataFrame:", departure_df.duplicated().sum())
    print("Duplicates in arrival DataFrame:", arrival_df.duplicated().sum())

    # Specify the file path and name for the CSV file
    # output_path = '/Users/renkee/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/combined_data.csv'
    # Define the output path with the desired filename format
    # Get current date minus 3 months
    three_months_ago = datetime.now() - relativedelta(months=3)
    current_month_year = three_months_ago.strftime("%m-%Y")
    
    output_path = f'/home/ubuntu/scraper/{current_month_year}-data.csv'

    # Write the DataFrame to a CSV file
    final_df.to_csv(output_path, index=False)
    
    # Upload to S3 with the new filename
    upload_to_s3(output_path, "airline-additional-data", f"{current_month_year}-data.csv")
    
    delete_local_path(departure_folder)
    delete_local_path(arrival_folder)
    delete_local_path(output_path)


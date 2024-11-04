import pandas as pd
import os

# Directory containing CSV files
departure_folder = '/Users/renkee/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/departure_data'
arrival_folder = '/Users/renkee/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/arrival_data'

# Function to read and standardize column names
def read_and_standardize_csv(file_path):
    df = pd.read_csv(file_path, skiprows=7)
    df.columns = [col.strip().lower() for col in df.columns]  # Convert column names to lowercase
    return df

# Read and concatenate CSV files
departure_df = pd.concat(
    [read_and_standardize_csv(os.path.join(departure_folder, f)) for f in os.listdir(departure_folder) if f.endswith('.csv')],
    ignore_index=True
)

arrival_df = pd.concat(
    [read_and_standardize_csv(os.path.join(arrival_folder, f)) for f in os.listdir(arrival_folder) if f.endswith('.csv')],
    ignore_index=True
)

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
    'origin airport', 'scheduled arrival time', 'actual arrival time',
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

# Display the number of rows
print("Number of rows in the departure DataFrame:", departure_df.shape[0])
print("Number of rows in the arrival DataFrame:", arrival_df.shape[0])
print("Number of rows in the final combined DataFrame:", final_df.shape[0])

# # Define the columns to retain in the final DataFrame
# departure_columns = [
#     'Carrier Code', 'Date (MM/DD/YYYY)', 'Flight Number', 'Tail Number',
#     'Destination Airport', 'Scheduled Departure Time', 'Actual Departure Time',
#     'Scheduled Elapsed Time (Minutes)', 'Actual Elapsed Time (Minutes)',
#     'Departure Delay (Minutes)', 'Taxi-Out Time (Minutes)',
#     'Delay Carrier (Minutes)', 'Delay Weather (Minutes)',
#     'Delay National Aviation System (Minutes)', 'Delay Security (Minutes)',
#     'Delay Late Aircraft Arrival (Minutes)'
# ]

# arrival_columns = [
#     'Origin Airport', 'Scheduled Arrival Time', 'Actual Arrival Time',
#     'Taxi-In time (Minutes)'
# ]

# # Filter the DataFrames to keep only necessary columns
# departure_df = departure_df[departure_columns]
# arrival_df = arrival_df[['Carrier Code', 'Date (MM/DD/YYYY)', 'Flight Number', 'Tail Number'] + arrival_columns]

# # Perform the join on the specified keys
# final_df = pd.merge(
#     departure_df,
#     arrival_df,
#     on=['Carrier Code', 'Date (MM/DD/YYYY)', 'Flight Number', 'Tail Number'],
#     how='inner'
# )

# # Display the final DataFrame or save it for further processing
# print(final_df.head())

# # Optional: Save to a CSV file
# final_df.to_csv('combined_flight_data.csv', index=False)

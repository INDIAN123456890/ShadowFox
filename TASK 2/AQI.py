import pandas as pd

# Load the CSV file
file_path = 'C:\ShadowFox\TASK 2\delhiaqi.csv'
delhiaqi_df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
delhiaqi_df['date'] = pd.to_datetime(delhiaqi_df['date'] ,format='%d-%m-%Y %H:%M', dayfirst=True)

# Create separate 'date' and 'time' columns
delhiaqi_df['date_only'] = delhiaqi_df['date'].dt.date
delhiaqi_df['time_only'] = delhiaqi_df['date'].dt.time

# Define the AQI breakpoints for each pollutant according to Indian standards
breakpoints = {
    'pm2_5': [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200), (91, 120, 201, 300), (121, 250, 301, 400), (251, 380, 401, 500)],
    'pm10': [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200), (251, 350, 201, 300), (351, 430, 301, 400), (431, 600, 401, 500)],
    'no2': [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200), (181, 280, 201, 300), (281, 400, 301, 400), (401, 1000, 401, 500)],
    'so2': [(0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200), (381, 800, 201, 300), (801, 1600, 301, 400), (1601, 2100, 401, 500)],
    'o3': [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200), (169, 208, 201, 300), (209, 748, 301, 400), (749, 1000, 401, 500)],
    'co': [(0, 1, 0, 50), (1.1, 2, 51, 100), (2.1, 10, 101, 200), (10.1, 17, 201, 300), (17.1, 34, 301, 400), (34.1, 50, 401, 500)],
    'nh3': [(0, 200, 0, 50), (201, 400, 51, 100), (401, 800, 101, 200), (801, 1200, 201, 300), (1201, 1800, 301, 400), (1801, 2000, 401, 500)],
}

# Function to calculate the sub-index for a given pollutant value and breakpoints
def calculate_sub_index(value, breakpoints):
    for lower, upper, sub_index_lower, sub_index_upper in breakpoints:
        if lower <= value <= upper:
            return sub_index_lower + ((sub_index_upper - sub_index_lower) / (upper - lower)) * (value - lower)
    return None

# Function to calculate the AQI for a row
def calculate_aqi(row):
    sub_indices = [
        calculate_sub_index(row['pm2_5'], breakpoints['pm2_5']),
        calculate_sub_index(row['pm10'], breakpoints['pm10']),
        calculate_sub_index(row['no2'], breakpoints['no2']),
        calculate_sub_index(row['so2'], breakpoints['so2']),
        calculate_sub_index(row['o3'], breakpoints['o3']),
        calculate_sub_index(row['co'], breakpoints['co']),
        calculate_sub_index(row['nh3'], breakpoints['nh3']),
    ]
    
    # Filter out None values
    valid_sub_indices = [index for index in sub_indices if index is not None]
    
    # Return the maximum sub-index as the AQI, if there are valid sub-indices
    return round(max(valid_sub_indices)) if valid_sub_indices else None

# Apply the AQI calculation to each row
delhiaqi_df['AQI'] = delhiaqi_df.apply(calculate_aqi, axis=1)

# Save the updated dataframe to a new CSV file
output_file_path = 'C:\ShadowFox\TASK 2\output.csv'

delhiaqi_df.to_csv(output_file_path, index=False)

# Display the first few rows to confirm the AQI calculation
print(delhiaqi_df.head())

import pandas as pd
import http.client as http_client
from urllib import parse
import json
import time
import os
from random import randint  # Import for generating random integers

# Paths configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input and output file paths
input_file = os.path.join(DATA_DIR, "input_data.xlsx")
output_file_excel = os.path.join(OUTPUT_DIR, "geocoded_data.xlsx")
output_file_csv = os.path.join(OUTPUT_DIR, "geocoded_data.csv")

# Load the input Excel file
df = pd.read_excel(input_file)
df.columns = df.columns.str.strip()

# Add latitude and longitude columns
df['latitude'] = None
df['longitude'] = None

# Total number of rows in the dataframe
total_rows = len(df)

# Generic field names
FIELD_NUMBER = 'number'         # Replace with your column name for address number
FIELD_STREET = 'street'         # Replace with your column name for street name
FIELD_CITY = 'city'             # Replace with your column name for city
FIELD_POSTAL_CODE = 'postal_code'  # Replace with your column name for postal code

# Function to geocode an address using Nominatim
def geocode_address(address):
    connection = http_client.HTTPSConnection('nominatim.openstreetmap.org')
    connection.request(
        'GET',
        '/search?' + parse.urlencode({'q': address, 'format': 'json', 'addressdetails': 1}),
        '',
        {'Accept': 'application/json', 'User-Agent': 'Python'}
    )
    response = connection.getresponse()
    data = json.loads(response.read().decode())
    connection.close()
    return data


# Iterate over each row in the dataframe
for index, row in df.iterrows():
    print(f"Processing row {index + 1}/{total_rows}")

    # List of address combinations (removed complement column)
    address_combinations = [
        f"{row[FIELD_NUMBER]} {row[FIELD_STREET]}, {row[FIELD_CITY]}",
        f"{row[FIELD_NUMBER]} {row[FIELD_CITY]}, {row[FIELD_POSTAL_CODE]}",
        f"{row[FIELD_STREET]}, {row[FIELD_CITY]}",
        f"{row[FIELD_CITY]}, {row[FIELD_POSTAL_CODE]}",
        row[FIELD_CITY]
    ]

    coordinates_found = False
    for address in address_combinations:
        if pd.isna(address):
            continue

        # Try to geocode
        data = geocode_address(address)

        # Wait for a random interval between requests
        time.sleep(randint(1, 3))

        # If coordinates are found, update the dataframe
        if data:
            df.at[index, 'latitude'] = data[0]['lat']
            df.at[index, 'longitude'] = data[0]['lon']
            coordinates_found = True
            break

    if not coordinates_found:
        print(f"No address found for row {index + 1}")

# Save the updated dataframe to both Excel and CSV files
df.to_excel(output_file_excel, index=False)
df.to_csv(output_file_csv, index=False)

print(f"Geocoding completed. Output saved to {output_file_excel} and {output_file_csv}")

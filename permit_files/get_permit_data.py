import requests
import csv

# Specify the ODATA API URL
odata_url = "https://data.sandiegocounty.gov/api/odata/v4/dyzh-7eat"

# Specify the number of rows you want to retrieve (e.g., 10 rows)
top_count = 100

# Define the query parameters with $top
params = {"$top": top_count}

try:
    # Send a GET request to the ODATA API
    response = requests.get(odata_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Define the CSV file name
        csv_file_name = "permit_data.csv"

        # Access and export the retrieved rows to a CSV file
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=data["value"][0].keys())
            csv_writer.writeheader()
            for row in data["value"]:
                csv_writer.writerow(row)

        print(f"Data exported to {csv_file_name} successfully.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

import requests

# Specify the ODATA API URL
odata_url = "https://data.sandiegocounty.gov/api/odata/v4/dyzh-7eat"

# Specify the number of rows you want to retrieve (e.g., 10 rows)
top_count = 5

# Define the query parameters with $top
params = {"$top": top_count}

try:
    # Send a GET request to the ODATA API
    response = requests.get(odata_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Access and display the retrieved rows row by row
        for i, row in enumerate(data["value"], start=1):
            # print(f"Row {i}:")
            for key, value in row.items():
                print(f"{key}: {value}")
            print("\n")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

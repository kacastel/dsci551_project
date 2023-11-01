import requests
import json

base_url = "https://api.artic.edu/api/v1/artworks"
total_artworks = 123203 
# total_artworks = 1000
items_per_request = 100
offset = 0
all_artworks = []

while offset < total_artworks:
    params = {
        "limit": items_per_request,
        "offset": offset
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        artworks_data = response.json()
        all_artworks.extend(artworks_data['data'])
        offset += items_per_request
        print(f"Retrieved {offset} out of {total_artworks} artworks.")
    else:
        print(f"Failed to retrieve data for offset {offset}. Status code: {response.status_code}")
        break

# Save all the artworks to a JSON file
with open("artworks.json", "w") as json_file:
    json.dump(all_artworks, json_file)

print("All artworks retrieved and saved to 'artworks.json'.")

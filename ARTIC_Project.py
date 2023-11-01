import json

# JSON Data from File with specified encoding (e.g., 'utf-8')
with open('Artic_data.json', 'r', encoding='utf-8') as data_file:
    data = json.load(data_file)

def show_columns():
    if data["data"]:
        # Assuming that all entries have the same structure, you can take the columns from the first entry.
        columns = list(data["data"][0].keys())
        return columns
    else:
        return "The database is empty."

def show_db():
    while True:
        try:
            artworks_set = int(input("Enter an integer (0 to N-1): "))  # Assuming N is the number of items in "data"
            if 0 <= artworks_set < len(data["data"]):
                # Access the specified element in the "data" array
                first_data_item = data["data"][artworks_set]

                # Iterate through the keys and values in the selected data item
                for key, value in first_data_item.items():
                    # Print the key and value
                    print(f"{key}: {value}")
                break
            else:
                print("Invalid input. Please enter a valid integer within the range (0 to N-1).")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

while True:
    choice = input("ARTIC db> ")

    if "columns" in choice.lower():
        print(show_columns())
    elif "database" in choice.lower():
        show_db()
    elif "exit" in choice.lower():
        break
    else:
        print("Invalid choice. Please select a valid option.")

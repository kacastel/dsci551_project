import json
import random

# JSON Data from File with specified encoding (e.g., 'utf-8')
with open('artworks_100.json', 'r', encoding='utf-8') as data_file:
    data = json.load(data_file)

def show_columns(entry):
    selected_columns = {
        "id": entry.get("id", ""),
        "title": entry.get("title", ""),
        "main_reference_number": entry.get("main_reference_number", ""),
        "date_start": entry.get("date_start", ""),
        "date_end": entry.get("date_end", ""),
        "date_display": entry.get("date_display", ""),
        "artist_display": entry.get("artist_display", ""),
        "place_of_origin": entry.get("place_of_origin", ""),
        "description": entry.get("description", ""),
        "dimensions": entry.get("dimensions", ""),
        "medium_display": entry.get("medium_display", ""),
        "credit_line": entry.get("credit_line", ""),
        "publication_history": entry.get("publication_history", ""),
        "exhibition_history": entry.get("exhibition_history", ""),
        "provenance_text": entry.get("provenance_text", ""),
        "latitude": entry.get("latitude", ""),
        "longitude": entry.get("longitude", ""),
        "artwork_type_title": entry.get("artwork_type_title", ""),
        "department_title": entry.get("department_title", ""),
        "artist_title": entry.get("artist_title", ""),
        "category_titles": entry.get("category_titles", ""),
        "material_titles": entry.get("material_titles", ""),
        "image_id": entry.get("image_id", "")
    }
    return selected_columns

def delete_information():
    artwork_id = int(input("Enter Artwork's ID: "))
    deleted = False  # To track whether any entry has been deleted
    for entry in data["data"]:
        if entry["id"] == artwork_id:
            print(entry)
            check_deletion = input("Delete this element of the database? Y/N: ")
            if check_deletion.lower() == "y":
                data["data"].remove(entry)  # Remove the entire entry
                deleted = True
                print(f"Information for {artwork_id} deleted successfully.")

    if not deleted:
        return f"No information found for {artwork_id}."

    # Save the updated data back to the file
    with open("artworks_100.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)

def generate_id():
    # Generate a random integer ID between 10000 and 9999999
    return random.randint(10000, 999999)

def add_new_entry():
    new_entry = {}
    new_entry["id"] = generate_id()
    new_entry["title"] = input("Title: ")
    new_entry["main_reference_number"] = input("Main Reference Number: ")
    new_entry["date_start"] = input("Start Date: ")
    new_entry["date_end"] = input("End Date: ")
    new_entry["date_display"] = input("Date Display: ")
    new_entry["artist_display"] = input("Artist Display: ")
    new_entry["place_of_origin"] = input("Place of Origin: ")
    new_entry["description"] = input("Description: ")
    new_entry["dimensions"] = input("Dimensions: ")
    new_entry["medium_display"] = input("Medium Display: ")
    new_entry["credit_line"] = input("Credit Line: ")
    new_entry["publication_history"] = input("Publication History: ")
    new_entry["exhibition_history"] = input("Exhibition History: ")
    new_entry["provenance_text"] = input("Provenance Text: ")
    new_entry["latitude"] = input("Latitude: ")
    new_entry["longitude"] = input("Longitude: ")
    new_entry["artwork_type_title"] = input("Artwork Type Title: ")
    new_entry["department_title"] = input("Department Title: ")
    new_entry["artist_title"] = input("Artist Title: ")
    new_entry["category_titles"] = input("Category Titles: ")
    new_entry["material_titles"] = input("Material Titles: ")
    new_entry["image_id"] = input("Image ID: ")

    data["data"].append(new_entry)

    # Save the updated data back to the file
    with open("artworks_100.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)

def modify_information():
    artwork_id = int(input("Enter Artwork's ID: "))
    for entry in data["data"]:
        if entry["id"] == artwork_id:
            print(show_columns(entry))  # Pass the entry to show_columns
            while True:
                attribute = input("Enter the attribute from above to modify (or 'done' to exit): ")
                if attribute == 'done':
                    break
                if attribute in entry:
                    new_value = input(f"Enter new value for {attribute}: ")
                    entry[attribute] = new_value
                    print(f"{attribute} for {artwork_id} updated successfully.")
                else:
                    print(f"Invalid attribute: {attribute}")
            print(f"Information for {artwork_id} updated successfully.")
            # Save the updated data back to the file
            with open("artworks_100.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=2)
            return  # Exit the function after saving
    return f"No information found for {artwork_id}"


def apply_custom_filter(data, command):
    filtered_entries = []
    
    # Split the command into tokens
    tokens = command.split()

    if len(tokens) < 5:
        return "Invalid command syntax. Example: 'deliver the id, title, and description of artworks with a date_start and date_end within 1985'"

    # Extract the requested columns
    if 'the' in tokens:
        col_start = tokens.index('the') + 1
        col_end = tokens.index('of')
        columns = tokens[col_start:col_end]
    else:
        return "Invalid command syntax. Missing 'the' keyword."

    # Extract the filter criteria
    if 'with' in tokens:
        filter_start = tokens.index('with') + 1
        filter_criteria = " ".join(tokens[filter_start:])
    else:
        return "Invalid command syntax. Missing 'with' keyword."

    for entry in data["data"]:
        # Add code here to implement filters based on the criteria

        # Example filter: Check if date_start and date_end are within the specified year (1985)
        if "date_start" in entry and "date_end" in entry:
            date_start = str(entry["date_start"])  # Convert to string
            date_end = str(entry["date_end"])  # Convert to string
            if date_start.isdigit() and date_end.isdigit():
                date_start = int(date_start)
                date_end = int(date_end)
                if 1985 >= date_start and 1985 <= date_end:
                    filtered_entries.append(entry)

        # # Example filter: Check if date_start and date_end are within the specified year (1985)
        # if "date_start" in entry and "date_end" in entry:
        #     date_start = entry["date_start"]
        #     date_end = entry["date_end"]
        #     if date_start.isdigit() and date_end.isdigit():
        #         date_start = int(date_start)
        #         date_end = int(date_end)
        #         if 1985 >= date_start and 1985 <= date_end:
        #             filtered_entries.append(entry)

    if filtered_entries:
        result = []
        for entry in filtered_entries:
            result.append({col: entry.get(col, '') for col in columns if col in entry})
        return result
    else:
        return "No matching entries found."

# Example custom command
command = "deliver the id, title, and description of artworks with a date_start and date_end within 1985"

# Apply the custom filter and print the results
filtered_result = apply_custom_filter(data, command)
if isinstance(filtered_result, list):
    for entry in filtered_result:
        print(show_columns(entry))
else:
    print(filtered_result)



while True:
    print("\nOptions:")
    print("1. Add Information")
    print("2. Delete Information")
    print("3. Modify Information")
    print("4. Show columns")
    print("5. Projection")
    print("6. Exit")

    choice = input("ARTIC db> ").lower()

    if any(keyword in choice for keyword in ["add", "insert", "create"]):
        print(add_new_entry())
    if any(keyword in choice for keyword in ["delete", "remove", "erase"]):
        print(delete_information())
    if any(keyword in choice for keyword in ["modify", "change", "alter", "edit"]):
        print(modify_information())
    if any(keyword in choice for keyword in ["columns", "show", "display"]):
        if data["data"]:
            entry_id = int(input("Enter the ID of the artwork to display: "))
            entry = next((entry for entry in data["data"] if entry["id"] == entry_id), None)
            if entry:
                print(show_columns(entry))
            else:
                print(f"No information found for Artwork ID {entry_id}.")
        else:
            print("The database is empty.")
    if any(keyword in choice for keyword in ["project", "filter", "projection"]):
        command = input("Enter the filter command: ")
        filtered_result = apply_custom_filter(data, command)
        if isinstance(filtered_result, list):
            for entry in filtered_result:
                print(show_columns(entry))
        else:
            print(filtered_result)
    elif "exit" in choice:
        break
    else:
        print("Invalid choice. Please select a valid option.")
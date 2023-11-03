import json
import random

# JSON Data from File with specified encoding (e.g., 'utf-8')
with open('artworks_100.json', 'r', encoding='utf-8') as data_file:
    data = json.load(data_file)
    

def show_columns():
    if data["data"]:
        first_entry = data["data"][int(input("Enter an index value: "))]
        selected_columns = {
            "id": first_entry.get("id", ""),
            "title": first_entry.get("title", ""),
            "main_reference_number": first_entry.get("main_reference_number", ""),
            "date_start": first_entry.get("date_start", ""),
            "date_end": first_entry.get("date_end", ""),
            "date_display": first_entry.get("date_display", ""),
            "artist_display": first_entry.get("artist_display", ""),
            "place_of_origin": first_entry.get("place_of_origin", ""),
            "description": first_entry.get("description", ""),
            "dimensions": first_entry.get("dimensions", ""),
            "medium_display": first_entry.get("medium_display", ""),
            "credit_line": first_entry.get("credit_line", ""),
            "publication_history": first_entry.get("publication_history", ""),
            "exhibition_history": first_entry.get("exhibition_history", ""),
            "provenance_text": first_entry.get("provenance_text", ""),
            "latitude": first_entry.get("latitude", ""),
            "longitude": first_entry.get("longitude", ""),
            "artwork_type_title": first_entry.get("artwork_type_title", ""),
            "department_title": first_entry.get("department_title", ""),
            "artist_title": first_entry.get("artist_title", ""),
            "category_titles": first_entry.get("category_titles", ""),
            "material_titles": first_entry.get("material_titles", ""),
            "image_id": first_entry.get("image_id", "")
        }
        return selected_columns
    else:
        return "The database is empty."


def delete_information():
    artwork_id = int(input("Enter Artwork's ID: "))
    deleted = False  # To track whether any entry has been deleted
    for entry in data["data"]:  # Use a copy of the list for safe removal
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
    # return str(random.randint(10000, 999999))
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

# def modify_information():
#     artwork_id = int(input("Enter Artwork's ID: "))
#     for entry in data["data"]:
#         if entry["id"] == artwork_id:
#             print(show_columns(artwork_id))
#             attribute = input("Enter the attribute from above to modify: ")
#             if attribute in entry:
#                 new_value = input(f"Enter new value for {attribute}: ")
#                 entry[attribute] = new_value
#                 return f"Information for {artwork_id} updated successfully."
#             else:
#                 return f"Invalid attribute: {attribute}"
#     return f"No information found for {artwork_id}."

def modify_information():
    artwork_id = int(input("Enter Artwork's ID: "))
    print(artwork_id)
    for entry in data["data"]:
        if entry["id"] == artwork_id:
            while True:
                # print(show_columns(artwork_id))
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
    return f"No information found for {artwork_id}."


while True:

    print("\nOptions:")
    print("1. Add Information")
    print("2. Delete Information")
    print("3. Modify Information")
    print("4. Show columns")
    print("6. Exit")

    choice = input("ARTIC db> ").lower()  # Convert the input to lowercase for case-insensitive matching

    if any(keyword in choice for keyword in ["add", "insert", "create"]):
        print(add_new_entry())
    if any(keyword in choice for keyword in ["delete", "remove", "erase"]):
        print(delete_information())
    if any(keyword in choice for keyword in ["modify", "change", "alter", "edit"]):
        print(modify_information())
    if any(keyword in choice for keyword in ["columns", "show", "display"]):
        print(show_columns())
    elif "exit" in choice:
        break
    else:
        print("Invalid choice. Please select a valid option.")


# # Save the updated data to a file
# with open("artworks_100.json", "w") as json_file:
#     json.dump(data, json_file, indent=2)

# print("Goodbye!")
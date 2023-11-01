import json

# #JSON Data from File
with open('data.json', 'r') as data_file:
    data = json.load(data_file)


# Define functions for various actions
def add_information():
    new_entry = {}
    new_entry["First_Name"] = input("Enter First Name: ")
    new_entry["Last_Name"] = input("Enter Last Name: ")
    new_entry["Age"] = int(input("Enter Age: "))
    new_entry["City"] = input("Enter City: ")
    new_entry["Occupation"] = input("Enter Occupation: ")
    data["data"].append(new_entry)
    return "Information added successfully."

def delete_information():
    first_name = input("Enter First Name to delete: ")
    last_name = input("Enter Last Name to delete: ")
    for entry in data["data"]:
        if entry["First_Name"] == first_name and entry["Last_Name"] == last_name:
            data["data"].remove(entry)
            return f"Information for {first_name} {last_name} deleted successfully."
    return f"No information found for {first_name} {last_name}."

def modify_information():
    first_name = input("Enter First Name to modify: ")
    last_name = input("Enter Last Name to modify: ")
    for entry in data["data"]:
        if entry["First_Name"] == first_name and entry["Last_Name"] == last_name:
            attribute = input("Enter the attribute to modify (First_Name, Last_Name, Age, City, Occupation): ")
            if attribute in entry:
                new_value = input(f"Enter new value for {attribute}: ")
                entry[attribute] = new_value
                return f"Information for {first_name} {last_name} updated successfully."
            else:
                return f"Invalid attribute: {attribute}"
    return f"No information found for {first_name} {last_name}."

# def filter_information():
#     filter_criteria = input("Enter City name or age range (e.g., 'New York' or '25 to 30'): ")
#     filtered_data = []
#     if "to" in filter_criteria:
#         age_range = filter_criteria.split("to")
#         try:
#             age_start = int(age_range[0].strip())
#             age_end = int(age_range[1].strip())
#             for entry in data["data"]:
#                 if age_start <= entry["Age"] <= age_end:
#                     filtered_data.append(entry)
#         except ValueError:
#             return "Invalid age range format."
#     else:
#         city_name = filter_criteria.strip()
#         for entry in data["data"]:
#             if entry["City"] == city_name:
#                 filtered_data.append(entry)

#     if filtered_data:
#         return json.dumps(filtered_data, indent=2)
#     else:
#         return "No matching records found."

def show_db():
    print(data)

# Function to show the list of columns
def show_columns():
    if data["data"]:
        # Assuming that all entries have the same structure, you can take the columns from the first entry.
        columns = list(data["data"][0].keys())
        return columns
    else:
        return "The database is empty."
    
# Function to subset data
def subset_data():
    subset_choice = input("Do you want to subset your data? (Y/N): ")
    if subset_choice.lower() == "y":
        # Prompt the user to specify columns
        columns_to_subset = input("Enter the columns to subset (comma-separated, e.g., First_Name, Age): ").strip().split(",")
        columns_to_subset = [col.strip() for col in columns_to_subset]

        # Prompt the user to specify conditions for city and age
        city_condition = input("Enter the city condition (e.g., 'New York' or 'Los Angeles'): ").strip()
        age_condition = input("Enter the age condition (e.g., '25 to 30'): ").strip()

        # Filter data based on conditions
        filtered_data = []
        for entry in data["data"]:
            if entry["City"] == city_condition and age_condition:
                age_range = age_condition.split("to")
                age_start = int(age_range[0].strip())
                age_end = int(age_range[1].strip())
                if age_start <= entry["Age"] <= age_end:
                    filtered_data.append({col: entry[col] for col in columns_to_subset if col in entry})

        if filtered_data:
            return json.dumps(filtered_data, indent=2)
        else:
            return "No matching records found."
    elif subset_choice.lower() == "n":
        return "Subset operation canceled."
    else:
        return "Invalid choice. Please enter 'Y' for yes or 'N' for no."

# Main loop
while True:
    choice = input("What would you like to do? ")

    # Check for keywords in the user input
    if "add" in choice.lower():
        print(add_information())
    elif "delete" in choice.lower():
        print(delete_information())
    elif "modify" in choice.lower():
        print(modify_information())
    # elif "filter" in choice.lower():
    #     print(filter_information())
    elif "database" in choice.lower():
        print(show_db())
    elif "columns" in choice.lower():
        print(show_columns())
    elif "subset" in choice.lower():
        print(subset_data())
    elif "exit" in choice.lower():
        break
    else:
        print("Invalid choice. Please select a valid option.")

# Save the updated data to a file (optional)
with open("updated_data.json", "w") as json_file:
    json.dump(data, json_file, indent=2)

print("Goodbye!")

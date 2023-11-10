import csv
import random
import string

# Load CSV Data
data = []
csv_file_path = 'permit_data.csv'

def load_data():
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

def save_data():
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = desired_columns
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

desired_columns = [
    # Include columns needed for Query 1
    "id", "record_id", "open_date", "issued_date", "record_status", 
    "record_group", "record_type", "record_subtype", "record_category", 
    "primary_scope_code", "use", "homeowner_biz_owner", "street_address", 
    "city", "state", "zip_code", "full_address", "parcel_number", 
    "valuation", "floor_area", "contractor_name", "contractor_address", 
    "contractor_phone", "created_online", "last_updated", "geocoded_column"
]

def show_columns(entry):
    selected_columns = {}
    for column in desired_columns:
        selected_columns[column] = entry.get(column, "")
    return selected_columns

def generate_random_id():
    while True:
        new_id = ''.join(random.choice(string.digits) for _ in range(random.randint(3, 6)))
        if not any(entry["id"] == new_id for entry in data):
            return new_id

def add_data():
    new_id = generate_random_id()
    new_entry = {"id": new_id}
    for field in desired_columns:
        if field != "id":
            user_input = input(f"Enter data for '{field}' (Press Enter to leave it empty): ")
            if user_input:
                new_entry[field] = user_input
            else:
                new_entry[field] = None
    data.append(new_entry)
    save_data()
    print(f"New data with ID {new_id} added successfully.")

def delete_information():
    permit_id = input("Enter Permit ID: ")
    deleted_entry = None

    for entry in data:
        if entry["id"] == permit_id:
            print("Permit Information to Delete:")
            columns_and_values = show_columns(entry)
            for key, value in columns_and_values.items():
                print(f"{key}: {value}")

            check_deletion = input("Delete this entry from the database? (Y/N): ")
            if check_deletion.lower() == "y":
                deleted_entry = entry
                data.remove(entry)
                print(f"Permit information for {permit_id} deleted successfully.")
                break

    if deleted_entry:
        save_data()
    else:
        print(f"No information found for Permit ID {permit_id}.")

def modify_information():
    permit_id = input("Enter Permit ID: ")
    modified_entry = None

    for entry in data:
        if entry["id"] == permit_id:
            print("Permit Information to Modify:")
            columns_and_values = show_columns(entry)
            for key, value in columns_and_values.items():
                print(f"{key}: {value}")

            while True:
                attribute = input("Enter the attribute from above to modify (or 'done' to exit): ")
                if attribute == 'done':
                    break
                if attribute in entry:
                    new_value = input(f"Enter new value for {attribute}: ")
                    entry[attribute] = new_value
                    print(f"{attribute} for Permit ID {permit_id} updated successfully.")
                else:
                    print(f"Invalid attribute: {attribute}")

            modified_entry = entry
            save_data()
            print(f"Permit information for {permit_id} updated successfully.")
            break

    if not modified_entry:
        print(f"No information found for Permit ID {permit_id}.")


def query_csv(file_path, query):
    # Load CSV data into a list of dictionaries
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Parse the SQL-like query
    select_index = query.find("select")
    from_index = query.find("from")
    where_index = query.find("where")

    # Extract selected columns
    selected_columns = [col.strip() for col in query[select_index + 6:from_index].split(',')]

    # Extract table name
    table_name = query[from_index + 4:where_index].strip()

    # Extract WHERE clause
    where_clause = query[where_index + 5:].strip()

    # Apply filters based on WHERE clause
    filtered_data = data
    if where_clause:
        # Split conditions based on 'and'
        conditions = where_clause.split('and')
        for condition in conditions:
            condition = condition.strip()
            filter_conditions = condition.split('=')
            column_to_filter = filter_conditions[0].strip()
            filter_value = filter_conditions[1].strip().replace("'", "")

            # Apply the filter for each condition
            filtered_data = [row for row in filtered_data if row.get(column_to_filter) == filter_value]

    # Prepare and print the projection
    for row in filtered_data:
        projection = {col: row[col] for col in selected_columns}
        print(projection)

load_data()

while True:
    print("\nOptions:")
    print("1. Show columns")
    print("2. Add data")
    print("3. Modify data")
    print("4. Delete data")
    print("5. Query CSV data")  # Option for Query 1
    print("6. Exit")

    choice = input("Permits db> ").lower()

    if any(keyword in choice for keyword in ["columns", "show", "display"]):
        if data:
            entry_id = input("Enter the ID of the data to display: ")
            entry = next((entry for entry in data if entry["id"] == entry_id), None)
            if entry:
                columns_and_values = show_columns(entry)
                for key, value in columns_and_values.items():
                    print(f"{key}: {value}")
            else:
                print(f"No information found for ID {entry_id}.")
        else:
            print("The database is empty.")

    elif "add" in choice:
        add_data()

    elif "modify" in choice:
        modify_information()

    elif "delete" in choice:
        delete_information()

    # elif "query" in choice or "select" in choice:
    elif "query" in choice:

        # Option for Query 1
        user_query = input("Enter the SQL-like query: ")
        query_csv(csv_file_path, user_query)

    elif "exit" in choice:
        break

    else:
        print("Invalid choice. Please select a valid option.")
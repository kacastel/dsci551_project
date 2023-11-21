
import csv
import random
import string
import re
import numpy as np

# Load CSV Data
data = []
csv_file_path = 'Building_Permits.csv'
# csv_file_path = 'Building_Permits.csv'


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


# Function to evaluate the WHERE condition
def evaluate_condition(row, condition):
    operators = ['>', '<', '>=', '<=', '=', '!=']
    for operator in operators:
        if operator in condition:
            column, value = condition.split(operator)
            column = column.strip()
            value = value.strip()

            if operator == '=':
                operator = '=='

            if '*' in value:
                # If the value contains "*", perform wildcard matching
                value_pattern = value.replace('*', '.*')
                if re.match(value_pattern, row.get(column)) is not None:
                    return True
            else:
                # Perform standard comparison with conversion for "valuation" column
                if column in row:
                    if column == "valuation":
                        try:
                            row_value = float(row[column])
                            value = float(value)
                            if eval(f'{row_value} {operator} {value}'):
                                return True
                        except ValueError:
                            # Handle the case where the "valuation" column cannot be converted to a numeric type
                            pass
                    else:
                        if eval(f'"{row[column]}" {operator} "{value}"'):
                            return True
    return False

# Function to group data by a column
def group_by_column(data, column_name, aggregate_function):
    grouped_data = {}
    for row in data:
        key = row.get(column_name)
        if key not in grouped_data:
            grouped_data[key] = []

        # Convert the valuation to a numeric value, or use None if conversion fails
        valuation = row.get('valuation')
        try:
            valuation = float(valuation) if valuation else None
        except ValueError:
            valuation = None

        grouped_data[key].append(valuation)

    grouped_results = []
    for key, values in grouped_data.items():
        # Filter out None values for aggregation
        filtered_values = [v for v in values if v is not None]

        if aggregate_function:
            if aggregate_function == 'max':
                result = max(filtered_values) if filtered_values else None
            elif aggregate_function == 'min':
                result = min(filtered_values) if filtered_values else None
            elif aggregate_function == 'avg':
                result = np.mean(filtered_values) if filtered_values else None
            elif aggregate_function == 'sum':
                result = sum(filtered_values) if filtered_values else None
            elif aggregate_function == 'count':
                result = len(filtered_values)
        else:
            result = filtered_values

        grouped_results.append({column_name: key, aggregate_function.capitalize() if aggregate_function else "Data": result})
    print(grouped_results)
    return grouped_results

def join_or_display_data(permit_data_file, medical_cases_file):
    joined_data = []
    permit_data_chunk = []
    chunk_count = 0

    with open(permit_data_file, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            permit_data_chunk.append(row)
            chunk_count += 1

            if chunk_count == 1000:
                medical_cases = {}
                with open(medical_cases_file, 'r', encoding='utf-8') as medical_file:  # Specify UTF-8 encoding
                    csv_reader = csv.DictReader(medical_file)
                    for case_row in csv_reader:
                        for permit_row in permit_data_chunk:
                            if permit_row['city'] == case_row['death_city']:
                                joined_row = {**permit_row, **case_row}
                                joined_data.append(joined_row)
                permit_data_chunk = []
                chunk_count = 0

    # Process any remaining data in the last chunk
    if permit_data_chunk:
        medical_cases = {}
        with open(medical_cases_file, 'r', encoding='utf-8') as medical_file:  # Specify UTF-8 encoding
            csv_reader = csv.DictReader(medical_file)
            for case_row in csv_reader:
                for permit_row in permit_data_chunk:
                    if permit_row['city'] == case_row['death_city']:
                        joined_row = {**permit_row, **case_row}
                        joined_data.append(joined_row)

    return joined_data



def query_permit_data(data, user_input, group_by=None, aggregate_function=None, sort_order=None):
    
    # Split the user input into query components
    query_components = re.split(r'\s+', user_input)
    select_clause = query_components[1:query_components.index('from')]
    where_index = query_components.index('where') if 'where' in query_components else None

    # Filter the dataset based on the WHERE clause if present
    filtered_data = data
    if where_index is not None:
        where_clause = ' '.join(query_components[where_index + 1:])
        filtered_data = [row for row in data if evaluate_condition(row, where_clause)]

    # Extract the SELECTed columns from the filtered data
    selected_data = []
    for row in filtered_data:
        row_data = {}
        for column in select_clause:
            row_data[column] = row[column]
        selected_data.append(row_data)

    if group_by is not None:
        # Grouping and aggregating data if group_by is specified
        grouped_results = group_by_column(selected_data, group_by, aggregate_function)
    else:
        # If no grouping, return the selected data directly
        grouped_results = selected_data

    # Sorting the results if sort_order is specified
    if sort_order and aggregate_function:
        try:
            grouped_results.sort(key=lambda x: (x[aggregate_function.capitalize()] is None, x[aggregate_function.capitalize()]), reverse=(sort_order.lower() == 'desc'))
        except KeyError:
            print("Invalid sort_order or aggregate_function")

    return grouped_results


# Load initial data
load_data()

# Main loop
while True:
    print("\nOptions:")
    print("1. Show columns")
    print("2. Add data")
    print("3. Modify data")
    print("4. Delete data")
    print("5. Query data")  # Option for Query 1
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

    elif "query" in choice:
        joined_data = join_or_display_data("Building_Permits.csv", "city_deaths.csv")  # Create joined_data
        if not joined_data:
            print("No data to query. Please join the datasets first.")
        else:
            user_query = input("Enter the SQL-like query: ")
            group_by_column_name = input("Enter column to group by (or leave blank for none): ")
            aggregate_function = input("Enter aggregate function (max, min, avg, sum, count, or leave blank for none): ")
            sort_order = input("Enter sort order (asc, desc, or leave blank for none): ")

            group_by_column_name = None if not group_by_column_name else group_by_column_name
            aggregate_function = None if not aggregate_function else aggregate_function
            sort_order = None if not sort_order else sort_order

            # results = query_permit_data(joined_data, user_query, group_by=group_by_column_name, aggregate_function=aggregate_function, sort_order=sort_order)
            results = query_permit_data(joined_data, user_query, group_by=group_by_column_name, aggregate_function=aggregate_function, sort_order=sort_order)

            for result in results:
                for column, value in result.items():
                    print(f'{column}: {value}')
                print('-' * 20)

    elif "exit" in choice:
        break

    else:
        print("Invalid choice. Please select a valid option.")
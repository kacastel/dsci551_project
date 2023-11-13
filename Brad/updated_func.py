import json
import sys
import numpy as np

with open('data.json', 'r') as data_file:
    data = json.load(data_file)

with open('columns.json', 'r') as data_file:
    item_col_names = json.load(data_file)

with open('columns_types.json', 'r') as data_file:
    item_col_types = json.load(data_file)

#basic functions (include acknowledgment of process success)
#------------------------------------------------------------------------------------------
def create_item(name, columns, types):
    if name not in data:
        data[name] = []
        item_col_names[name] = columns

        item_col_types[name] = {}
        for i in range(len(columns)):
            item_col_types[name][columns[i]] = types[i]

        with open("columns.json", "w") as file:
            json.dump(item_col_names, file, indent = 2)

        with open("columns_types.json", "w") as file:
            json.dump(item_col_types, file, indent = 2)

        with open("data.json", "w") as file:
            json.dump(data, file, indent = 2)
        print('Item ' + name + ' created')
    else:
        print('Item ' +  name + ' already exists')
        
def delete_item(name):
    if name in data:
        del data[name]
        del item_col_names[name]
        del item_col_types[name]

        with open("columns.json", "w") as file:
            json.dump(item_col_names, file, indent = 2)

        with open("columns_types.json", "w") as file:
            json.dump(item_col_types, file, indent = 2)

        with open("data.json", "w") as file:
            json.dump(data, file, indent = 2)
        print('Item ' + name + ' removed')
    else:
        print("Item " + name + ' does not exist')

# inserting data
def add_info(name): #empty string for null values
     if name in item_col_names:
        columns = item_col_names[name]
        value_dict = {}
        for col in columns:
            col_value = input('Value for ' + col + ': ')   

            if item_col_types[name][col] == 'str':
                value_dict[col] = col_value

            elif item_col_types[name][col] == 'int':
                if col_value == '': #no value
                    value_dict[col] = ''
                else:
                    value_dict[col] = int(col_value)
            else: #float
                if col_value == '': #no value
                    value_dict[col] = ''
                else:
                    value_dict[col] = float(col_value)
                
        data[name].append(value_dict)
        with open("data.json", "w") as file:
            json.dump(data, file, indent = 2)
        print('Information added to ' + name)
     else:
        print('Item ' + name + ' does not exist')

#deleting data
def delete_info(name):
    if name in item_col_names:
        columns = input('Using which columns? ').split(', ')
        filters = {}
        for col in columns:
            filter = input('Criteria for ' + col + ': ')
            if item_col_types[name][col] == 'str':
                filters[col] = filter
            elif item_col_types[name][col] == 'int':
                if filter == '': #no value
                    filters[col] = ''
                else:
                    filters[col] = int(filter)
            else: #float
                if filter == '': #no value
                    filters[col] = ''
                else:
                    filters[col] = float(filter)

        global data
        new_data = data.copy()
        del new_data[name]
        new_data[name] = []

        info = data[name]
        for i in range(len(info)):
            change = 1
            for filter in filters:
                if info[i][filter] != filters[filter]:
                    change = 0
                    break
            if change == 0:
                new_data[name].append(info[i])

        data = new_data
        with open("data.json", "w") as file:
                json.dump(new_data, file, indent = 2)
        print('Information deleted in ' + name)
    else:
        print('Item ' + name + ' does not exist')
    
#modifying data
def modify_info(name):
    if name in item_col_names:
        update_col = input('Which column to update? ')
        original_val = input('Original value for ' + update_col + ': ')
        new_val = input('New value for ' + update_col + ': ')

        if original_val != '':
            if item_col_types[name][update_col] == 'int':
                original_val = int(original_val)
          
            if item_col_types[name][update_col] == 'float':
                original_val = float(original_val)

        if new_val != '':
            if item_col_types[name][update_col] == 'int':
                new_val = int(new_val)
          
            if item_col_types[name][update_col] == 'float':
                new_val = float(new_val)

        for entry in data[name]:
            if entry[update_col] == original_val:
                entry[update_col] = new_val #modify
    
        with open("data.json", "w") as file:
            json.dump(data, file, indent = 2)
        print('Information modified in ' + name)
    else:
        print('Item ' + name + ' does not exist')

#----------------------------------------------------------------------------------------
# Query functions
# Sequential Steps: join, filter, group, aggregate, order, project
def query_pipeline(name):
    if name not in item_col_names:
        print('Item ' + name + ' does not exist')
        return
    
    #join
    #-------------------------------------------------------------------------------------------
    df = data[name].copy() # so data doesn't change, resolves reference issues
    join = input('Join? ') #inner join only
    col_types = item_col_types[name].copy()
    if join == 'Y':
        other_item = input('Select item to join with ' + name + ': ')
        if other_item not in item_col_names:
            print('Item ' + other_item + ' does not exist')
            return
        col_1 = input('Select column to join on in ' + name + ': ')
        col_2 = input('Select column to join on in ' + other_item + ': ')
        
        for key in item_col_types[other_item]:
            col_types[key] = item_col_types[other_item][key]

        joined = []
        for entry_1 in df:
            new_entry = {}
        #entry = [{}, {}, {}]
            for entry_2 in data[other_item]:
                if entry_1[col_1] == entry_2[col_2]: #join exists
                    for col in entry_1:
                        new_entry[col] = entry_1[col]
                    for col  in entry_2:
                        new_entry[col] = entry_2[col]
            joined.append(new_entry)

        remove_join = [entry for entry in joined if entry != {}] #only want entries where there is a match
        df = remove_join
    #------------------------------------------------------------------------------------------------------
   
    #filter
    #------------------------------------------------------------------------------------
    filter = input('Filter? ')
    if filter == 'Y':
        columns = input('Which columns to filter? ').split(', ')
        col_val = {}
        for col in columns:
            value = input('Filter value for ' + col + ': ')
            if value != '':
                if col_types[col] == 'str':
                    col_val[col] = value

                elif col_types[col] == 'int':
                    col_val[col] = int(value)
                
                else: #float
                    col_val[col] = float(value)
            else:
                col_val[col] = value
        
        returned = []
        for entry in df:
            check = 1
            for col in col_val:
                if entry[col] != col_val[col]:
                    check = 0
                    break
            if check == 1:
                returned.append(entry)
        df = returned 
    #-------------------------------------------------------------------------------------

    #group/aggregate
    #------------------------------------------------------------------------------------ 
    group = input('Group? ')
    if group == 'Y':
        group_col = input('Which columns to group? ')
        group_col = group_col.split(', ')
        #group on multiple columns
        col_aggregate = input('Which column to aggregate? ')
        agg_func = input('Which aggregate function? ')

        if col_types[col_aggregate] == 'str' and agg_func != 'count':
            print('Error: Aggregation ' + agg_func + ' cannot be performed on string type')
            return

        group_data = {}
        for entry in df:
            unique_group = () #separate data by groups
            for col in group_col:
                unique_group += (entry[col], )

            if '' in unique_group: #exclude null group values
                continue

            if unique_group not in group_data:
                if entry[col_aggregate] != '': #exclude null values in aggregation
                    group_data[unique_group] = [entry[col_aggregate]]
            else:
                if entry[col_aggregate] != '': #exclude null values in aggregation
                    group_data[unique_group].append(entry[col_aggregate])

        final_agg = {}
        if agg_func == 'count':
            for unique_group in group_data:
                final_agg[unique_group] = len(group_data[unique_group])
        elif agg_func == 'sum':
            for unique_group in group_data:
                final_agg[unique_group] = sum(group_data[unique_group])
        elif agg_func == 'max': 
            for unique_group in group_data:
                final_agg[unique_group] = max(group_data[unique_group])
        elif agg_func == 'min':
            for unique_group in group_data:
                final_agg[unique_group] = min(group_data[unique_group])
        else: #agg_func = 'avg'
            for unique_group in group_data:
                final_agg[unique_group] = sum(group_data[unique_group]) / len(group_data[unique_group])

        df = final_agg

        #order
        order = input('Order? ')
        if order == 'Y':
            form = input('Ascending or Descending? ')
            if form == 'Ascending':
                df = dict(sorted(final_agg.items(), key = lambda x: x[1], reverse = False))
            else:
                df = dict(sorted(final_agg.items(), key = lambda x: x[1], reverse = True))
        

    #project (select columns)
    if group == 'N':
        selected_col = input('Select columns: ').split(', ')
        if len(selected_col) == 1 and 'all' in selected_col:
            print(df)
            return
        
        selected_data = []
        for entry in df:
            returned_entry = {}
            for col in selected_col:
                returned_entry[col] = entry[col]
            selected_data.append(returned_entry)
        
        df = selected_data
    
    print(df)

    #columns = input('Columns: ')
    #if columns == 'all':
    
    #else:

# Main loop
while True:
    choice = input("db> ")
    if 'make' in choice and 'item' in choice: #make item students
        item_name = choice.split(' ')[2]
        col = input("Columns: ") #id, name, program
        col_names = col.split(', ')
        types = input('Types: ')
        col_types = types.split(', ')
        create_item(item_name, col_names, col_types)

    elif 'remove' in choice and 'item' in choice: #remove item students
        item_name = choice.split(' ')[2]
        delete_item(item_name)

    elif 'add' in choice: #add to students
        item_name = choice.split(' ')[2]
        add_info(item_name)

    elif 'delete' in choice: #delete in students
        item_name = choice.split(' ')[2]
        delete_info(item_name)
        
    elif 'change' in choice: #change in students
        item_name = choice.split(' ')[2]
        modify_info(item_name)

    elif 'query' in choice: #query in students
        item_name = choice.split(' ')[2]
        query_pipeline(item_name)

    elif "exit" in choice:
        break

    else:
       print("Invalid command")
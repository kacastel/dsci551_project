import json
import sys
import numpy as np
import os

with open('attribute_types.json', 'r') as data_file:
    col_types = json.load(data_file)

#basic functions (include acknowledgment of process success)
#------------------------------------------------------------------------------------------
def create_item(name, columns, types):
    open(name + '.json', 'w') #create file to store updated data

    col_types[name] = {}
    for i in range(len(columns)):
        col_types[name][columns[i]] = types[i]

    with open("attribute_types.json", "w") as file:
        json.dump(col_types, file, indent = 2)

    print('Item ' + name + ' created')
        
def delete_item(name):
    del col_types[name]
    with open("attribute_types.json", "w") as file:
        json.dump(col_types, file, indent = 2)
    
    os.remove(name + '.json')
    print('Item ' + name + ' removed')

# inserting data
def add_info(name): #empty string for null values
    columns = list(col_types[name].keys())
    value_dict = {}
    for col in columns:
        col_value = input('Value for ' + col + ': ')   

        if col_types[name][col] == 'str':
            value_dict[col] = col_value

        elif col_types[name][col] == 'int':
            if col_value == '': #no value
                value_dict[col] = ''
            else:
                value_dict[col] = int(col_value)
        else: #float
            if col_value == '': #no value
                value_dict[col] = ''
            else:
                value_dict[col] = float(col_value)
                
    with open(name + '.json', "a") as f:
        json.dump(value_dict, f)
        f.write('\n')
    print('Information added to ' + name)

#deleting data
def delete_info(name):
    columns = input('Using which columns? ').split(', ')
    filters = {}
    for col in columns:
        filter = input('Value for ' + col + ': ') #equal to only
        if col_types[name][col] == 'str':
            filters[col] = filter
        elif col_types[name][col] == 'int':
            if filter == '': #no value
                filters[col] = ''
            else:
                filters[col] = int(filter)
        else: #float
            if filter == '': #no value
                filters[col] = ''
            else:
                filters[col] = float(filter)

    open('new_' + name + '.json', 'w') #create file to store updated data

    with open(name + '.json', 'r') as f:
        for line in f: #chunking line by line
            entry = json.loads(line)
            change = 1
            for filter in list(filters.keys()): #loops through columns
                if entry[filter] != filters[filter]:
                    change = 0
                    break

            if change == 0:
                with open('new_' + name + '.json', "a") as file:
                    json.dump(entry, file)
                    file.write('\n')

    os.remove(name + '.json')
    os.rename('new_' + name + '.json', name + '.json')
    print('Information deleted in ' + name)
    
#modifying data
def modify_info(name):
    update_col = input('Which column to update? ')
    original_val = input('Original value for ' + update_col + ': ')
    new_val = input('New value for ' + update_col + ': ')

    if original_val != '':
        if col_types[name][update_col] == 'int':
            original_val = int(original_val)
          
        if col_types[name][update_col] == 'float':
            original_val = float(original_val)

    if new_val != '':
        if col_types[name][update_col] == 'int':
            new_val = int(new_val)
          
        if col_types[name][update_col] == 'float':
            new_val = float(new_val)

    open('new_' + name + '.json', 'w') #create file to store updated data
    with open(name + '.json', 'r') as f:
        for line in f: #chunking line by line
            entry = json.loads(line)
            if entry[update_col] == original_val:
                entry[update_col] = new_val #modify
            with open('new_' + name + '.json', "a") as file:
                json.dump(entry, file)
                file.write('\n')

    os.remove(name + '.json')
    os.rename('new_' + name + '.json', name + '.json')
    print('Information modified in ' + name)

#----------------------------------------------------------------------------------------
# Query functions
# Sequential Steps: join, filter, group, aggregate, order, project
def query_pipeline(name):
    #join
    #-------------------------------------------------------------------------------------------
    with open(name + '.json', 'r') as f:
        for line in f: #chunking line by line
            entry = json.loads(line)
            with open('saved.json', "a") as file: #create copy to perform further additional operations
                json.dump(entry, file)
                file.write('\n')

    join = input('Join? ') #inner join only
    if join == 'Y':
        other_item = input('Select item to join with ' + name + ': ')
        col_1 = input('Select attribute to join on in ' + name + ': ')
        col_2 = input('Select attribute to join on in ' + other_item + ': ')
  
        with open('saved.json', 'r') as f:
            for line_1 in f: #chunking line by line
                entry_1 = json.loads(line_1)
                with open(other_item + '.json', "r") as file: 
                    for line_2 in file: #chunking line by line
                        joined_entry = {}
                        entry_2 = json.loads(line_2)
                        if entry_1[col_1] == entry_2[col_2]: #join exists
                            for col in entry_1:
                                joined_entry[col] = entry_1[col]
                            for col in entry_2:
                                joined_entry[col] = entry_2[col]
                            
                        with open('new.json', 'a') as file:
                            if joined_entry != {}:
                                json.dump(joined_entry, file)
                                file.write('\n')
        
        #update results
        os.remove('saved.json')
        os.rename('new.json', 'saved.json')
    #------------------------------------------------------------------------------------------------------
   
    #filter
    #------------------------------------------------------------------------------------
    filter = input('Filter? ')
    if filter == 'Y':
        columns = input('Which attributes to filter? ').split(', ')
        col_val = {}
        col_operator = {}
        for col in columns:
            operator = input('Comparison Operator for ' + col + ': ')
            value = input('Filter value for ' + col + ': ')
            col_operator[col] = operator

            if value != '':
                if col_types[name][col] == 'str':
                    col_val[col] = value

                elif col_types[name][col] == 'int':
                    col_val[col] = int(value)
                
                else: #float
                    col_val[col] = float(value)
            else:
                col_val[col] = value

        with open('saved.json', 'r') as f:
            for line in f: #chunking line by line 
                entry = json.loads(line)
                check = 1
                for col in col_val:
                    if col_operator[col] == 'gt':
                        try:
                            if entry[col] > col_val[col]:
                                continue
                            else: 
                                check  = 0
                                break
                        except: #for null values
                            check = 0
                            break

                    elif col_operator[col] == 'lt':
                        try:
                            if entry[col] < col_val[col]:
                                continue
                            else: 
                                check  = 0
                                break
                        except:
                            check = 0
                            break

                    elif col_operator[col] == 'gte':
                        try:
                            if entry[col] >= col_val[col]:
                                continue
                            else: 
                                check  = 0
                                break
                        except:
                            check = 0
                            break

                    elif col_operator[col] == 'lte':
                        try:
                            if entry[col] <= col_val[col]:
                                continue
                            else: 
                                check  = 0
                                break
                        except:
                            check = 0
                            break

                    elif col_operator[col] == 'ne':
                        if entry[col] != col_val[col]:
                            continue
                        else: 
                            check  = 0
                            break

                    else: #col_operator is 'eq'
                        if entry[col] == col_val[col]:
                            continue
                        else: 
                            check  = 0
                            break

                if check == 1:
                    with open('new.json', 'a') as file:
                        json.dump(entry, file)
                        file.write('\n')
        
        #update results
        os.remove('saved.json')
        os.rename('new.json', 'saved.json')

    #-------------------------------------------------------------------------------------

    #group/aggregate
    #------------------------------------------------------------------------------------ 
    group = input('Group? ')
    if group == 'Y':
        group_col = input('Which attributes to group? ')
        group_col = group_col.split(', ')
        #group on multiple columns
        col_aggregate = input('Which attribute to aggregate? ')
        item_name = input('Which item contains the aggregate attribute ' + col_aggregate + '? ')
        agg_func = input('Which aggregate function? ')

        if col_types[item_name][col_aggregate] == 'str' and agg_func not in ['count', 'min', 'max']:
            print('Error: Aggregation ' + agg_func + ' cannot be performed on string type')
            return

        with open('saved.json', 'r') as f:
            group_data = {}
            for line in f: #chunking line by line
                entry = json.loads(line)
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

        #order
        order = input('Order? ')
        if order == 'Y':
            form = input('Ascending or Descending? ')
            if form == 'Ascending':
                ordered = dict(sorted(final_agg.items(), key = lambda x: x[1], reverse = False))
            else:
                ordered = dict(sorted(final_agg.items(), key = lambda x: x[1], reverse = True))

            with open('new.json', 'a') as file:
                group_vals = ordered.items()
                for pair in group_vals:
                    json.dump(pair, file)
                    file.write('\n')

        else: #no order needed
            with open('new.json', 'a') as file:
                group_vals = final_agg.items()
                for pair in group_vals:
                    json.dump(pair, file)
                    file.write('\n')

        #update results
        os.remove('saved.json')
        os.rename('new.json', 'saved.json')

    #project (select columns)
    if group == 'N':
        selected_col = input('Select attributes: ').split(', ')
        if len(selected_col) == 1 and 'all' in selected_col: #select all the columns
            with open('saved.json', 'r') as f:
                for line in f: #chunking line by line 
                    entry = json.loads(line)
                    print(entry)
            os.remove('saved.json') #remove file used to update results
            return
        
        with open('saved.json', 'r') as f:
            for line in f: #chunking line by line 
                entry = json.loads(line)
                new_entry = {}
                for col in selected_col:
                    new_entry[col] = entry[col]
                print(new_entry)
        os.remove('saved.json') #remove file used to update results
    
    else:
        with open('saved.json', 'r') as f:
            for line in f: #chunking line by line 
                entry = json.loads(line)
                print(entry)
        os.remove('saved.json') #remove file used to update results

# Main loop
while True:
    choice = input("db> ")
    if 'make' in choice and 'item' in choice: #make item students
        item_name = choice.split(' ')[2]
        col = input("Attributes: ") #ex. id, name, program
        names = col.split(', ')
        types = input('Types: ')
        types = types.split(', ')
        create_item(item_name, names, types)

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
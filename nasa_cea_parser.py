### Libraries
import pandas as pd
import sys
import argparse

def get_word_list_and_start_index(cea_out_file):
    try:
        with open(cea_out_file, 'r') as f:
            # Read the entire content into a single string variable
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        file_content = ""

    ### Remove the spaces
    word_list = file_content.split()

    # print(word_list)

    ### Look for amount of keywords

    count = 0
    target_sequence = ["MOLE", "FRACTIONS", "CH4"]
    target_len = len(target_sequence)
    start_indexes = []

    # Iterate through the list up to the point where the sequence can still fit
    for i in range(len(word_list) - target_len + 1):
        # Check if the slice of the list matches the target sequence
        if word_list[i:i + target_len] == target_sequence:
            count += 1
            start_indexes.append(i)

    return word_list, start_indexes, count
        
# print(f"Found {count} instances of 'MOLE FRACTION CH4'.")
# print(f"They start at indexes: {start_indexes}.")
# print(word_list[731])

# Assuming 'word_list' is the variable holding all words

### Function to extract the table data
def extract_data_block(word_list, start_index):
    """
    Extracts a list of words starting from start_index until '*' is found.
    """
    data_block = []
    
    # Iterate through the list starting from the specified index
    for word in word_list[start_index:]:
        # Stop condition
        if word == '*':
            break
        
        # Add the word to the data block
        data_block.append(word)
        
    return data_block

### Adjust for real start indexes
def get_table_list(word_list, start_indexes, count):
    real_start_indexes = []
    for i in start_indexes:
        real_start_indexes.append(i + 2)

    # print(extract_data_block(word_list, real_start_indexes[0]))

    ### Go through every counted instance and extract the table, creating a list of tables

    table_list = []

    for i in range(count):
        table_list.append(extract_data_block(word_list, real_start_indexes[i]))

    return table_list

### Split each table into a row for each component
## Could do this by searching for "words" that don't start with a 0,
## There will never be a 1, so all non-zeros will be the components

def split_to_rows(table_list):
    """
    Splits a flat list of component names and mole fractions into a list of lists (rows).
    """
    table_rows = []
    current_row = []
    
    for item in table_list:
        # Check if the item is a species name (i.e., NOT a number starting with '0')
        # We also ensure the item isn't an empty string just in case.
        if item and not item.startswith('0'):
            # This is a new component name, so the previous row is complete.
            if current_row:
                table_rows.append(current_row)
            
            # Start a new row with the component name
            current_row = [item]
        
        # If the item starts with '0', it's a composition value.
        elif item:
            # Add the composition value to the current row
            current_row.append(item)
            
    # Append the last row after the loop finishes
    if current_row:
        table_rows.append(current_row)
        
    return table_rows

# print(split_to_rows(table_list[0]))

### Use function to split all tables into rows of each component
def get_aggregated_mole_fractions_dict(table_list, count):
    compositions = []

    for i in range(count):
        compositions.append(split_to_rows(table_list[i]))

    # print(compositions)
    # print(compositions[0])
    # print(compositions[0][0])

    ### Now we aggregate each component into a dictionary where the component is the key
    ### and the value is a list of the compositions in order

    aggregated_mole_fractions = {}

    for table in range(len(compositions)):
        for row in range(len(compositions[table])):
            # print(compositions[table][row])
            component_name = compositions[table][row][0]
            mole_fractions = compositions[table][row][1:]
            
            try:
            # Check if the component is already a key in the dictionary
                if component_name not in aggregated_mole_fractions:
                    # If not, initialize the key with the current list of fractions
                    aggregated_mole_fractions[component_name] = []
                    
                # Extend the existing list with the new fractions
                # The extend method adds all elements from 'mole_fractions' to the end of the list,
                # maintaining the correct order across all instances.
                aggregated_mole_fractions[component_name].extend(mole_fractions)
            except TypeError:
                aggregated_mole_fractions[component_name] = []


    # print(aggregated_mole_fractions)
    # print(len(aggregated_mole_fractions["CH4"]))

    return aggregated_mole_fractions

def main():
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(
        description="Parses NASA-CEA output text to create a clean CSV/Excel file of MOLE FRACTIONS."
    )
    
    # Input File Path (The CEA output)
    parser.add_argument(
        "input_file",
        help="Path to the input NASA-CEA output file (e.g., cea_results.txt)."
    )
    
    # Output File Name/Path (The exported spreadsheet)
    parser.add_argument(
        "output_file",
        help="Desired name for the output file (e.g., combustion_data)."
    )
    
    # File Extension (The format choice)
    parser.add_argument(
        "-e", "--extension",
        choices=['csv', 'xlsx'],
        default='xlsx',
        help="The desired output file format. Choices: 'csv' or 'xlsx'. Default is 'xlsx'."
    )
    
    # Parse the arguments provided by the user
    args = parser.parse_args()
    
    # --- Integration Point: Use the Arguments ---
    
    cea_out_file = args.input_file
    output_base_name = args.output_file
    file_ext = args.extension
    
    print(f"Reading data from: {cea_out_file}")
    print(f"Exporting to: {output_base_name}.{file_ext}")

    try:
        # Run functions in order
        (word_list, start_indexes, count) = get_word_list_and_start_index(cea_out_file)
        table_list = get_table_list(word_list, start_indexes, count)
        aggregated_mole_fractions = get_aggregated_mole_fractions_dict(table_list, count)

        # Create a DataFrame where columns are the species
        df = pd.DataFrame(aggregated_mole_fractions)

        # This makes the species the index and the mole fractions the columns.
        df = df.transpose()
        
        # Optional: Rename the columns if you know how many you have (e.g., 4 instances)
        num_columns = len(df.columns)
        df.index.name = 'Species'

        # Export the DataFrame to the specified file type
        output_path = f'{output_base_name}.{file_ext}'

        if file_ext == 'csv':
            # CSV export (most compatible)
            df.to_csv(output_path)
            print(f"\nSuccess! Data exported to: {output_path}")

        elif file_ext == 'xlsx':
            # XLSX export (requires the 'openpyxl' or 'xlsxwriter' library installed)
            # Install with: pip install openpyxl
            df.to_excel(output_path, sheet_name='Mole Fractions')
            print(f"\nSuccess! Data exported to: {output_path}")

        # elif file_ext == 'ods':
        #     df.to_excel(output_path, sheet_name='Mole Fractions')
        #     print(f"\nSuccess! Data exported to: {output_path}")
            
        else:
            print(f"\nError: Unsupported file extension '{file_ext}'. Only 'csv' and 'xlsx' are supported.")

    except NameError:
        print("\nError: The dictionary 'aggregated_mole_fractions' was not found. Please ensure it was created correctly.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during export: {e}")

if __name__ == "__main__":
    main()
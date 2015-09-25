'''
Created on 25 sep. 2015

@author: Brian
'''

def load_csv(filepath):
    # Get the list of rows in the file
    content = readfile(filepath)
    
    # Get a dictionary that contains each possible column, with all the data for the data type in this column
    # These are nested dictionaries, where each nested dictionary contains a columnheader with the column name
    # and a data element that contains a list with all the values
    axes_dictionary = parse_csv_file(content)
   
    return axes_dictionary

def readfile(filepath):
    with open(filepath, 'r') as openfile:
        # Read the whole file
        content = openfile.readlines()
        # Clean each line, removing \r and split each line on tabs
        table = cleanrows(content)
        
        return table
    

def cleanrows(content):
    # Go through each line, remove windows line endings + whitespace, and split each line on tabs
    # .strip() does not use the \r that are added in the Windows line-endings
    table = []
    
    # Remove rows that have missing values
    for row in content:
        cleaned_row = row.replace("\r", "").rstrip("\n").split('\t')
        table.append(cleaned_row)
    return table

def parse_csv_file(content):
    # First row is always column headers
    column_headers = content[0]
    
    # Skip column header when we parse the data
    data_rows = content[1:]
    
    # Make dictionary to store column data
    axes_dictionary = {}
    for idx, header in enumerate(column_headers):
        # Create nested dictionary with the columnheader and associated data
        axes_dictionary[idx] = {"columnheader": header,
                                "data": [row[idx] for row in data_rows]}
    
    return axes_dictionary
    
def writefile(filepath, content):
    # Open file and write contents
    with open(filepath, 'w') as writefile:
        writefile.writelines(content)
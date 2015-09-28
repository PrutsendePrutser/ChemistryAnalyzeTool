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
        
def export_plot_data(axes_data):
    print("Enter your path and filename here:")
    fname = input()
    
    table = []
    # Add leading tab to columnheader row for sample column
    headerline = "\t" + "\t".join([axis[1] for axis in axes_data])+"\n"
    
    table.append(headerline)
    # Go through the values
    for idx, val in enumerate(axes_data[0][2]):
        # Add sample number + the value for each column, separated by tabs
        row = str(idx) + "\t" + "\t".join([val, axes_data[1][2][idx], axes_data[2][2][idx]])+"\n"
        table.append(row)
    
    writefile(fname, table)

def export_plot_data_with_original_axis(original_axis, axes_data):
    print("Enter your path and filename here:")
    fname = input()
    
    table = []
    # Add leading tab to columnheader row for the sample column
    headerline = "\t" + "\t".join([axis[1] for axis in axes_data] + [original_axis[1]])+"\n"
    table.append(headerline)
    
    # Go over the values
    for idx, val in enumerate(original_axis[2]):
        # Add sample number + the value for each column, separated by tabs
        row = str(idx) + "\t" + "\t".join([axes_data[0][2][idx], axes_data[1][2][idx], axes_data[2][2][idx], val])+"\n"
        table.append(row)
    
    writefile(fname, table)
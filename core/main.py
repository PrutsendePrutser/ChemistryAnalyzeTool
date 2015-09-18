'''
Created on 6 sep. 2015

@author: Brian
'''
import plot

assigned_axes = []
axes_dictionary = {}

def main():
    while True:
        # Ask for filepath
        filepath = input("Enter the path to the file you want to analyze.")
        # Parse specified file
        try:
            axes_dictionary = load_csv(filepath)
        # If file does not exist, jump back to specifying filepath again
        except IOError:
            print("File not found, please enter the correct path to your file, using forward slashes instead of backslashes.")
            continue
        
        # Prompt user to choose the plot type
        print("""Choose the number of the plot type you want to use:
                1. 3D surface plot
                2. 3D scatter plot""")
        plottype = int(input())
        
        # Let the user choose a data type for the x-, y- and z-axis
        assigned_axes = assign_axes(axes_dictionary)
        
        # Make the plot
        handle_plot_choice(plottype, assigned_axes)
        
        # Make sure we exit after plotting
        break

def load_csv(filepath):
    # Get the list of rows in the file
    content = readfile(filepath)
    
    # Get a dictionary that contains each possible column, with all the data for the data type in this column
    # These are nested dictionaries, where each nested dictionary contains a columnheader with the column name
    # and a data element that contains a list with all the values
    axes_dictionary = parse_csv_file(content)
    return axes_dictionary

def parse_csv_file(content):
    # First row is always column headers
    headers = content[0]
    
    # Skip column header when we parse the data
    data_rows = content[1:]
    
    # Make dictionary to store column data
    axes_dictionary = {}
    
    for idx, header in enumerate(headers):
        # Create nested dictionary with the columnheader and associated data
        axes_dictionary[idx] = {"columnheader": header,
                                "data": [row[idx] for row in data_rows[1:]]}
    
    return axes_dictionary

def readfile(filepath):
    with open(filepath, 'r') as openfile:
        # Read the whole file
        content = openfile.readlines()
        # Clean each line, removing \r and split each line on tabs
        cleaned_content = cleanrows(content)
        return cleaned_content

def cleanrows(content):
    # Go through each line, remove windows line endings + whitespace, and split each line on tabs
    # .strip() does not use the \r that are added in the Windows line-endings
    table = [row.replace("\r", "").strip().split('\t') for row in content]
    
    cleaned_content = []
    # Remove rows that have missing values
    for idx, row in enumerate(table):
        # Check if row contains any empty elements
        for v in row:
            if not v.strip():
                print("Row number %d contains at least one empty value and is removed from the dataset" % idx + 2)
                break
        # If there are no empty elements we get into the else, add the row to the cleaned_content
        else:
            cleaned_content.append(row)
            
    
def writefile(filepath, content):
    with open(filepath, 'w') as writefile:
        writefile.writelines(content)
        
def handle_plot_choice(plottype, assigned_axes):
    if plottype == 1:
        plot.create_3d_surface_plot(assigned_axes)
    elif plottype == 2:
        plot.create_3d_scatter_plot(assigned_axes)

def handle_axis_assignment(columnheader, axis_letter, axes_dictionary):
    # Go over the dictionary values
    for axis in axes_dictionary.values():
        # If the user wants to assign the axis with this header name
        if axis["columnheader"] == columnheader:
            # Return a tuple with the axis-letter, the header name and the data
            return(axis_letter, columnheader, axis["data"])
    # Return None in case we don't find anything
    return None
    
def assign_axis(axis_titles, axes_dictionary, axis_number):
    # if it's a bytes object already, we only need to decode
    if type(axis_number) is bytes:
        axis_letter = axis_number.decode('utf-8')
    # In case something goes wrong and it's an int value, we need to cast to
    # bytes before decoding
    else:
        axis_letter = bytes(axis_number).decode('utf-8')
    print("Assign column to %s - axis:" % axis_letter)
    # Show axis titles with choice number
    for idx, axis in enumerate(axis_titles):
        choice_number = str(idx + 1)
        print("{}. {}".format(choice_number, axis))
    # Get input
    choice = int(input())
    # Get columnheader
    columnheader = axis_titles[choice - 1]
    return handle_axis_assignment(columnheader, axis_letter, axes_dictionary)
    

def assign_axes(axes_dictionary):
    # Start with x-axis and increment from there on
    starting_axis = b'x'
    # Get the titles for display
    axis_titles = [axis["columnheader"] for axis in axes_dictionary.values()]
    print("Please assign your data columns to an axis")
    print("")
    # CHeck which axes we assigned already
    assigned_axis_letters = []
    
    # We work with 3D-plots atm, therefore we use 3 axes
    for i in range(3):
        # Assign data to the current axis if the axis does not already have data assigned
        if starting_axis not in assigned_axis_letters: 
            assigned_axis = assign_axis(axis_titles, axes_dictionary, starting_axis)
        # If we assigned something
        if assigned_axis is not None:
            # Add to the assigned list
            assigned_axes.append(assigned_axis)
            # Remove from the title list, so it doesn't get displayed anymore, no point in
            # using the same axis more than once in a plot            
            axis_titles.remove(assigned_axis[1])
        # Update assigned axis letters
        assigned_axis_letters = [axis[0] for axis in assigned_axes]
        
        # Increment the starting_axis by 1, making it go from x -> y, or y -> z
        starting_axis = bytes([starting_axis[0] + 1])
    
    return assigned_axes

main()
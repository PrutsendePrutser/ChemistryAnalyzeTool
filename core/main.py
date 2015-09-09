'''
Created on 6 sep. 2015

@author: Brian
'''
import plot
import struct

assigned_axes = []
axes_dictionary = {}

def main():
    while True:
        # Ask for filepath
        filepath = input("Enter the path to the file you want to parse, using forward slashes instead of backslashes.")
        # Parse specified file
        try:
            axes_dictionary = load_csv(filepath)
            print(axes_dictionary)
        # If file does not exist, jump back to specifying filepath again
        except IOError:
            print("File not found, please enter the correct path to your file, using forward slashes instead of backslashes.")
            continue
        print("""Choose the number of the plot type you want to use:
                1. 2D-plot
                2. 3D-plot
                3. 3D-plot with rotatable axes""")
        # Prompt user to choose the plot type
        plottype = int(input())
        
        assigned_axes = assign_axes(axes_dictionary)
        
        handle_plot_choice(plottype, assigned_axes)
        break
        #handle_plot_choice(plottype, axes_dictionary)
        

def load_csv(filepath):
    content = readfile(filepath)
    axes_dictionary = parse_csv_file(content)
    return axes_dictionary

def parse_csv_file(content):
    headers = content[0]
    data_rows = content[1:]
    axes_dictionary = {}
    for idx, header in enumerate(headers):
        axes_dictionary[idx] = {"columnheader": header,
                                "data": [row[idx] for row in data_rows]}
    
    return axes_dictionary

def readfile(filepath):
    with open(filepath, 'r') as openfile:
        content = openfile.readlines()
        cleaned_content = cleanrows(content)
        return cleaned_content

def cleanrows(content):
    return [row.replace("\r", "").strip().split('\t') for row in content]
    
def writefile(filepath, content):
    with open(filepath, 'w') as writefile:
        writefile.writelines(content)
        
def handle_plot_choice(plottype, assigned_axes):
    for axis in assigned_axes:
        print(len(axis[2]))
    plot.create_3d_plot(assigned_axes)

def handle_axis_assignment(columnheader, axis_letter, axes_dictionary):
    for axis in axes_dictionary.values():
        print(axis)
        if axis["columnheader"] == columnheader:
            return(axis_letter, columnheader, axis["data"])
    return None
    
def assign_axis(axis_titles, axes_dictionary, axis_number):
    if type(axis_number) is bytes:
        axis_letter = axis_number.decode('utf-8')
    else:
        axis_letter = bytes(axis_number).decode('utf-8')
    print("Assign column to %s - axis:" % axis_letter)
    for idx, axis in enumerate(axis_titles):
        choice_number = str(idx + 1)
        print("{}. {}".format(choice_number, axis))
    choice = int(input())
    columnheader = axis_titles[choice - 1]
    return handle_axis_assignment(columnheader, axis_letter, axes_dictionary)
    

def assign_axes(axes_dictionary):
    # Start with x-axis and increment from there on
    starting_axis = b'x'
    axis_titles = [axis["columnheader"] for axis in axes_dictionary.values()]
    print("Please assign your data columns to an axis")
    print("")
    assigned_axis_letters = []
    print(type(starting_axis))
    
    for i in range(3):
        if starting_axis not in assigned_axis_letters: 
            assigned_axis = assign_axis(axis_titles, axes_dictionary, starting_axis)
        if assigned_axis is not None:
            assigned_axes.append(assigned_axis)            
            axis_titles.remove(assigned_axis[1])
        assigned_axis_letters = [axis[0] for axis in assigned_axes]
        
        starting_axis = bytes([starting_axis[0] + 1])
    
    return assigned_axes

main()
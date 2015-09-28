'''
Created on 6 sep. 2015

@author: Brian
'''
import core.plot as plot
import utils.formula_parser as formula_parser
import utils.file_utils as fileutils

from copy import deepcopy

assigned_axes = []
axes_dictionary = {}
plottype = 0

def main():
    while True:
        # Ask for filepath
        filepath = input("Enter the path to the file you want to analyze.")
        # Parse specified file
        try:
            axes_dictionary = fileutils.load_csv(filepath)
        # If file does not exist, jump back to specifying filepath again
        except IOError:
            print("File not found, please enter the correct path to your file, using forward slashes instead of backslashes.")
            continue
        
        # Prompt the user to specify a plot type
        plottype = get_plot_type()
        
        # Let the user choose a data type for the x-, y- and z-axis
        assigned_axes = assign_axes(axes_dictionary)
        
        # Make the plot
        handle_plot_choice(plottype, assigned_axes)
        
        export_type = show_export_prompt(transformed = False)
        if export_type == 1:
            fileutils.export_plot_data(assigned_axes)
        else:
            return
        
        # Ask the user if he wants to apply a formula to one of the axes
        transform_prompt(assigned_axes, plottype)
        
        # Make sure we exit after plotting
        break

def get_plot_type():
    # Prompt user to choose the plot type
    print("""Choose the number of the plot type you want to use:
            1. 3D surface plot
            2. 3D scatter plot""")
    plottype = int(input())
    return plottype

def get_formula():
    print ("Enter your formula here:")
    formula = input()
    return formula

def get_axis_to_transform():
    print("For which axis do you want to transform the data?")
    print("Enter -1 to exit the transform prompt.\n")
    for idx, axis in enumerate(assigned_axes):
        print("{}. {}-axis: {}".format(idx+1, axis[0], axis[1]))
    choice = int(input()) - 1
    return choice

def transform_data(formula, choice, assigned_axes):
    # Create a deep copy so we don't change values in the original nested lists that contain the values
    assigned_axes_copy = deepcopy(assigned_axes)
    
    # Collect the elements from the axes that contains the data
    axes_data = [axis[2] for axis in assigned_axes_copy]
    
    # Get a list that contains nested lists with the x, y and z coordinates for each data point
    axes_data_lists = get_axes_data_in_lists(axes_data)
    
    # Update the values for the selected axis, applying the formula
    assigned_axes_copy[choice][2] = transform_values(formula, axes_data_lists)
    
    # Change the column header for the selected column to contain the formula
    assigned_axes_copy[choice][1] = formula
    
def show_export_prompt(transformed = False):
    print("1. Pass")
    print("2. Export plot data to a csv file")
    if (transformed):
        print("3. Export plot data + original axis to a csv file ")
    export_type = int(input())
    
    return export_type

def transform_prompt(assigned_axes, plottype):
    choice = 0
    while choice >= 0:
        
        # Prompt user to choose an axis to apply a formula to
        choice = get_axis_to_transform()
        
        # -1 means exit
        if choice < 0:
            break
        
        # Get the formula
        formula = get_formula()
        
        # Get the transformed data
        transformed_data = transform_data(formula, choice, assigned_axes)
        
        # Plot the new data
        handle_plot_choice(plottype, transformed_data)
        
        # Ask the user for the export type
        export_type = show_export_prompt(transformed = True)
        
        # Export data in plot
        if export_type == 1:
            fileutils.export_plot_data(transformed_data)
        # Export data in plot + the original axis
        elif export_type == 2:
            fileutils.export_plot_data_with_original_axis(assigned_axes[choice], transformed_data)
        else:
            continue
    
def get_axes_data_in_lists(axes_data):
    axes_data_lists = []
    # Go over the data
    for idx, data_point in enumerate(axes_data[0]):
        # Create a list that contains floating point values of the data points
        data_list = list(map(float, (data_point, axes_data[1][idx], axes_data[2][idx])))
        # Add
        axes_data_lists.append(data_list)
    
    return axes_data_lists

def transform_values(formula, axis_data):
    # List 
    transformed_values = []
    
    use_x_axis = False
    use_y_axis = False
    use_z_axis = False
    
    X = 0
    Y = 1
    Z = 2
    
    formula = formula.lower()
    if "x" in formula:
        use_x_axis = True
    if "y" in formula:
        use_y_axis = True
    if "z" in formula:
        use_z_axis = True
    
    xval = None
    yval = None
    zval = None
    
    for data_point in axis_data:
        if use_x_axis:
            xval = data_point[X]
        if use_y_axis:
            yval = data_point[Y]
        if use_z_axis:
            zval = data_point[Z]
        transformed_values.append(str(formula_parser.transform(formula, xval, yval, zval)))
    return transformed_values

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
            # Return a list with the axis-letter, the header name and the data
            return [axis_letter, columnheader, axis["data"]]
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
    for idx, axis in enumerate(axis_titles[1:]):
        choice_number = str(idx + 1)
        print("{}. {}".format(choice_number, axis))
    # Get input
    choice = int(input())
    # Get columnheader
    columnheader = axis_titles[choice]
    
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
        
    xaxis = []
    yaxis = []
    zaxis = []
    
    for idx, v in enumerate(assigned_axes[0][2]):
        if v.strip() and assigned_axes[1][2][idx].strip() and assigned_axes[2][2][idx].strip():
            xaxis.append(v)
            yaxis.append(assigned_axes[1][2][idx])
            zaxis.append(assigned_axes[2][2][idx])
        else:
            print("Row %s is missing values, skipping.." % str(idx+1))
    assigned_axes[0][2] = xaxis
    assigned_axes[1][2] = yaxis
    assigned_axes[2][2] = zaxis
    
    return assigned_axes

main()
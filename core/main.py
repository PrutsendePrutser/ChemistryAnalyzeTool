'''
Created on 6 sep. 2015

@author: Brian
'''

def main():
    while True:
        filepath = input("Enter the path to the file you want to parse, using forward slashes instead of backslashes.")
        try:
            axes_dictionary = load_csv(filepath)
        except IOError:
            print("File not found, please enter the correct path to your file, using forward slashes instead of backslashes.")
            continue
        print("""Choose the number of the plot type you want to use:
                1. 2D-plot
                2. 3D-plot
                3. 3D-plot with rotatable axes""")
        plottype = int(input())
        handle_plot_choice(plottype, axes_dictionary)
        

def load_csv(filepath):
    content = readfile(filepath)
    axes_dictionary = parse_csv_file(content)
    return axes_dictionary

def parse_csv_file(content):
    headers = content[0].split('\t')
    axes_dictionary = {}
    for idx, header in enumerate(headers):
        axes_dictionary[idx] = {"columnheader": header,
                                "data": []}
    for row in content[1:]:
        row_data = row.split(',')
        for idx, val in enumerate(row_data):
            axes_dictionary[idx]["data"].append(val)
    
    return axes_dictionary

def readfile(filepath):
    with open(filepath, 'r') as openfile:
        content = openfile.readlines()
        cleaned_content = cleanrows(content)
        return cleaned_content

def cleanrows(content):
    return [row.replace("\r", "").strip() for row in content]
    
def writefile(filepath, content):
    with open(filepath, 'w') as writefile:
        writefile.writelines(content)
        
def handle_plot_choice(plottype, axes_dictionary):
    pass

def handle_axis_assignment(axis_nr, axis_title):
    pass
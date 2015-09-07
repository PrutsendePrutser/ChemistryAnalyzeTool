'''
Created on 6 sep. 2015

@author: Brian
'''

def main():
    pass

def readfile(filepath):
    with open(filepath, 'r') as openfile:
        return openfile.readlines()
    
def writefile(filepath, content):
    with open(filepath, 'w') as writefile:
        writefile.writelines(content)
        
def handle_plot_choice(plottype):
    pass

def handle_axis_assignment(axis_nr, axis_title):
    pass
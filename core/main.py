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
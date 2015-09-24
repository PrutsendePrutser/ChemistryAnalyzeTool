from math import *

def transform(formula, x=None, y=None, z=None):
    # Apply the current formula using the values that were passed in
    value = eval(formula)
    
    # Return the value
    return value
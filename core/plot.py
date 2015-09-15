'''
Created on 7 sep. 2015

@author: Brian
'''
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plot
import numpy as np

def create_3d_surface_plot(assigned_axes):
    # Plot figure
    figure = plot.figure()
    
    # Axes in the plot
    axes = figure.gca(projection='3d')
    
    # Create numpy arrays with floating point values so we can plot the data
    X = np.array([float(num) for num in assigned_axes[0][2]])
    Y = np.array([float(num) for num in assigned_axes[1][2]])
    Z = np.array([float(num) for num in assigned_axes[2][2]])
    
    # Create tri-surface plot with jet colorscheme
    axes.plot_trisurf(X, Y, Z, cmap=cm.get_cmap('jet'), linewidth=0.2)

    # Set labels
    axes.set_xlabel(assigned_axes[0][1])
    axes.set_ylabel(assigned_axes[1][1])
    axes.set_zlabel(assigned_axes[2][1])

    # Show
    plot.show()
    
def create_3d_scatter_plot(assigned_axes):
    # Create plot figure
    figure = plot.figure()
    
    # Axes in the plot
    axes = figure.add_subplot(111, projection='3d')
    
    # Loop over the datapoints
    for i in range(len(assigned_axes[0][2])):
        x = float(assigned_axes[0][2][i])
        y = float(assigned_axes[1][2][i])
        z = float(assigned_axes[2][2][i])
        
        # Scatter the points in the graph
        axes.scatter(x, y, z, c="r", marker="^")
    
    # Set labels
    axes.set_xlabel(assigned_axes[0][1])
    axes.set_ylabel(assigned_axes[1][1])
    axes.set_zlabel(assigned_axes[2][1])
    
    # Show
    plot.show()

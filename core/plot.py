'''
Created on 7 sep. 2015

@author: Brian
'''
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def createplot(plottype):
    pass

def assign_column_to_axis(axis, column_name):
    pass

def visualize(plot):
    pass

def create_3d_plot(assigned_axes):
    print(len(assigned_axes[0][2]))
    print(len(assigned_axes[1][2]))
    print(len(assigned_axes[2][2]))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.array([float(num) for num in assigned_axes[0][2]])
    Y = np.array([float(num) for num in assigned_axes[1][2]])
    Z = np.array([float(num) for num in assigned_axes[2][2]])
    surf = ax.plot_trisurf(X, Y, Z, cmap=cm.get_cmap('jet'), linewidth=0.2)

    plt.show()

def create_2d_plot(plot):
    pass

def export_to_image(plot):
    pass

def export_to_csv(plot):
    pass

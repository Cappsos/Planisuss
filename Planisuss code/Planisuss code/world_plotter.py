
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

from settings import *

# global variables
animation_array = np.zeros((NUMCELLS, NUMCELLS,3), dtype=int)


def initialize_plot():
    """initialize the plot"""
    fig, ax = plt.subplots(num='Planisuss')
    

    return fig, ax
    
def build_animation_array(world):
    # iterate through world array and build a numpy rgb array that contains the correct color for each cell
    for y in range(NUMCELLS):
        for x in range(NUMCELLS):
            animation_array[y][x] = world[y][x].get_color()
    return animation_array


def plot_the_world(day, world, ax):
    """plot the world"""
    
    ax.clear()
    
    animation_array = build_animation_array(world)

    ax.imshow(animation_array, interpolation='nearest')
    ax.set_title(f"Day: {day}")

    
    
    

    
    
    
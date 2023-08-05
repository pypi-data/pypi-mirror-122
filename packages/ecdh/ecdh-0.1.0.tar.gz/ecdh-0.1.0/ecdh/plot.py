import os
import sys
from datetime import date
from math import ceil, sqrt

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D

import numpy as np


"""
# Plot class specifications:
percentage = <bool>     // Only used when qc-plot = True and changes scale from specific capacity to percent of first cycle
qcplot = <bool>         // Displays capacity over cycle life plot
vqplot = <bool>         // Displays voltage versus capacity for all cycles
suptitle = <string>     // Changes the top title to whatever you put it to
ylabel = <string>       // Changes y-scale label on the vq plots
xlabel = <string>       // Changes x-scale label on the vq plots
numfiles = <int>        // Amount of files which is passed in the file list
"""

class Plot:
    def __init__(self, numfiles = 1, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.taken_subplots = 0
        #print(self.percentage)
        
        # Finding number of subplots
        if self.qcplot is True:
            self.subplots = 1
        else:
            self.subplots = 0
        if self.all_in_one is True:
            self.subplots+= 1
        else:
            if self.vqplot is True:
                self.subplots += numfiles
            
            if self.dqdvplot is True:
                self.subplots += numfiles


        
        # List of available colors
        self.colors =  ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan' ]

        # Initiate figure and axes
        if self.subplots > 2: # Then two columns, or more.
            rows = int(sqrt(self.subplots))
            cols = ceil(self.subplots/rows)
            self.fig, self.axes = plt.subplots(nrows = rows, ncols = cols)
            self.axes = self.axes.reshape(-1)
        else:
            self.fig, self.axes = plt.subplots(nrows = self.subplots)
        self.fig.suptitle(str(date.today()))
        try:
            iter(self.axes)
        except:
            self.axes = [self.axes]
        for ax in self.axes:
            #ax.figure.set_size_inches(8.4, 4.8, forward = True)
            ax.set(
            title = 'Generic subplot title',
            ylabel = 'Potential [V]',
            xlabel = 'Specific Capacity [mAh/g]',
            #ylim = (2.5,5),
            #xlim = (0, 150),
            #xticks = (np.arange(0, 150), step=20)),
            #yticks = (np.arange(3, 5, step=0.2)),
            )
            ax.tick_params(direction='in', top = 'true', right = 'true')

        # If cycle life is to be plotted: Make the first subplot this.
        if self.qcplot == True:
            self.taken_subplots +=1
            # Dealing with percentage
            if self.percentage == True:
                ylabel = 'Capacity retention [%]'
                self.axes[0].yaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1, decimals = 0))
            else:
                ylabel = 'Specific capacity [mAh/g]'
            
            self.axes[0].set(
                title = 'Cycle life',
                ylabel = ylabel,
                xlabel = 'Cycles'
            )

    def give_subplot(self):
        ax = self.axes[self.taken_subplots]
        self.taken_subplots += 1 #Increment the subplots availability and give it to whomever.
        return ax


    def draw(self, save =False, show = True):
        
        if self.qcplot == True:
            # Get labels and handles for legend generation and eventual savefile
            handles, labels = self.axes[0].get_legend_handles_labels()
            handles.append(Line2D([0], [0], marker='o', color='black', alpha = 0.2, label = 'Charge capacity', linestyle=''))
            self.axes[0].legend(handles=handles)
            if type(self.specific_cycles) != bool:
                self.axes[0].scatter(self.specific_cycles, np.zeros(len(self.specific_cycles)), marker = "|")
            # Title also has to be adjusted
        
        # Makes more space.
        #self.fig.subplots_adjust(hspace=0.4, wspace=0.4)

        if self.all_in_one is True:
            plt.legend()

        # Save if True, If out path specified, save there.
        if save == True:
            savename = "CapRet"
            for label in labels:
                savename += "_" + label
            plt.savefig(savename)
        elif type(save) == str:
            plt.savefig(save)

        if show == True:
            plt.show()

            
    def get_color(self):
        give_color = self.colors[0]
        self.colors = self.colors[1:]
        return give_color

    def cycle_color(self, ncycle):
        colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
        return colors[self.specific_cycles.index(ncycle)]

    def colormap(self, color):
        color_hsv = np.asarray(mcolors.rgb_to_hsv(mcolors.to_rgb(color)))
        color_start = color_hsv.copy()
        color_end = color_hsv.copy()

        color_start[2] = 0
        color_end[2] = 1

        color1 = np.asarray(mcolors.hsv_to_rgb(color_start))*255
        color2 = np.asarray(mcolors.hsv_to_rgb(color_end))*255
        

        n = 100 #Numer of steps for colors
        diff = (color1-color2)/n
        colors = np.zeros((n,3))
        for i in range(len(colors)):
            colors[i] = color1 - i*diff
        colors = colors/255
        self.cmap = mpl.colors.LinearSegmentedColormap.from_list('colormap', colors)
        return self.cmap


    def plot_CV(self, cellobj):
        """Takes a cells dataframe and plots it in a CV plot (I/mA vs Ewe/V)"""
        # Get subplot from main plotclass
        if self.all_in_one is False:
            ax = self.give_subplot()
            ax.set_title("CV: {}".format(os.path.basename(cellobj.fn)))
        else:
            ax = self.axes[0]
            ax.set_title("Cyclic Voltammograms")
            
        # Plot it
        ax.plot(cellobj.df['Ewe/V'], cellobj.df['<I>/mA'], color = cellobj.color, label = os.path.basename(cellobj.fn))
        ax.set_ylabel("Current [mA]")
        ax.set_xlabel("Potential [V]")


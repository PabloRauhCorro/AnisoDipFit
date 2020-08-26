'''
Genetic Algorithm: Plot the score in dependence of individual parameters
'''

import sys
import numpy as np
from PyQt5 import QtTest
import scipy
from supplement.constants import const
import fitting.graphics.set_backend
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from supplement.constants import const
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

from fitting.error_estimation import calculate_score_threshold


# No. of plots: 1      2      3      4      5      6      7      8      9     10     11     12     13     14     15     16
alignement = [[1,1], [1,2], [1,3], [2,2], [2,3], [2,3], [2,4], [2,4], [3,3], [3,4], [3,4], [3,4], [4,4], [4,4], [4,4], [4,4]]


def plot_score_vs_parameters(widget, parameters, error_estimation, confidence_interval, score_vs_parameters, numerical_error, best_parameters):
    #the purpose of this try except is to remove previous plots for when a user runs error analysis multiple times


    for i in range(len(widget.subplot_list)):
        try:
            widget.figure.delaxes(widget.subplot_list[i])
        except KeyError:
            pass
        widget.subplot_list[i] = None

    ##the purpose of this try except is to remove previous colorbars for when a user runs error analysis multiple times
    try:
        widget.colorbar.remove()
        widget.colorbar = None
    except AttributeError:
        pass

    Ne = len(parameters)
    c = 1
    for i in range(Ne):
        dim = len(parameters[i])
        score_threshold = calculate_score_threshold(confidence_interval, numerical_error, dim)
        if (dim == 1):
            widget.subplot_list[i] = widget.figure.add_subplot(alignement[Ne-1][0], alignement[Ne-1][1], c )
            c = c + 1
            im = plot_1d(widget.subplot_list[i], parameters[i], score_vs_parameters[i], score_threshold, best_parameters)
        elif (dim == 2):
            widget.subplot_list[i] = widget.figure.add_subplot(alignement[Ne - 1][0], alignement[Ne - 1][1], c)
            c = c + 1
            im = plot_2d(widget.subplot_list[i], parameters[i], score_vs_parameters[i], score_threshold, best_parameters)

    cax_is_defined = 0
    if Ne ==1:
        widget.figure.subplots_adjust(wspace=0.3, hspace=0.5, right=0.7, bottom=0.25, top=0.8)
    elif Ne == 2:
        widget.figure.subplots_adjust(wspace=0.05, hspace=0.5, right=0.8, bottom=0.25, top=0.8)
        cax = widget.figure.add_axes([0.85, 0.25, 0.01, 0.57]) #left, bottom, width, height
        cax_is_defined = 1
    elif Ne == 3:
        widget.figure.subplots_adjust(wspace=0.3, hspace=0.5, left =0.1, right = 0.85, bottom = 0.25 ,top = 0.75)
        cax = widget.figure.add_axes([0.9, 0.25, 0.01, 0.5])  # left, bottom, width, height
        cax_is_defined = 1
    elif Ne == 4:
        widget.figure.subplots_adjust(wspace=0.1, hspace=0.3, left=0.2, right=0.7, bottom=0.1, top=0.95)
        cax = widget.figure.add_axes([0.75, 0.1, 0.015, 0.85])  # left, bottom, width, height
        cax_is_defined = 1
    elif Ne == 5 or Ne == 6:
        widget.figure.subplots_adjust(wspace=0.1, hspace=0.5, left=0.05, right=0.85, bottom=0.1, top=0.95)
        cax = widget.figure.add_axes([0.9, 0.1, 0.015, 0.85])  # left, bottom, width, height
        cax_is_defined = 1
    elif Ne == 8 or Ne == 7:
        widget.figure.subplots_adjust(wspace=0.4, hspace=0.5, left =0.05, right = 1.05, bottom = 0.15 ,top = 0.9)
    elif Ne == 9:
        widget.figure.subplots_adjust(wspace=0.3, hspace=0.5, left =0.1, right = 0.8, bottom = 0.1 ,top = 0.95)
        cax = widget.figure.add_axes([0.85, 0.1, 0.01, 0.8])  # left, bottom, width, height
        cax_is_defined = 1
    if not cax_is_defined:
        cax = None

    sublot_lst_for_ax_kwarg = []
    for i in range(Ne):
        sublot_lst_for_ax_kwarg.append(widget.subplot_list[i])

    widget.colorbar = widget.figure.colorbar(im, cax= cax, orientation='vertical', ax = sublot_lst_for_ax_kwarg)
    widget.colorbar.ax.set_title(const['chi2_label']['normalized_by_sn'])

    QtTest.QTest.qWait(200)
    widget.canvas.draw()
    QtTest.QTest.qWait(200)



def plot_1d(figure, parameters, score_vs_parameters, score_threshold, best_parameters):
    # Read out the values of fitting parameters and RMSD values
    name1 = parameters[0]
    x1 = [(x / const['variable_scales'][name1]) for x in score_vs_parameters[name1]]
    y = score_vs_parameters['score']
    # Read out the optimized values of fitting parameters
    x1_opt = best_parameters[name1]['value'] / const['variable_scales'][name1]
    y_opt = np.amin(y)
    # Set the maximum and the minimum of y
    cmin = np.amin(y) + score_threshold
    cmax = 2 * cmin
    # Plot the figure

    im = figure.scatter(x1, y, c=y, cmap='jet_r', vmin=cmin, vmax=cmax)
    figure.set_xlim(round(np.amin(x1),1), round(np.amax(x1),1))
    figure.set_xlabel(const['variable_labels'][name1])
    figure.set_ylabel(const['chi2_label']['normalized_by_sn'])
    figure.plot(x1_opt, y_opt, color='black', marker='o', markerfacecolor='white', markersize=12, clip_on=False)
    #plt.margins(0.05)
    # Make the axes of equal scale
    xl, xh = figure.get_xlim()
    yl, yh = figure.get_ylim()
    figure.set_aspect( (xh-xl)/(yh-yl) )
    return im


def plot_2d(figure, parameters, score_vs_parameters, score_threshold, best_parameters):
    # Read out the values of fitting parameters and RMSD values
    name1 = parameters[0]
    name2 = parameters[1]
    x1 = [(x / const['variable_scales'][name1]) for x in score_vs_parameters[name1]]
    x2 = [(x / const['variable_scales'][name2]) for x in score_vs_parameters[name2]]
    y = score_vs_parameters['score']
    # Read out th optimized values of fitting parameters
    x1_opt = best_parameters[name1]['value'] / const['variable_scales'][name1]
    x2_opt = best_parameters[name2]['value'] / const['variable_scales'][name2]
    # Interpolate the data on a regular grid
    x1min = np.min(x1)
    x1max = np.max(x1)
    x2min = np.min(x2)
    x2max = np.max(x2)
    x1r = np.linspace(x1min, x1max, num=200)
    x2r = np.linspace(x2min, x2max, num=200)


    QtTest.QTest.qWait(300)

    X, Y = np.mgrid[x1min:x1max:200j, x2min:x2max:200j]
    Z = griddata((x1, x2), y, (X, Y), method='linear')

    # Set the maximum and the minimum of Z
    cmin = np.amin(y) + score_threshold
    cmax = 2 * cmin
    # Plot the figure
    QtTest.QTest.qWait(300)
    im = figure.pcolor(X, Y, Z, cmap='jet_r', vmin=cmin, vmax=cmax)
    figure.set_xlim(np.amin(x1), np.amax(x1))
    figure.set_ylim(np.amin(x2), np.amax(x2))
    figure.set_xlabel(const['variable_labels'][name1])
    figure.set_ylabel(const['variable_labels'][name2])
    figure.plot(x1_opt, x2_opt, color='black', marker='o', markerfacecolor='white', markersize=12, clip_on=False)
    # Make the axis of equal scale
    xl, xh = figure.get_xlim()
    yl, yh = figure.get_ylim()
    # Make ticks
    figure.set_xticks(np.linspace(round(x1min, 1), round(x1max, 1), 3))
    figure.set_yticks(np.linspace(round(x2min, 1), round(x2max, 1), 3))
    figure.xaxis.labelpad = 0
    figure.yaxis.labelpad = 0
    xl, xh = figure.get_xlim()
    yl, yh = figure.get_ylim()

    figure.set_aspect((xh - xl) / (yh - yl))
    #aspect = (xh - xl) / (yh - yl)
    return im
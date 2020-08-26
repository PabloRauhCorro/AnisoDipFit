'''
Genetic Algorithm: Plot the score in dependence of optimization step
'''

import numpy as np
from supplement.constants import const
import fitting.graphics.set_backend
import matplotlib.pyplot as plt


def plot_score(widget, score, normalized_by_sn=False, save_figure=False, filename=''):
    #y = [v for v in score if not v==0]
    y = score
    x = np.linspace(1,len(y),len(y))
    widget.ax1.clear()
    widget.ax1.grid(True)
    widget.ax1.semilogy(x, y, linestyle='-', marker='o', color='k')
    widget.ax1.set_xlim(0, x[-1] + 1)
    widget.ax1.set_xlabel('Optimization step')

    if normalized_by_sn:
        widget.ax1.set_ylabel(const['chi2_label']['normalized_by_sn'])
    else:
        widget.ax1.set_ylabel(const['chi2_label']['unitary_sn'])
    widget.ax1.tick_params(length=4)
    widget.canvas.draw()


def update_score_plot( widget, score, optimization_step, normalized_by_sn=False):
    #y = [v for v in score if not v==0]
    y = score
    x = np.linspace(1,len(y),len(y))
    widget.ax1.clear()
    widget.ax1.semilogy(x, y, linestyle='-', marker='o', color='k')
    widget.ax1.set_xlim(0, optimization_step + 2)
    if optimization_step == len(score) - 1:
        widget.ax1.set_xlim(0, x[-1] + 1)
    widget.ax1.set_xlabel('The number of optimization steps')
    if normalized_by_sn:
        widget.ax1.set_ylabel(const['chi2_label']['normalized_by_sn'])
    else:
        widget.ax1.set_ylabel(const['chi2_label']['unitary_sn'])
    widget.ax1.grid(True)
    widget.canvas.draw()



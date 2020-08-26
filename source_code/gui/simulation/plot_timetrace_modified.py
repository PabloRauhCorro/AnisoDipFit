'''
Plot the simulated and experimental PDS time traces
'''

import numpy as np
import simulation.graphics.set_backend
import matplotlib.pyplot as plt


def plot_timetrace(widget,t_sim, sig_sim, t_exp, sig_exp, save_figure=False):
    try:
        widget.canvas.axes.clear()
    except AttributeError:
        widget.canvas.axes = widget.figure.add_subplot(111)
    if not (t_exp == []):    
        widget.canvas.axes.plot(t_exp, sig_exp, 'k-')
        widget.canvas.axes.plot(t_sim, sig_sim, 'r--')
        widget.canvas.axes.legend(('exp', 'sim'), loc='upper right', frameon=False)
    else:
        widget.canvas.axes.plot(t_sim, sig_sim, 'r-')
    widget.canvas.axes.set_xlim([min(t_sim), max(t_sim)])
    widget.canvas.axes.set_ylim([np.amin(sig_sim)-0.1, 1.1])
    widget.canvas.axes.set_xlabel(r'$\mathit{t}$ ($\mathit{\mu s}$)')
    widget.canvas.axes.set_ylabel('Echo intensity (a.u.)')

    widget.canvas.draw()

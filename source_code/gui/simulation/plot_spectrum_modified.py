'''
Plot the simulated and experimental dipolar spectra
'''

import numpy as np
import simulation.graphics.set_backend
import matplotlib.pyplot as plt


def plot_spectrum(widget, f_sim, spc_sim, f_exp, spc_exp, normalized=False, xn=[], ranges=[], save_figure=False):

    try:
        widget.canvas.axes.clear()
    except AttributeError:
        widget.canvas.axes = widget.figure.add_subplot(111)

    if not (f_exp == []):
        widget.canvas.axes.plot(f_exp, spc_exp, 'k-')
        widget.canvas.axes.plot(f_sim, spc_sim, 'r--')
        widget.canvas.axes.legend(('exp', 'sim'), loc='upper right', frameon=False)
        if not (ranges == []):
            widget.canvas.axes.set_xlim(-ranges['f_max'], ranges['f_max'])
            widget.canvas.axes.set_ylim(0.0, ranges['spc_max']+0.1)
        else:
            #self.sim_spectrum_plot.canvas.axes.set_xlim(np.amin(f_exp), np.amax(f_exp))
            widget.canvas.axes.set_xlim(-ranges['f_max'], ranges['f_max'])  #edited in
            widget.canvas.axes.set_ylim(0.0, np.amax(spc_exp)+0.1)
        widget.canvas.axes.set_xlabel(r'Frequency (MHz)')
        widget.canvas.axes.set_ylabel('Amplitude')
    else:
        if normalized:
            widget.canvas.axes.plot(xn, spc_sim, 'k-')
            widget.canvas.axes.set_xlim(np.amin(xn), np.amax(xn))
            widget.canvas.axes.set_ylim(0, np.amax(spc_sim)+0.1)
            widget.canvas.axes.set_xlabel(r'$\nu_{dd}$ ($\nu_{0}$)')
            widget.canvas.axes.set_ylabel('Amplitude')
        else:
            widget.canvas.axes.plot(f_sim, spc_sim, 'k-')
            widget.canvas.axes.set_xlim(-ranges['f_max'],ranges['f_max'])
            widget.canvas.axes.set_ylim(0.0, np.amax(spc_sim)+0.1)
            widget.canvas.axes.set_xlabel(r'Frequency (MHz)')
            widget.canvas.axes.set_ylabel('Amplitude')


    widget.canvas.draw()

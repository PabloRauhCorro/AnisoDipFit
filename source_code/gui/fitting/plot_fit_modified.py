
import numpy as np
import sys
import simulation.graphics.set_backend
import matplotlib.pyplot as plt


def plot_fit(widget,fit, data, fitted_data, ranges, save_figure=False, filename=''):
    widget.ax2.clear()
    widget.ax2.grid(True)
    if fitted_data == 'spectrum':
        widget.ax2.plot(data['f'], data['spc'], 'k-')
        graph = widget.ax2.plot(data['f'], fit, 'r--')
        widget.ax2.legend(('exp', 'fit'), loc='upper right', frameon=False)
        if ranges['f_max']:
            widget.ax2.set_xlim(-ranges['f_max'], ranges['f_max'])
        else:
            widget.ax2.set_xlim(np.amin(data['f']), np.amax(data['f']))
        widget.ax2.set_ylim(0.0, ranges['spc_max']+0.1)
        widget.ax2.set_xlabel(r'Frequency (MHz)')
        widget.ax2.set_ylabel('Amplitude')
    elif fitted_data == 'timetrace':
        widget.ax2.plot(data['t'], data['sig'], 'k-')
        graph = widget.ax2.plot(data['t'], fit, 'r--')
        widget.ax2.legend(('exp', 'fit'), loc='upper right', frameon=False)
        if ranges['t_max']:
            widget.ax2.set_xlim(ranges['t_min'], ranges['t_max'])
        else:
            widget.ax2.set_xlim(np.amin(data['t']), np.amax(data['t']))
        widget.ax2.set_ylim(np.amin(data['sig']) - 0.2, np.amax(data['sig']) + 0.1)
        widget.ax2.set_xlabel(r'$\mathit{t}$ ($\mathit{\mu s}$)')
        widget.ax2.set_ylabel('Echo intensity (a.u.)')

    widget.ax2.tick_params(length = 4)
    widget.canvas.draw()
    return graph


def update_fit_plot( widget, fit, graph):
    graph[0].set_ydata(fit)
    widget.canvas.draw()
    widget.canvas.flush_events()



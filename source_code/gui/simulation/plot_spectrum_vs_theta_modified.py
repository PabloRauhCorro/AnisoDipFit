'''
Plot the simulated dipolar spectra in dependence of the theta angle
'''

import numpy as np
import simulation.graphics.set_backend
import matplotlib.pyplot as plt


def plot_spectrum_vs_theta(widget, f_sim, spc_sim, theta, spc_vs_theta, normalized=False, xn=[], ranges=[], save_figure=False):
    widget.ax1.clear()
    widget.ax2.clear()
    if normalized:
        widget.ax1.plot(xn, spc_sim, 'k-')
        widget.ax1.set_xlim(np.amin(xn), np.amax(xn))
        widget.ax1.set_ylim(0, np.amax(spc_sim)+0.1)
        widget.ax1.set_xlabel(r'$\nu_{dd}$ ($\nu_{0}$)')
        widget.ax1.set_ylabel('Amplitude')
    else:
        widget.ax1.plot(f_sim, spc_sim, 'k-')
        if (ranges['f_max']):
            widget.ax1.set_xlim(-ranges['f_max'], ranges['f_max'])
            widget.ax1.set_ylim(0.0, ranges['spc_max']+0.1)
        else:
            widget.ax1.set_xlim(np.amin(f_sim), np.amax(f_sim))
            widget.ax1.set_ylim(0.0, np.amax(spc_sim)+0.1)
        widget.ax1.set_xlabel(r'Frequency (MHz)')
        widget.ax1.set_ylabel('Amplitude')

    if normalized:
        X, Y = np.meshgrid(xn, theta)
        Z = spc_vs_theta
        widget.ax2.contour(X, Y, Z, 100, cmap='jet', vmin=np.amin(Z), vmax=np.amax(Z))
        widget.ax2.set_xlim(np.amin(xn), np.amax(xn))
        widget.ax2.set_ylim(np.amin(theta), np.amax(theta))
        widget.ax2.set_xlabel(r'$\nu_{dd}$ ($\nu_{0}$)')
        widget.ax2.set_ylabel(r'$\mathit{\theta}$ (degree)')
    else:
        X, Y = np.meshgrid(f_sim, theta)
        Z = spc_vs_theta
        widget.ax2.contour(X, Y, Z, 100, cmap='jet', vmin=np.amin(Z), vmax=np.amax(Z))
        if (ranges['f_max']):
            widget.ax2.set_xlim(-ranges['f_max'], ranges['f_max'])
        else:
            widget.ax2.set_xlim(np.amin(f_sim), np.amax(f_sim))
        widget.ax2.set_ylim(np.amin(theta), np.amax(theta))
        widget.ax2.set_xlabel(r'Frequency (MHz)')
        widget.ax2.set_ylabel(r'$\mathit{\theta}$ (degree)')
    widget.canvas.draw()

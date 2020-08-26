'''
Plot the simulated dipolar spectra in dependence of some parameter
'''

import numpy as np
import simulation.graphics.set_backend
import matplotlib.pyplot as plt
from  matplotlib.figure  import  Figure
from mpl_toolkits.mplot3d import Axes3D


def plot_spectrum_vs_parameter_3d( widget, f_sim, parameter, spc_vs_parameter, normalized=False, xn=[], ranges=[],
                                  save_figure=False, par_label='', invert_parameter_axis=False):


    #widget.figure.set_tight_layout(True)
    Np = parameter.size
    Nc = int(1.5 * Np)
    cmap = plt.cm.get_cmap('gray', Nc)
    cmaplist = [cmap(i) for i in range(Nc)]
    # the purpose of this try except statement is explained in explanation.txt
    try:
        widget.figure.delaxes(widget.canvas.axes)
        widget.canvas.axes = widget.figure.gca(projection='3d')
    except AttributeError:
        widget.canvas.axes = widget.figure.gca(projection='3d')
    # Plot the spectrum vs parameter
    if normalized:
        for i in range(Np):
            widget.canvas.axes.plot(xn, parameter[i]*np.ones(f_sim.size), spc_vs_parameter[i], color=cmaplist[i])
        widget.canvas.axes.set_xlim(np.amin(xn), np.amax(xn))
        widget.canvas.axes.set_ylim(np.amin(parameter), np.amax(parameter))
        widget.canvas.axes.set_zlim(0.0, np.amax(spc_vs_parameter)+0.1)
        widget.canvas.axes.set_xlabel(r'$\nu_{dd}$ ($\nu_{0}$)', labelpad=20)
        widget.canvas.axes.set_ylabel(par_label, labelpad=20)
        widget.canvas.axes.set_zlabel('Amplitude', labelpad=20)
    else:
        for i in range(Np):
            if ranges['f_max']:
                idx = [j for j in range(f_sim.size) if (f_sim[j] >= -ranges['f_max']) and (f_sim[j] <= ranges['f_max'])]
                f_selected = np.array([f_sim[j] for j in idx])
                spc_vs_parameter_selected = np.array([spc_vs_parameter[i][j] for j in idx])
                widget.canvas.axes.plot(f_selected, parameter[i]*np.ones(f_selected.size), spc_vs_parameter_selected, color=cmaplist[i])
                widget.canvas.axes.set_xlim(np.amin(f_selected), np.amax(f_selected))
            else:
                widget.canvas.axes.plot(f_sim, parameter[i]*np.ones(f_sim.size), spc_vs_parameter[i], color=cmaplist[i])
                widget.canvas.axes.set_xlim(np.amin(f_sim), np.amax(f_sim))
        widget.canvas.axes.set_ylim(np.amin(parameter), np.amax(parameter))
        widget.canvas.axes.set_zlim(0.0, np.amax(spc_vs_parameter)+0.1)
        widget.canvas.axes.set_xlabel(r'Frequency (MHz)', labelpad=20)
        widget.canvas.axes.set_ylabel(par_label, labelpad=20)
        widget.canvas.axes.set_zlabel('Amplitude', labelpad=20)
    widget.canvas.axes.tick_params(axis='y', which='major', pad=10)
    widget.canvas.axes.tick_params(axis='z', which='major', pad=10)
    widget.canvas.axes.view_init(elev=45, azim=-85)

    if invert_parameter_axis:
        #widget.canvas.axes.invert_yaxis()  #broken?
        widget.canvas.axes.set_ylim(np.amax(parameter), np.amin(parameter))

    widget.canvas.draw()


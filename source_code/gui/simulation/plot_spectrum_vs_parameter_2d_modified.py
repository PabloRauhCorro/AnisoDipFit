'''
Plot the simulated dipolar spectra in dependence of some parameter
'''

import numpy as np
import math
import simulation.graphics.set_backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_spectrum_vs_parameter_2d( widget, f_sim, parameter, spc_vs_parameter, normalized=False, xn=[], ranges=[],
                                  save_figure=False, par_label='', invert_parameter_axis=False):

    #the purpose of this try except statement is explained in explanation.txt
    try:
        widget.figure.delaxes(widget.canvas.axes)
        widget.canvas.axes = widget.figure.add_subplot(111)
    except AttributeError:
        widget.canvas.axes = widget.figure.add_subplot(111)
    Nx = f_sim.size
    Np = parameter.size
    Nskip = Nskip = int((Np-1) / 10) + 1
    count = 0
    # Set the values of increment and baseline
    if invert_parameter_axis:
        increment = -0.7 * np.amax(spc_vs_parameter)
        baseline = (-increment * Np) * np.ones(Nx)
    else:
        increment = 0.7 * np.amax(spc_vs_parameter)
        baseline = np.zeros(Nx)

    if normalized:
        for i in range(Np):
            widget.canvas.axes.plot(xn, spc_vs_parameter[i] + baseline, 'k-')
            if (count == 0):
                widget.canvas.axes.text(np.amax(xn)+0.5, baseline[0]-0.07, str(int(parameter[i])))
            count = count + 1
            if (count == Nskip):
                count = 0
            baseline = baseline + increment * np.ones(Nx)
            if (i == Np-1):
                widget.canvas.axes.text(np.amax(xn)+0.5, baseline[0]+0.4*Nskip*increment, par_label)
        widget.canvas.axes.set_xlim(np.amin(xn), np.amax(xn))
        widget.canvas.axes.set_xlabel(r'$\nu_{dd}$ ($\nu_{0}$)')
        widget.canvas.axes.set_xticks(np.linspace(-math.floor(np.amax(xn)), math.floor(np.amax(xn)), 2 * int(math.floor(np.amax(xn))) + 1))
        widget.canvas.axes.xaxis.grid(color='darkgray', linestyle='--', linewidth=1)
    else:
        #this if statement was added to make sure that the axis limits of the 2d plot are -f_max, f_max
        if ranges['f_max'] <np.amax(f_sim) and ranges['f_max'] != 0:
            k = 0
            for each in f_sim:
                if each <= -ranges['f_max']:
                    k += 1

            j = 0
            for each in f_sim:
                if each <= ranges['f_max']:
                    j += 1
            f_sim = f_sim[k:j]
            Nx = f_sim.size
            spc_vs_parameter = spc_vs_parameter[0:Np, k:j]
            baseline = baseline[k:j]

        for i in range(Np):
            widget.canvas.axes.plot(f_sim, spc_vs_parameter[i]+baseline, 'k-')
            if (count == 0):
                widget.canvas.axes.text(np.amax(f_sim)+0.5, baseline[0]-0.07, str(int(parameter[i])))
            count = count + 1
            if (count == Nskip):
                count = 0
            baseline = baseline + increment * np.ones(Nx)
            if (i == Np-1):
                widget.canvas.axes.text(np.amax(f_sim)+0.5, baseline[0]+0.4*Nskip*increment, par_label)
        widget.canvas.axes.set_xlim(np.amin(f_sim), np.amax(f_sim))
        widget.canvas.axes.set_xlabel(r'Frequency (MHz)')
    #axes.set_ylabel('Amplitude')   
    widget.canvas.axes.spines['left'].set_visible(False)
    widget.canvas.axes.spines['right'].set_visible(False)
    widget.canvas.axes.spines['top'].set_visible(False)
    widget.canvas.axes.tick_params(axis = 'y', which = 'both', left = False, right = False, labelleft = False, labelright = False)
    widget.canvas.axes.tick_params(axis = 'x', which = 'both', top = False, bottom = True)
    widget.canvas.draw()

'''
Save fitting results
'''

import sys
import numpy as np
from fitting.output.save_fit import save_fit
from fitting.output.save_score import save_score
from fitting.output.save_fitting_parameters import save_fitting_parameters


from fitting.graphics.plot_fit import plot_fit
from fitting.graphics.plot_score import plot_score

import traceback


def save_fitting_data(optimizer, exp_data, fit_settings, output_settings, calc_settings, fitted_data_type):

    sys.stdout.write('Saving the fitting results into the directory:\n')
    sys.stdout.write(output_settings['directory'])
    # Save the fit
    filename = output_settings['directory'] + 'fit_' + fitted_data_type + '.dat'
    save_fit(optimizer.best_fit, exp_data, fitted_data_type, filename)
    # Saves the score vs optimization step
    filename = output_settings['directory'] + 'score_'+ fitted_data_type +'.dat'
    save_score(optimizer.best_score, filename)
    # Save the optimized fitting parameters
    filename = output_settings['directory'] + 'optimized_parameters_of_'+ fitted_data_type+ '_fit' +'.dat'
    save_fitting_parameters(optimizer.best_parameters, filename)

    filename = output_settings['directory'] + 'fit_' + fitted_data_type + '.png'
    fig_fit, graph_fit = plot_fit(optimizer.best_fit, exp_data, fitted_data_type ,
                                  calc_settings, output_settings['save_figures'], filename)
    filename = output_settings['directory'] + 'score_'+ fitted_data_type +'.png'
    fig_score, axes_score = plot_score(optimizer.best_score, True, output_settings['save_figures'], filename)
    sys.stdout.write('[DONE]\n\n')




'''
Saves the results of error analysis
'''

import sys
import numpy as np

from fitting.output.save_fitting_parameters import save_fitting_parameters
from fitting.graphics.plot_score_vs_parameters import plot_score_vs_parameters
from fitting.graphics.plot_confidence_intervals import plot_confidence_intervals

from save_data.save_score_vs_parameters_modified import save_score_vs_parameters


def save_error_analysis_data(optimizer, err_settings, output_settings, fitted_data_type):

    sys.stdout.write('Saving the results of the error analysis into the directory:\n')
    sys.stdout.write(output_settings['directory'])
    # Save the optimized fitting parameters
    filename = output_settings['directory'] + 'parameters_of_'+ fitted_data_type+'_fit_with_errors.dat'
    save_fitting_parameters(optimizer.best_parameters, filename)
    # Save the score vs individual fitting parameters
    save_score_vs_parameters(err_settings['variables'], optimizer.score_vs_parameters, output_settings['directory'], fitted_data_type)

    sys.stdout.write('Plotting the results of the error analysis... ')

    filename = output_settings['directory'] + 'parameter_errors_'+ fitted_data_type +'.png'
    plot_score_vs_parameters(err_settings['variables'], optimizer.score_vs_parameters,
                             err_settings['confidence_interval'], optimizer.numerical_error, optimizer.best_parameters,
                             output_settings['save_figures'], filename)
    filename = output_settings['directory'] + 'confidence_intervals_' + fitted_data_type + '.png'
    plot_confidence_intervals(err_settings['variables'], optimizer.score_vs_parameters,
                              err_settings['confidence_interval'], optimizer.numerical_error, optimizer.best_parameters,
                              output_settings['save_figures'], filename)
    sys.stdout.write('[DONE]\n\n')

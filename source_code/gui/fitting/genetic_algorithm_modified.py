'''
Genetic algorithm
'''

import sys
import time
import datetime
import numpy as np
from fitting.chromosome import Chromosome
from fitting.generation import Generation
from fitting.score_function import get_fit
from fitting.noise_estimation import calculate_noise_std
from fitting.get_parameters import get_parameters

from fitting.graphics.plot_fit import plot_fit, update_fit_plot, close_fit_plot
from fitting.graphics.plot_score import plot_score, update_score_plot, close_score_plot
from fitting.parameters2genes import parameters2genes
from supplement.constants import const

from gui.error_analysis.error_estimation_modified import ErrorEstimation

class GeneticAlgorithm:
    def __init__(self, settings, exp_data):
        self.num_generations = settings['num_generations']
        self.size_generation = settings['size_generation']
        self.prob_crossover = settings['prob_crossover']
        self.prob_mutation = settings['prob_mutation']
        self.fitted_data = settings['fitted_data']
        self.display_graphics = settings['display_graphics']
        if self.fitted_data == 'spectrum':
            self.best_fit = np.zeros(exp_data['spc'].size)
        elif self.fitted_data == 'timetrace':
            self.best_fit = np.zeros(exp_data['sig'].size)
        self.best_score = np.zeros(self.num_generations)
        self.best_parameters = {}
        self.score_vs_parameters = []
        self.numerical_error = 0


    def run_optimization(self, fit_settings, simulator, exp_data, spinA, spinB, calc_settings, fitting_thread):
        sys.stdout.write('Starting the fitting...\n')
        self.GUI_statusbar_updater(fitting_thread, 'Fitting..')
        self.GUI_progressbar_updater(fitting_thread, 0)
        time_start = time.time()
        for i in range(self.num_generations):
            if (i == 0):
                # Create the first generation
                self.generation = Generation(self.size_generation)
                self.generation.first_generation(fit_settings['parameters']['bounds'])
            else:
                # Create the next generation
                self.generation.produce_offspring(fit_settings['parameters']['bounds'], self.prob_crossover,
                                             self.prob_mutation)
            # Score the generation
            self.generation.score_chromosomes(fit_settings, simulator, exp_data, spinA, spinB, calc_settings)
            # Sort chromosomes according to their score
            self.generation.sort_chromosomes()
            # Save the best score in each optimization step
            self.best_score[i] = self.generation.chromosomes[0].score
            # Calculate the best fit
            self.best_fit = get_fit(self.generation.chromosomes[0].genes, fit_settings, simulator, exp_data, spinA, spinB,
                              calc_settings)
            self.best_parameters = get_parameters(self.generation.chromosomes[0].genes,
                                                  fit_settings['parameters']['indices'],
                                                  fit_settings['parameters']['fixed'])
            fitting_thread.fit_results_for_parameter_table.emit(2, self.best_parameters)
            # Emit signal for plotting in GUI
            fitting_thread.fit_results_for_dynamic_plotting.emit(i, self.best_fit, self.best_score)
            percentage_value = 100* (i+1)/self.num_generations
            self.GUI_progressbar_updater(fitting_thread, int(percentage_value))
            sys.stdout.write('\r')
            sys.stdout.write("Optimization step %d / %d: chi2 = %f" % (i + 1, self.num_generations, self.best_score[i]))
            sys.stdout.flush()
        # Check that Chi2 is normalized by the variance of noise
        if calc_settings['noise_std'] == 0:
            noise_std = calculate_noise_std(self.best_fit, exp_data, fit_settings, calc_settings)
            calc_settings['noise_std'] = noise_std
            self.best_score = self.best_score / noise_std ** 2
        # Store the best genes
        time_finish = time.time()
        time_elapsed = str(datetime.timedelta(seconds=time_finish - time_start))
        sys.stdout.write('\n')
        sys.stdout.write('The fitting is finished. Total duration: %s\n\n' % (time_elapsed))
        self.GUI_statusbar_updater(fitting_thread, f'The fitting is finished. Total duration: {time_elapsed}')

    def error_analysis(self, err_settings, fit_settings, simulator, exp_data, spinA, spinB, calc_settings, error_analysis_thread):
        if not (err_settings['variables'] == []):
            self.GUI_progressbar_updater(error_analysis_thread, 5)
            sys.stdout.write('Starting the error analysis...\n')
            time_start = time.time()
            self.error_estimation = ErrorEstimation()
            self.GUI_statusbar_updater(error_analysis_thread, 'Calculating the dependence of score on fitting parameters...')
            # Calculate the dependence of score on fitting parameters
            self.score_vs_parameters = self.error_estimation.calculate_score_vs_parameters(self.best_parameters, err_settings, fit_settings,
                                                                     simulator, exp_data, spinA, spinB, calc_settings, error_analysis_thread)
            # Calculate the errors of fitting parameters
            self.GUI_statusbar_updater(error_analysis_thread, 'Calculating the errors of fitting parameters...')
            self.GUI_progressbar_updater(error_analysis_thread, 0)
            parameter_errors, self.numerical_error = self.error_estimation.calculate_parameter_errors(self.score_vs_parameters,
                                                                                self.best_parameters, err_settings,
                                                                                fit_settings, simulator, exp_data,
                                                                                spinA, spinB, calc_settings, error_analysis_thread)
            # Store the calculated errors together with the optimized parameters
            best_genes = parameters2genes(self.best_parameters)
            self.best_parameters = get_parameters(best_genes, fit_settings['parameters']['indices'],
                                                  fit_settings['parameters']['fixed'], parameter_errors)


            time_finish = time.time()
            time_elapsed = str(datetime.timedelta(seconds=time_finish - time_start))
            sys.stdout.write('The error analysis is finished. Total duration: %s\n\n' % (time_elapsed))
            self.GUI_statusbar_updater(error_analysis_thread, f'The error analysis is finished. Total duration: {time_elapsed}')

    def print_optimized_parameters(self):
        sys.stdout.write('Optimized fitting parameters:\n')
        sys.stdout.write(
            "{0:<16s} {1:<16s} {2:<16s} {3:<16s}\n".format('Parameter', 'Value', 'Optimized', 'Precision (+/-)'))
        for name in const['variable_names']:
            parameter = self.best_parameters[name]
            sys.stdout.write("{0:<16s} ".format(parameter['longname']))
            sys.stdout.write("{0:<16.3f} ".format(parameter['value'] / const['variable_scales'][name]))
            sys.stdout.write("{0:<16s} ".format(parameter['optimized']))
            sys.stdout.write("{0:<16.3f} \n".format(parameter['precision'] / const['variable_scales'][name]))
        sys.stdout.write('\n')


    def GUI_statusbar_updater(self, thread, status_message):
        thread.statusbar_signal.emit(status_message)

    def GUI_progressbar_updater(self, thread, progress_value):
        thread.progressbar_signal.emit(progress_value)

    def terminate_processes(self, mode):
        if mode == "fitting":
            self.generation.pool.terminate()
        elif mode == "error analysis":
            self.error_estimation.generation.pool.terminate()
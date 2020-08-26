from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import multiprocessing

from simulation.simulation_modified import Simulator
from fitting.genetic_algorithm_modified import GeneticAlgorithm

from fitting.noise_estimation import calculate_fit_and_noise_std



#this is a thread that performs the errior analysis calculations from DipFit. It is executed when run_button in GUI is pressed.
#Threading is necessary to avoid GUI freeze. The error analysis results are sent to the GUI using the signal/slot system
#Plotting will then be done in the main thread to ensure thread safety.
#subclass of QThread

class ErrorAnalysisThread(QThread):

    progressbar_signal = QtCore.pyqtSignal(int)
    statusbar_signal = QtCore.pyqtSignal(str)
    err_results_for_parameter_table = QtCore.pyqtSignal(int, dict)
    err_results_for_plotting = QtCore.pyqtSignal(GeneticAlgorithm)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        simulator = Simulator(self.ui.calc_settings)
        self.statusbar_signal.emit("Initializing the error analysis...")
        simulator.init_fitting(self.ui.fit_settings, self.ui.exp_data, self.ui.spinA, self.ui.spinB, self.ui.calc_settings)
        # Optimizer
        if self.ui.fit_settings['settings']['method'] == "genetic":
            self.optimizer = GeneticAlgorithm(self.ui.fit_settings['settings'], self.ui.exp_data)
        # Set the best parameters
        self.optimizer.best_parameters = self.ui.err_settings['optimized_parameters']
        # Check that the variance of noise is not 0
        if self.ui.calc_settings['noise_std'] == 0:
            self.ui.calc_settings['noise_std'] = calculate_fit_and_noise_std(self.optimizer.best_parameters, self.ui.fit_settings, simulator, self.ui.exp_data, self.ui.spinA, self.ui.spinB, self.ui.calc_settings)
        # Run the error analysis
        self.optimizer.error_analysis(self.ui.err_settings, self.ui.fit_settings, simulator, self.ui.exp_data, self.ui.spinA, self.ui.spinB, self.ui.calc_settings, self)
        self.optimizer.print_optimized_parameters()
        self.err_results_for_parameter_table.emit(1, self.optimizer.best_parameters)
        self.err_results_for_plotting.emit(self.optimizer)

    def terminate_processes(self):
        if multiprocessing.active_children():
            self.optimizer.terminate_processes("error analysis")

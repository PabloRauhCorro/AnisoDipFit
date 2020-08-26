from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import multiprocessing
import numpy as np

from simulation.simulation_modified import Simulator
from fitting.genetic_algorithm_modified import GeneticAlgorithm



#this is a thread that performs the fitting calculations from DipFit. It is executed when run_button in GUI is pressed.
#Threading is necessary to avoid GUI freeze. The fitting results are sent to the GUI using the signal/slot system
#Plotting will then be done in the main thread to ensure thread safety

#subclass of QThread



class FittingThread(QThread):

    fit_results_for_dynamic_plotting = QtCore.pyqtSignal(int, np.ndarray, np.ndarray)
    statusbar_signal = QtCore.pyqtSignal(str)
    progressbar_signal = QtCore.pyqtSignal(int)
    fit_results_for_parameter_table = QtCore.pyqtSignal(int, dict)
    reactivate_run_button_signal = QtCore.pyqtSignal(int)
    final_fit_results = QtCore.pyqtSignal(GeneticAlgorithm)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui


    def run(self):
        simulator = Simulator(self.ui.calc_settings)
        self.statusbar_signal.emit("Initializing the fitting process...")
        simulator.init_fitting(self.ui.fit_settings, self.ui.exp_data, self.ui.spinA, self.ui.spinB, self.ui.calc_settings)
        if self.ui.fit_settings['settings']['method'] == "genetic":
            # Optimizer
            self.optimizer = GeneticAlgorithm(self.ui.fit_settings['settings'], self.ui.exp_data)
            # Run the fitting
            # The argument self is added to enable statusbar updates, dynamic plotting by sending signals
            self.optimizer.run_optimization(self.ui.fit_settings, simulator, self.ui.exp_data, self.ui.spinA, self.ui.spinB, self.ui.calc_settings, self)
            self.final_fit_results.emit(self.optimizer)
            self.reactivate_run_button_signal.emit(1)

    def terminate_processes(self):
        if multiprocessing.active_children():
            self.optimizer.terminate_processes("fitting")

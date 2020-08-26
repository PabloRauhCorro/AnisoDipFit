from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from simulation.simulation_modified import Simulator
import sys
import traceback

#this is a thread that performs the simulation calculations from DipFit. It is executed when run_button in GUI is pressed.
#Threading is necessary to avoid GUI freeze. The simulation results are sent to the GUI using the signal/slot system
#Plotting will then be done in the main thread to ensure thread safety
#subclass of QThread

class SimulationThread(QThread):

    sim_results_signal = QtCore.pyqtSignal(Simulator)
    statusbar_signal = QtCore.pyqtSignal(str)
    progressbar_signal = QtCore.pyqtSignal(int)
    RMSD_spc_signal = QtCore.pyqtSignal(float)
    RMSD_timetr_signal = QtCore.pyqtSignal(float)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):

        simulator = Simulator(self.ui.calc_settings)
        #The argument self is added to enable statusbar updates (see run_simulation_for further info)
        simulator.run_simulation(self.ui.sim_settings, self.ui.exp_data, self.ui.spinA, self.ui.spinB, self.ui.calc_settings, self)
        self.sim_results_signal.emit(simulator)

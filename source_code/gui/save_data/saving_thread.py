from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from simulation.output.save_simulation_data import save_simulation_data
from simulation.graphics.plot_simulation_data import plot_simulation_data

from save_data.save_fitting_data_modified import save_fitting_data
from save_data.save_error_analysis_data_modified import save_error_analysis_data




class Saving_Thread(QThread):

    statusbar_signal = QtCore.pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def pass_mode(self, mode):
        self.mode = mode

    def run(self):

        if self.mode == 'simulation':
            save_simulation_data(self.ui.simulation_results,  self.ui.sim_settings, self.ui.exp_data, self.ui.output_settings)
            plot_simulation_data(self.ui.simulation_results, self.ui.sim_settings, self.ui.exp_data, self.ui.calc_settings, self.ui.output_settings)
            self.statusbar_signal.emit('The simulation results and graphics have been saved')


        elif self.mode == 'fitting':

            if hasattr(self.ui, 'fit_results_spc'):
                save_fitting_data(self.ui.fit_results_spc, self.ui.exp_data, self.ui.fit_settings,
                                  self.ui.output_settings, self.ui.calc_settings, 'spectrum')
            if hasattr(self.ui, 'fit_results_timetrace'):
                save_fitting_data(self.ui.fit_results_timetrace, self.ui.exp_data, self.ui.fit_settings,
                                  self.ui.output_settings, self.ui.calc_settings, 'timetrace')
            self.statusbar_signal.emit('The fitting results and graphics have been saved')



        elif self.mode == 'error_analysis':
            if hasattr(self.ui, 'err_analysis_results_spc'):
                save_error_analysis_data(self.ui.err_analysis_results_spc, self.ui.err_settings_spc, self.ui.output_settings, 'spectrum')
            if hasattr(self.ui, 'err_analysis_results_timetrace'):
                save_error_analysis_data(self.ui.err_analysis_results_timetrace, self.ui.err_settings_timetrace, self.ui.output_settings, 'timetrace')
            self.statusbar_signal.emit('The error analysis results and graphics have been saved')
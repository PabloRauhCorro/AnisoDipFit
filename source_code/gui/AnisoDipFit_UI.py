

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import multiprocessing


from interface.QMainWindow_modified import QMainWindow
from interface.add_methods_to_class import add_methods_to_class
from interface.setupUi import setupUi
from interface.retranslateUi import retranslateUi
from interface.gen_algorithm_param_window import Gen_Algorithm_Parameter_Window
from interface.about_window import About_Window


from input.dictionary_updater import dictionary_updater
from input.config_file_creation import dict_for_cfg, create_cfg_file
from input.update_GUI_from_cfg import update_GUI_from_cfg

from simulation.simulation_modified import Simulator
from simulation.simulation_thread import SimulationThread
from simulation.plot_spectrum_modified import plot_spectrum
from simulation.plot_timetrace_modified import plot_timetrace
from simulation.plot_spectrum_vs_theta_modified import plot_spectrum_vs_theta
from simulation.plot_spectrum_vs_parameter_2d_modified import plot_spectrum_vs_parameter_2d
from simulation.plot_spectrum_vs_parameter_3d_modified import plot_spectrum_vs_parameter_3d

from fitting.plot_score_modified import plot_score, update_score_plot
from fitting.plot_fit_modified import plot_fit, update_fit_plot
from fitting.genetic_algorithm_modified import GeneticAlgorithm
from fitting.fitting_thread import FittingThread

from error_analysis.error_estimation_modified import ErrorEstimation
from error_analysis.error_analysis_thread import ErrorAnalysisThread
from error_analysis.plot_score_vs_parameters_modified import plot_score_vs_parameters
from error_analysis.plot_confidence_interval_modified import plot_confidence_intervals

from save_data.saving_thread import Saving_Thread

sys.path.append('..')

from input.load_spectrum import load_spectrum
from input.load_timetrace import load_timetrace
from input.symmetric_boundaries import symmetric_boundaries

from supplement.constants import const
import interface.set_style



#This class decorator adds methods to the class (see file add_methods_to_class.py)
#The methods are stored in the tuple "methods"
#The purpose of this decorator is to improve code readability and structure by reducing the code length of this file (GUIproto.py)
#for example, the functions setupUi and retranslateUi contain 3000+ lines of code that mostly does trivial widget labeling (created in QtDesigner)

methods = (setupUi, retranslateUi, dictionary_updater, dict_for_cfg, create_cfg_file, update_GUI_from_cfg)

@add_methods_to_class(methods)
class Ui_MainWindow(object):

    def __init__(self):
        self.setupUi(MainWindow)
        self.button_event_connector()
        self.deactivate_widgets()
        self.set_parameter_dictionaries()

    #the dictionaries of the parameters that are needed to perform the calculations. These dictionaries will be filled based on user input to the GUI
    def set_parameter_dictionaries(self):
        self.mode = {'simulation': 0, 'fitting': 0, 'error_analysis': 0}
        self.exp_data = {'path_spectrum': '', 'path_timetrace': '', 't': [], 'sig': [], 'f': [], 'spc': []}
        self.spinA = {'type': '', 'g': ''}
        self.spinB = {'type': '', 'g': ''}
        self.sim_settings = {'modes': {}, 'parameters': {}, 'settings': {'plot_3d': 0, 'faxis_normalized': 0}}
        self.fit_settings = {'settings': {'fitted_data' : '', 'method': 'genetic', 'num_generations': 500, 'size_generation': 128,
                                          'prob_crossover': 0.5, 'prob_mutation': 0.01, 'display_graphics': 0},
                             'parameters': {}}
        self.err_settings = {}
        self.calc_settings = {'Ns': '', 'r_distr': '', 'xi_distr': '', 'phi_distr': '', 'f_min': '',
                              'f_max': '', 't_min': '', 't_max': '', 'g_selectivity': '', 'spc_max': ''}
        self.output_settings = {'directory': '', 'save_data': 1, 'save_figures': 1}
        self.filename = self.output_settings['directory'] + 'spc.png'
        self.log_text = ""


    # this function will be called when the run button is pressed and it will inititiate the DIPfit code in a different thread)
    def on_run_button_click(self):
        self.deactivate_widgets(2)
        self.dictionary_updater()

        if self.mode['fitting'] or self.mode['error_analysis']:
            if not self.check_if_user_entered_exp_data():
                self.deactivate_widgets(1)
                self.do_not_proceed = 1
        if hasattr(self, 'do_not_proceed'):
            if self.do_not_proceed:
                return None

        if self.mode['simulation']:
            self.simulation_thread = SimulationThread(self)
            self.simulation_thread.sim_results_signal.connect(self.plot_sim_data_on_GUI)
            self.simulation_thread.statusbar_signal.connect(self.statusbar_adder)
            self.simulation_thread.progressbar_signal.connect(self.progressbar_updater)
            self.simulation_thread.start()
            self.sim_checkbox_comboBox_connector()


        elif self.mode['fitting']:
            self.update_parameter_fit_output_table(0, best_parameters=None)
            self.fitting_tab.setTabEnabled(2, True)
            self.fitting_thread = FittingThread(self)
            self.fitting_thread.fit_results_for_dynamic_plotting.connect(self.plot_score_and_fit_on_GUI)
            self.fitting_thread.statusbar_signal.connect(self.statusbar_adder)
            self.fitting_thread.progressbar_signal.connect(self.progressbar_updater)
            self.fitting_thread.fit_results_for_parameter_table.connect(self.update_parameter_fit_output_table)
            self.fitting_thread.reactivate_run_button_signal.connect(self.deactivate_widgets)
            self.fitting_thread.final_fit_results.connect(self.store_fit_results)
            self.fitting_thread.start()


        elif self.mode['error_analysis']:
            self.error_analysis_thread = ErrorAnalysisThread(self)
            self.error_analysis_thread.statusbar_signal.connect(self.statusbar_adder)
            self.error_analysis_thread.progressbar_signal.connect(self.progressbar_updater)
            self.error_analysis_thread.err_results_for_parameter_table.connect(self.update_parameter_fit_output_table)
            self.error_analysis_thread.err_results_for_plotting.connect(self.plot_error_analysis_on_GUI)
            self.error_analysis_thread.start()


        else:
            messagebox = QMessageBox()
            messagebox.setText(
                "Do not press the run button while you are in the General Tab, as the operation mode of AnisoDipFit will be undefined.")
            messagebox.setStandardButtons(QMessageBox.Ok)
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.exec()
            self.deactivate_widgets(1)


    def on_stop_button_click(self):
        if self.mode['simulation']:
            if self.simulation_thread.isRunning():
                self.simulation_thread.terminate()
                sys.stdout.write("\nThe simulation thread has been terminated")
                self.statusbar_adder("The simulation thread has been terminated.")
                self.progressbar_updater(0)

        if self.mode['fitting']:
            if self.fitting_thread.isRunning():
                self.fitting_thread.terminate_processes()
                self.fitting_thread.terminate()
                sys.stdout.write("\nThe fitting thread and background worker processes have been terminated.\n")
                self.statusbar_adder("The fitting thread and background worker processes have been terminated.")
                self.progressbar_updater(0)

        if self.mode['error_analysis']:
            if self.error_analysis_thread.isRunning():
                self.error_analysis_thread.terminate_processes()
                self.error_analysis_thread.terminate()
                sys.stdout.write("\nThe error analysis thread and background worker processes have been terminated.\n")
                self.statusbar_adder("The error analysis thread and background worker processes have been terminated.")
                self.progressbar_updater(0)

        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)


    #This function conects buttons to their functions, called in setupUi method
    def button_event_connector(self):
        self.run_button.clicked.connect(self.on_run_button_click)
        self.stop_button.clicked.connect(self.on_stop_button_click)
        self.searchspectrum_button.clicked.connect(self.load_spectrum_path)
        self.searchtimetrace_button.clicked.connect(self.load_timetrace_path)
        self.show_exp_spec_button.toggled.connect(self.exp_spectrum_plotter)
        self.show_exptimet_button.toggled.connect(self.exp_timetrace_plotter)
        self.sim_plot_comboBox.activated.connect(self.sim_displayed_plot_changer)
        self.normalize_faxis_sim_radiobutton.toggled.connect(self.normalize_faxis_sim)
        self.plot_3d_button.toggled.connect(self.plot_3d)
        self.sim_specvsT_chbox.toggled.connect(self.g_selectivity_box.setChecked)
        self.action_save_as_cfg.triggered.connect(lambda: self.create_cfg_file(MainWindow, True))
        self.action_load_cfg.triggered.connect(self.update_GUI_from_cfg)
        self.action_save_sim_results.triggered.connect(self.save_simulation_results)
        self.action_save_fit_results.triggered.connect(self.save_fitting_results)
        self.action_save_err_results.triggered.connect(self.save_error_analysis_results)
        self.action_save_log.triggered.connect(self.save_log_file)
        self.menuAbout.aboutToShow.connect(self.show_about_window)
        self.open_log_button.clicked.connect(self.show_log)
        self.edit_algorithm_pbutton.clicked.connect(self.show_algorithm_parameters)
        self.maxf_line.editingFinished.connect(self.exp_spectrum_plotter)
        self.maxf_line.editingFinished.connect(self.plot_3d)
        self.maxtime_line.editingFinished.connect(self.exp_timetrace_plotter)
        self.search_opt_param_file_button.clicked.connect(self.load_optimized_parameters)

        self.g_selectivity_box.stateChanged.connect(lambda : self.deactivate_widgets(4))
        self.fit_data_type_combox.activated.connect(lambda : self.deactivate_widgets(5))
        self.use_fit_results_chbox.stateChanged.connect(lambda : self.deactivate_widgets(3))
        self.r_mean_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(1))
        self.r_width_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(2))
        self.phi_mean_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(3))
        self.phi_width_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(4))
        self.xi_mean_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(5))
        self.xi_width_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(6))
        self.temp_opt_chbox.stateChanged.connect(lambda : self.err_analysis_parameter_table_displayer(7))



    # these functions are used to enable the user to browse his directories for the experimental data
    def load_spectrum_path(self, spectrum_path_given_from_cfg = 0):

        if not spectrum_path_given_from_cfg:
            self.filedialog = QtWidgets.QFileDialog()
            self.spectrumpath_line.setText(self.filedialog.getOpenFileName(MainWindow, 'Load spectrum', "", "(*.txt, *.dat)")[0])

        #if statement because the user might close the filedialog without choosing anything
        if not self.spectrumpath_line.text() == "":
            self.exp_data['path_spectrum'] = self.spectrumpath_line.text()
            f, spc = load_spectrum(self.exp_data['path_spectrum'])

            # check if user accidentally loaded his timetrace, which would lead to program crash
            if f[0] == 0 and np.amax(spc) == spc[0]:
                messagebox = QMessageBox()
                messagebox.setText("Did you load a timetrace instead of a spectrum? Please recheck the provided filepath.")
                messagebox.setStandardButtons(QMessageBox.Ok)
                messagebox.setIcon(QMessageBox.Warning)
                messagebox.exec()
                return None

            self.exp_data['f'], self.exp_data['spc'] = symmetric_boundaries(f, spc)
            if not spectrum_path_given_from_cfg or self.maxf_line.text() == '0':
                self.maxf_line.setText(str(round(np.amax(self.exp_data['f']), 1)))
            self.show_exp_spec_button.setChecked(True)
            self.fit_data_type_combox.setCurrentText('Spectrum')


    def load_timetrace_path(self, timetrace_path_given_from_cfg = 0):
        if not timetrace_path_given_from_cfg:
            self.filedialog2 = QtWidgets.QFileDialog()
            self.timetracepath_line.setText(self.filedialog2.getOpenFileName(MainWindow, 'Load timetrace',"", "(*.txt, *.dat)")[0])

        #if statement because the user might close the file dialog without choosing anything
        if not self.timetracepath_line.text() == "":
            self.exp_data['path_timetrace'] = self.timetracepath_line.text()
            self.exp_data['t'], self.exp_data['sig'] = load_timetrace(self.exp_data['path_timetrace'])
            if not timetrace_path_given_from_cfg or self.maxtime_line.text() == "0":
                self.maxtime_line.setText(str(round(np.amax(self.exp_data['t']), 1)))
            self.show_exptimet_button.setChecked(True)
            self.fit_data_type_combox.setCurrentText('Time trace')


    #these functions are used to plot experimental data in the general tab. Uses pyqtgraph as plot-package, not matplotlib. Change later
    def exp_spectrum_plotter(self):
        try:
            self.exp_data_plot.canvas.axes.clear()
        except AttributeError:
            self.exp_data_plot.canvas.axes = self.exp_data_plot.figure.add_subplot(111)
        #this is just a way of checking if there is data in exp_data['f']
        try:
            self.exp_data['f'][0]
            self.exp_data_plot.canvas.axes.plot(self.exp_data['f'], self.exp_data['spc'], 'k-')

        except IndexError:
            if self.spectrumpath_line.text():
                self.exp_data['path_spectrum'] = self.spectrumpath_line.text()
                f, spc = load_spectrum(self.exp_data['path_spectrum'])
                self.exp_data['f'], self.exp_data['spc'] = symmetric_boundaries(f, spc)
                self.exp_data_plot.canvas.axes.plot(self.exp_data['f'], self.exp_data['spc'], 'k-')

        self.exp_data_plot.canvas.axes.set_xlabel(r'Frequency (MHz)')
        self.exp_data_plot.canvas.axes.set_ylabel('Amplitude')
        self.exp_data_plot.canvas.axes.set_xlim(-float(self.maxf_line.text()), float(self.maxf_line.text()))
        self.exp_data_plot.canvas.draw()


    def exp_timetrace_plotter(self):
        #this is just a way of checking is an axes has already been created
        try:
            self.exp_data_plot.canvas.axes.clear()
        except AttributeError:
            self.exp_data_plot.canvas.axes = self.exp_data_plot.figure.add_subplot(111)

        #this is just a way of checking if there is data in exp_data['t']
        try:
            self.exp_data['t'][0]
            self.exp_data_plot.canvas.axes.plot(self.exp_data['t'], self.exp_data['sig'], 'k-')
        except IndexError:
            if self.timetracepath_line.text():
                self.exp_data['path_timetrace'] = self.timetracepath_line.text()
                self.exp_data['t'], self.exp_data['sig'] = load_timetrace(self.exp_data['path_timetrace'])
                self.exp_data_plot.canvas.axes.plot(self.exp_data['t'], self.exp_data['sig'], 'k-')
            else:
                return None

        self.exp_data_plot.canvas.axes.set_xlabel(r'$\mathit{t}$ ($\mathit{\mu s}$)')
        self.exp_data_plot.canvas.axes.set_ylabel('Echo intensity (a.u.)')
        self.exp_data_plot.canvas.axes.set_xlim( 0,float(self.maxtime_line.text()))
        self.exp_data_plot.canvas.draw()


    def load_optimized_parameters(self):
        self.filedialog2 = QtWidgets.QFileDialog()
        self.opt_param_line.setText(
            self.filedialog2.getOpenFileName(MainWindow, 'Load optimized fitting parameters', "", "(*.txt, *.dat)")[0])


    def check_if_user_entered_exp_data(self):
        exp_data_was_given = 1
        if self.spectrumpath_line.text() == "" and self.timetracepath_line.text() == "":
            exp_data_was_given = 0
        elif self.mode['fitting']:
            if self.fit_settings['settings']['fitted_data'] == 'spectrum' and self.spectrumpath_line.text() == "":
                exp_data_was_given = 0
            elif self.fit_settings['settings']['fitted_data'] == 'timetrace' and self.timetracepath_line.text() == "":
                exp_data_was_given = 0

        if not exp_data_was_given:
            messagebox = QMessageBox()
            messagebox.setText("No experimental data was given ")
            messagebox.setStandardButtons(QMessageBox.Ok)
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.exec()
        return exp_data_was_given

    # this function is connected to the signal emitted by the simulation thread (see on_run_button_click and simulation_thread).
    # simulator is stored in a variable called simulation_results to ensure that the class method normalize_f_axis_sim works
    # without having to rerun the simulation thread
    def plot_sim_data_on_GUI(self, simulator, does_plotting_happen_after_calculation=1):

        # storing the simulation results
        self.simulation_results = simulator

        # delegation for plotting simulation data
        sys.stdout.write('Plotting the simulation results... ')

        if self.sim_settings['modes']['spc']:
            plot_spectrum(self.sim_spectrum_plot, simulator.f, simulator.spc, self.exp_data['f'], self.exp_data['spc'],
                          self.sim_settings['settings']['faxis_normalized'], simulator.fn, self.calc_settings,
                          self.output_settings['save_figures'])

        if self.sim_settings['modes']['timetrace']:
            plot_timetrace(self.sim_timetrace_plot, simulator.t, simulator.sig, self.exp_data['t'],
                           self.exp_data['sig'],
                           self.output_settings['save_figures'])

        if self.sim_settings['modes']['spc_vs_theta']:
            plot_spectrum_vs_theta(self.sim_spec_vs_theta_plot, simulator.f, simulator.spc, simulator.theta_bins,
                                   simulator.spc_vs_theta,
                                   self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                   self.calc_settings,
                                   self.output_settings['save_figures'])

        if self.sim_settings['modes']['spc_vs_xi']:
            parameter_label = r'$\mathit{\xi}$ ' + u'(\N{DEGREE SIGN})'
            if self.sim_settings['settings']['plot_3d']:
                plot_spectrum_vs_parameter_3d(self.sim_spec_vs_xi_plot, simulator.f, simulator.xi_bins,
                                              simulator.spc_vs_xi,
                                              self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                              self.calc_settings,
                                              self.output_settings['save_figures'], parameter_label, False)
            else:
                plot_spectrum_vs_parameter_2d(self.sim_spec_vs_xi_plot, simulator.f, simulator.xi_bins,
                                              simulator.spc_vs_xi,
                                              self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                              self.calc_settings,
                                              self.output_settings['save_figures'], parameter_label, False)

        if self.sim_settings['modes']['spc_vs_phi']:
            parameter_label = r'$\mathit{\phi}$ ' + u'(\N{DEGREE SIGN})'
            if self.sim_settings['settings']['plot_3d']:
                plot_spectrum_vs_parameter_3d(self.sim_spec_vs_phi_plot, simulator.f, simulator.phi_bins,
                                              simulator.spc_vs_phi,
                                              self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                              self.calc_settings,
                                              self.output_settings['save_figures'], parameter_label, False)
            else:
                plot_spectrum_vs_parameter_2d(self.sim_spec_vs_phi_plot, simulator.f, simulator.phi_bins,
                                              simulator.spc_vs_phi,
                                              self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                              self.calc_settings,
                                              self.output_settings['save_figures'], parameter_label, False)

        if (self.sim_settings['modes']['spc_vs_temp'] and not simulator.spc_vs_temp == []):
            parameter_label = r'$\mathit{T (K)}$'
            if self.sim_settings['settings']['plot_3d']:
                plot_spectrum_vs_parameter_3d(self.sim_spec_vs_temp_plot, simulator.f, simulator.temp_bins,
                                              simulator.spc_vs_temp,
                                              self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                              self.calc_settings,
                                              self.output_settings['save_figures'], parameter_label, False)
            else:
                plot_spectrum_vs_parameter_2d(self.sim_spec_vs_temp_plot, simulator.f, simulator.temp_bins,
                                              simulator.spc_vs_temp,
                                              self.sim_settings['settings']['faxis_normalized'], simulator.fn,
                                              self.calc_settings,
                                              self.output_settings['save_figures'], parameter_label, False)
        sys.stdout.write('[DONE]\n\n')

        self.sim_displayed_plot_changer()
        self.tab_param_sub.setTabEnabled(2, True)
        self.deactivate_widgets(1)
        self.progressBar.setValue(0)

        if does_plotting_happen_after_calculation and not 'simulation' in MainWindow.results_are_not_saved:
            MainWindow.results_are_not_saved.append('simulation')


    def plot_score_and_fit_on_GUI(self, optimization_step, best_fit, best_score):
        if optimization_step == 0:
            plot_score(self.fit_and_score_plots, best_score, bool(self.calc_settings['noise_std']))
            self.fit_graph = plot_fit(self.fit_and_score_plots, best_fit, self.exp_data, self.fit_settings['settings']['fitted_data'], self.calc_settings )

        else:
            update_fit_plot(self.fit_and_score_plots, best_fit, self.fit_graph)
            update_score_plot(self.fit_and_score_plots, best_score, optimization_step, bool(self.calc_settings['noise_std']))


    def plot_error_analysis_on_GUI(self, err_analysis_results):

        self.store_err_analysis_results(err_analysis_results)
        # score_vs_parameters, numerical_error, best_parameters = error_analysis_test_data_2()
        self.statusbar_adder("Plotting the error analysis results...")
        self.progressbar_updater(5)
        QtTest.QTest.qWait(1000)

        error_estimation = ErrorEstimation()
        sys.stdout.write('Plotting the results of the error analysis... ')
        plot_score_vs_parameters(self.err_analysis_2d_plots, self.err_settings['variables'], error_estimation,
                                 self.err_settings['confidence_interval'], err_analysis_results.score_vs_parameters,
                                 err_analysis_results.numerical_error, err_analysis_results.best_parameters)


        self.progressbar_updater(50)
        plot_confidence_intervals(self.err_analysis_1d_plots, self.err_settings['variables'],
                                  err_analysis_results.score_vs_parameters,
                                  self.err_settings['confidence_interval'], err_analysis_results.numerical_error,
                                  err_analysis_results.best_parameters)
        sys.stdout.write('[DONE]\n\n')

        self.statusbar_adder("The error analysis results have been plotted.")
        self.progressbar_updater(0)
        self.tab_error_analysis.setTabEnabled(1, True)
        self.tab_error_analysis.setTabEnabled(2, True)
        self.deactivate_widgets(1)
        if not 'error analysis' in MainWindow.results_are_not_saved:
            MainWindow.results_are_not_saved.append('error analysis')


    # this function is used to replot simulation spectra with a normalized (or not normalized) frequency axis
    def normalize_faxis_sim(self):
        if self.normalize_faxis_sim_radiobutton.isChecked():
            self.sim_settings['settings']['faxis_normalized'] = 1
        else:
            self.sim_settings['settings']['faxis_normalized'] = 0
        self.simulation_results.normalize_faxis(self.sim_settings['parameters'])
        self.plot_sim_data_on_GUI(self.simulation_results, does_plotting_happen_after_calculation=0)

    # this function is used to replot simulation vs parameter spectra as 3d or 2d
    def plot_3d(self):
        if hasattr(self, 'simulation_results'):
            if self.plot_3d_button.isChecked():
                self.sim_settings['settings']['plot_3d'] = 1
            else:
                self.sim_settings['settings']['plot_3d'] = 0
            self.calc_settings['f_max'] = float(self.maxf_line.text())
            self.plot_sim_data_on_GUI(self.simulation_results, does_plotting_happen_after_calculation=0)


    def statusbar_adder(self, status_message):
        self.statusbar_label.setText(status_message)
        self.log_text += "\n" + status_message


    def progressbar_updater(self, progress_value):
        self.progressBar.setValue(progress_value)


    def store_fit_results(self, fit_results):

        if self.fit_settings['settings']['fitted_data'] == 'spectrum':
            self.fit_results_spc = fit_results
            self.err_analysis_type_combox.model().item(1).setEnabled(True)
        elif self.fit_settings['settings']['fitted_data'] == 'timetrace':
            self.fit_results_timetrace = fit_results
            self.err_analysis_type_combox.model().item(2).setEnabled(True)

        self.use_fit_results_chbox.setEnabled(True)
        self.use_fit_results_chbox.setChecked(True)
        self.progressbar_updater(0)
        if not 'fitting' in MainWindow.results_are_not_saved:
            MainWindow.results_are_not_saved.append('fitting')

    def store_err_analysis_results(self, err_analysis_results):

        if self.fit_settings['settings']['fitted_data'] == 'spectrum':
            self.err_analysis_results_spc = err_analysis_results
            self.err_settings_spc = self.err_settings
        elif self.fit_settings['settings']['fitted_data'] == 'timetrace':
            self.err_analysis_results_timetrace = err_analysis_results
            self.err_settings_timetrace =self.err_settings


    def show_log(self):
        log = QMessageBox()
        log.setWindowTitle("Log")
        log.setText(self.log_text)
        #log.setDetailedText("\n\n\n")
        log.setStyleSheet("QLabel{min-width: 500px; min-height: 500 px}")
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(12)
        log.setFont(font)
        log.exec()


    def save_log_file(self):
        self.filedialog = QtWidgets.QFileDialog()
        filepath = self.filedialog.getSaveFileName(MainWindow, 'Save log file', "AnisoDipFit_log", "( *.txt)")[0]
        if filepath:
            with open(filepath, 'w') as log_file:
                log_file.write(self.log_text)

    def save_simulation_results(self):
        if hasattr(self, 'simulation_results'):
            self.filedialog = QtWidgets.QFileDialog()
            filepath = self.filedialog.getExistingDirectory(MainWindow,
                                                            'Select a directory to save the simulation results')
            if filepath == '':
                return None
            self.output_settings['directory'] = filepath + "/"
            self.create_cfg_file(MainWindow, open_file_dialog=0, filepath=filepath)
            self.statusbar_adder('Saving the simulation data...')

            self.save_simulation_data_thread = Saving_Thread(self)
            self.save_simulation_data_thread.statusbar_signal.connect(self.statusbar_adder)
            self.save_simulation_data_thread.pass_mode('simulation')
            self.save_simulation_data_thread.start()

            if 'simulation' in MainWindow.results_are_not_saved:
                MainWindow.results_are_not_saved.remove('simulation')

    def save_fitting_results(self):
        if hasattr(self, 'fit_results_spc') or hasattr(self, 'fit_results_timetrace'):
            self.filedialog = QtWidgets.QFileDialog()
            filepath = self.filedialog.getExistingDirectory(MainWindow,
                                                            'Select a directory to save the fitting results')

            if filepath == '':
                return None

            self.output_settings['directory'] = filepath + "/"

            self.create_cfg_file(MainWindow, open_file_dialog=0, filepath=filepath)

            self.statusbar_adder('Saving the fitting data...')

            self.save_fitting_data_thread = Saving_Thread(self)
            self.save_fitting_data_thread.statusbar_signal.connect(self.statusbar_adder)
            self.save_fitting_data_thread.pass_mode('fitting')
            self.save_fitting_data_thread.start()

            if 'fitting' in MainWindow.results_are_not_saved:
                MainWindow.results_are_not_saved.remove('fitting')


    def save_error_analysis_results(self):
        if hasattr(self, 'err_analysis_results_spc') or hasattr(self, 'err_analysis_results_timetrace'):
            self.filedialog = QtWidgets.QFileDialog()
            filepath = self.filedialog.getExistingDirectory(MainWindow,
                                                            'Select a directory to save the error analysis results')
            if filepath == '':
                return None
            self.output_settings['directory'] = filepath + "/"

            self.create_cfg_file(MainWindow, open_file_dialog=0, filepath=filepath)

            self.statusbar_adder('Saving the error analysis results...')

            self.save_err_analysis_data_thread = Saving_Thread(self)
            self.save_err_analysis_data_thread.statusbar_signal.connect(self.statusbar_adder)
            self.save_err_analysis_data_thread.pass_mode('error_analysis')
            self.save_err_analysis_data_thread.start()

            if 'error analysis' in MainWindow.results_are_not_saved:
                MainWindow.results_are_not_saved.remove('error analysis')

    def show_about_window(self):
        self.about_window = QtWidgets.QDialog()
        self.about_window_ui = About_Window()
        self.about_window_ui.setupUi(self.about_window)
        self.about_window.show()


    #opens a pop up window to show and enable editing of the parameters of genetic algorithm
    def show_algorithm_parameters(self):
        self.new_window = QtWidgets.QDialog()
        self.new_window_ui = Gen_Algorithm_Parameter_Window(self.fit_settings['settings']['num_generations'],
                                       self.fit_settings['settings']['size_generation'],
                                       self.fit_settings['settings']['prob_crossover'],
                                       self.fit_settings['settings']['prob_mutation'])

        self.new_window_ui.setupUi(self.new_window)
        self.new_window_ui.gen_alg_confirm_button.clicked.connect(self.edit_algorithm_parameters)
        self.new_window_ui.gen_alg_cancel_button.clicked.connect(self.new_window.close)
        self.new_window.show()


    #updates the dictionary containing the genetic algorithm parameter
    def edit_algorithm_parameters(self):
        self.fit_settings['settings']['num_generations'] = int(self.new_window_ui.gen_number_line.text())
        self.fit_settings['settings']['size_generation'] = int(self.new_window_ui.chromo_number_line.text())
        self.fit_settings['settings']['prob_crossover'] = float(self.new_window_ui.crossover_rate_line.text())
        self.fit_settings['settings']['prob_mutation'] = float(self.new_window_ui.mutation_rate_line.text())
        self.new_window.close()


    # this function deactivates or activates widgets and buttons
    def deactivate_widgets(self, index=0):
        # these things need to be done right after launching the program
        if index == 0:
            self.label_68.setEnabled(False)
            self.magnetic_field_line.setEnabled(False)
            self.tab_param_sub.setTabEnabled(2, False)
            self.stop_button.setEnabled(False)
            self.fitting_tab.setTabEnabled(2, False)
            self.err_analysis_parameter_table_displayer(7)
            self.tab_error_analysis.setTabEnabled(1, False)
            self.tab_error_analysis.setTabEnabled(2, False)
            self.use_fit_results_chbox.setEnabled(False)
            self.err_analysis_type_combox.setEnabled(False)


        elif index == 1:
            self.run_button.setEnabled(True)
            self.stop_button.setEnabled(False)

        elif index == 2:
            self.run_button.setEnabled(False)
            self.stop_button.setEnabled(True)

        elif index == 3:
            if self.use_fit_results_chbox.isChecked():
                self.use_fit_results_chbox.setEnabled(True)
                self.err_analysis_type_combox.setEnabled(True)
                self.label_20.setEnabled(False)
                self.opt_param_line.setEnabled(False)
                self.search_opt_param_file_button.setEnabled(False)
                if hasattr(self, 'fit_results_spc'):
                    self.err_analysis_type_combox.model().item(1).setEnabled(True)
                    if self.fit_data_type_combox.currentText() == 'Spectrum':
                        self.err_analysis_type_combox.setCurrentText('Spectrum fit')
                else:
                    self.err_analysis_type_combox.model().item(1).setEnabled(False)
                if hasattr(self, 'fit_results_timetrace'):
                    self.err_analysis_type_combox.model().item(2).setEnabled(True)
                    if self.fit_data_type_combox.currentText() == 'Time trace':
                        self.err_analysis_type_combox.setCurrentText('Time trace fit')
                else:
                    self.err_analysis_type_combox.model().item(2).setEnabled(False)
                self.err_analysis_type_combox.model().item(0).setEnabled(False)
            else:
                self.label_20.setEnabled(True)
                self.opt_param_line.setEnabled(True)
                self.search_opt_param_file_button.setEnabled(True)
                self.err_analysis_type_combox.setEnabled(False)
                self.err_analysis_type_combox.model().item(0).setEnabled(True)
                self.err_analysis_type_combox.setCurrentText('')

        elif index == 4:
            if self.g_selectivity_box.isChecked():
                self.label_68.setEnabled(True)
                self.magnetic_field_line.setEnabled(True)
                self.magnetic_field_line.setText("1.1984")
            else:
                self.label_68.setEnabled(False)
                self.magnetic_field_line.setEnabled(False)
                self.magnetic_field_line.setText("")

        elif index == 5:
            if self.fit_data_type_combox.currentText() == 'Spectrum':
                if hasattr(self, 'fit_results_spc'):
                    self.use_fit_results_chbox.setChecked(True)
                else:
                    self.use_fit_results_chbox.setChecked(False)
                    self.use_fit_results_chbox.setEnabled(False)
                    self.err_analysis_type_combox.setEnabled(False)
                    self.err_analysis_type_combox.setCurrentText('')


            elif self.fit_data_type_combox.currentText() == 'Time trace':
                if hasattr(self, 'fit_results_timetrace'):
                    self.use_fit_results_chbox.setChecked(True)
                else:
                    self.use_fit_results_chbox.setChecked(False)
                    self.use_fit_results_chbox.setEnabled(False)
                    self.err_analysis_type_combox.setEnabled(False)
                    self.err_analysis_type_combox.setCurrentText('')

    # this function changes the displayed simulation plot to match the entry in the sim_comboBox
    def sim_displayed_plot_changer(self):
        self.sim_plot_stackedWidget.setCurrentIndex(self.sim_plot_comboBox.currentIndex())

        if self.sim_plot_comboBox.currentIndex() == 0 and self.timetracepath_line.text():
            self.RMSD_label.setText(
                "The RMSD between the experimental and simulated timetrace is: %f" % self.simulation_results.RMSD_timetrace)
        elif self.sim_plot_comboBox.currentIndex() == 1 and self.spectrumpath_line.text():
            self.RMSD_label.setText(
                "The RMSD between the experimental and simulated spectrum is: %f" % self.simulation_results.RMSD_spectrum)
        else:
            self.RMSD_label.setText("")


    # this function deactivates a widget if its displayed plot is not selected in the simulation checkboxes, called in on_run_button_click
    def sim_checkbox_comboBox_connector(self):
        if self.sim_specvsT_chbox.isChecked():
            self.sim_plot_comboBox.model().item(5).setEnabled(True)
            self.sim_plot_comboBox.setCurrentIndex(5)
        else:
            self.sim_plot_comboBox.model().item(5).setEnabled(False)

        if self.sim_specvsxi_chbox.isChecked():
            self.sim_plot_comboBox.model().item(4).setEnabled(True)
            self.sim_plot_comboBox.setCurrentIndex(4)
        else:
            self.sim_plot_comboBox.model().item(4).setEnabled(False)

        if self.sim_specvsphi_chbox.isChecked():
            self.sim_plot_comboBox.model().item(3).setEnabled(True)
            self.sim_plot_comboBox.setCurrentIndex(3)
        else:
            self.sim_plot_comboBox.model().item(3).setEnabled(False)

        if self.sim_specvstheta_chbox.isChecked():
            self.sim_plot_comboBox.model().item(2).setEnabled(True)
            self.sim_plot_comboBox.setCurrentIndex(2)
        else:
            self.sim_plot_comboBox.model().item(2).setEnabled(False)

        if self.sim_spec_chbox.isChecked():
            self.sim_plot_comboBox.model().item(1).setEnabled(True)
            self.sim_plot_comboBox.setCurrentIndex(1)
        else:
            self.sim_plot_comboBox.model().item(1).setEnabled(False)

        if self.sim_timetr_chbox.isChecked():
            self.sim_plot_comboBox.model().item(0).setEnabled(True)
            self.sim_plot_comboBox.setCurrentIndex(0)
        else:
            self.sim_plot_comboBox.model().item(0).setEnabled(False)


    # this function disables a parameter selection in the error analysis table based on user selection of optimized parameters in fitting tab
    def err_analysis_parameter_table_displayer(self, parameter_index):
        fitting_param_widget_list = [self.r_mean_opt_chbox, self.r_width_opt_chbox, self.phi_mean_opt_chbox,
                                     self.phi_width_opt_chbox,
                                     self.xi_mean_opt_chbox, self.xi_width_opt_chbox, self.temp_opt_chbox]

        self.err_param_table_comboboxes = [self.err_param_110_cbox, self.err_param_111_cbox, self.err_param_120_cbox,
                                           self.err_param_121_cbox,
                                           self.err_param_130_cbox, self.err_param_131_cbox, self.err_param_140_cbox,
                                           self.err_param_141_cbox,
                                           self.err_param_210_cbox, self.err_param_211_cbox, self.err_param_220_cbox,
                                           self.err_param_221_cbox,
                                           self.err_param_230_cbox, self.err_param_231_cbox, self.err_param_240_cbox,
                                           self.err_param_241_cbox,
                                           self.err_param_310_cbox, self.err_param_311_cbox, self.err_param_320_cbox,
                                           self.err_param_321_cbox,
                                           self.err_param_330_cbox, self.err_param_331_cbox, self.err_param_340_cbox,
                                           self.err_param_341_cbox,
                                           self.err_param_410_cbox, self.err_param_411_cbox, self.err_param_420_cbox,
                                           self.err_param_421_cbox,
                                           self.err_param_430_cbox, self.err_param_431_cbox, self.err_param_440_cbox,
                                           self.err_param_441_cbox]

        if fitting_param_widget_list[parameter_index - 1].isChecked():
            for combobox in self.err_param_table_comboboxes:
                combobox.model().item(parameter_index).setEnabled(True)

        else:
            for combobox in self.err_param_table_comboboxes:
                combobox.model().item(parameter_index).setEnabled(False)
                if combobox.currentIndex() == parameter_index:
                    combobox.setCurrentIndex(0)


    def update_parameter_fit_output_table(self, index, best_parameters):

        # changes the output table based on user selection of the parameters that should be optimized
        if index == 0:
            if self.r_mean_opt_chbox.isChecked():
                self.r_mean_opt_label.setText("Yes")
            if self.r_width_opt_chbox.isChecked():
                self.r_width_opt_label.setText("Yes")
            if self.phi_mean_opt_chbox.isChecked():
                self.phi_mean_opt_label.setText("Yes")
            if self.phi_width_opt_chbox.isChecked():
                self.phi_width_opt_label.setText("Yes")
            if self.xi_mean_opt_chbox.isChecked():
                self.xi_mean_opt_label.setText("Yes")
            if self.xi_width_opt_chbox.isChecked():
                self.xi_width_opt_label.setText("Yes")
            if self.temp_opt_chbox.isChecked():
                self.temp_opt_label.setText("Yes")

        # updates the parameter table to display the results of error analysis as well as fill in the values in case they aren't filled in yet
        if index == 1:
            self.r_mean_fit_error_label.setText(str(round(best_parameters['r_mean']['precision'], 2)))
            self.r_width_error_label.setText(str(round(best_parameters['r_width']['precision'], 2)))
            self.phi_mean_error_label.setText(str(round(best_parameters['phi_mean']['precision'], 2)))
            self.phi_width_error_label.setText(str(round(best_parameters['phi_width']['precision'], 2)))
            self.xi_mean_error_label.setText(str(round(best_parameters['xi_mean']['precision'], 2)))
            self.xi_width_error_label.setText(str(round(best_parameters['xi_width']['precision'], 2)))
            self.temp_error_label.setText(str(round(best_parameters['xi_width']['precision'], 2)))
            index = 2
            self.fitting_tab.setTabEnabled(2, True)

        # updates the parameter table to display the reults of fitting
        if index == 2:
            pi = 3.14159
            self.r_mean_output_value.setText(str(round(best_parameters['r_mean']['value'], 2)))
            self.r_width_output_value.setText(str(round(best_parameters['r_width']['value'], 2)))
            self.phi_mean_output_value.setText(str(round(best_parameters['phi_mean']['value'] * 360 / (2 * pi), 2)))
            self.phi_width_output_value.setText(str(round(best_parameters['phi_width']['value'] * 360 / (2 * pi), 2)))
            self.xi_mean_output_value.setText(str(round(best_parameters['xi_mean']['value'] * 360 / (2 * pi), 2)))
            self.xi_width_output_value.setText(str(round(best_parameters['xi_width']['value'] * 360 / (2 * pi), 2)))
            self.temp_output_value.setText(str(round(best_parameters['temp']['value'], 2)))





if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.showMaximized()
    sys.exit(app.exec_())

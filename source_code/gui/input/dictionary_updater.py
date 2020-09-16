import numpy as np
import sys
sys.path.append('..')
from input.load_spectrum import load_spectrum
from input.load_timetrace import load_timetrace
from input.symmetric_boundaries import symmetric_boundaries
from input.load_optimized_parameters import load_optimized_parameters
from mathematics.find_max_on_interval import find_max_on_interval
from supplement.constants import const
from PyQt5.QtWidgets import QMessageBox


def dictionary_updater(self):

        self.do_not_proceed = 0
        def mode():
            if self.main_widget.currentIndex() == 1:
                self.mode['simulation'] = 1
                self.mode['fitting'] = 0
                self.mode['error_analysis'] = 0
            elif self.main_widget.currentIndex() == 2:
                self.mode['simulation'] = 0
                self.mode['fitting'] = 1
                self.mode['error_analysis'] = 0
            elif self.main_widget.currentIndex() == 3:
                self.mode['simulation'] = 0
                self.mode['fitting'] = 0
                self.mode['error_analysis'] = 1


        def exp_data():
            self.exp_data['path_spectrum'] = self.spectrumpath_line.text()
            self.exp_data['path_timetrace'] = self.timetracepath_line.text()
            if not (self.exp_data['path_spectrum'] == ""):
                f, spc = load_spectrum(self.exp_data['path_spectrum'])
                self.exp_data['f'], self.exp_data['spc'] = symmetric_boundaries(f, spc)
            #else statement to make sure that there is no experimental data if the user removes his exp data paths and reruns program
            else:
                self.exp_data['f'], self.exp_data['spc'] = [], []
            if not (self.exp_data['path_timetrace'] == ""):
                self.exp_data['t'], self.exp_data['sig'] = load_timetrace(self.exp_data['path_timetrace'])
            else:
                self.exp_data['t'], self.exp_data['sig'] = [], []

        def spin_system():
            if self.mode['simulation']:
                self.spinA['type'] = self.spinA_type_box.currentText()
                self.spinA['g'] = np.array([float(self.spinA_gxx_line.text()),float(self.spinA_gyy_line.text()), float(self.spinA_gzz_line.text())])

                self.spinB['type'] = self.spinB_type_box.currentText()
                self.spinB['g'] = np.array([float(self.spinB_gxx_line.text()), float(self.spinB_gyy_line.text()),
                                        float(self.spinB_gzz_line.text())])

            else:
                self.spinA['type'] = self.spinA_type_box_fit.currentText()
                self.spinA['g'] = np.array([float(self.spinA_gxx_line_fit.text()), float(self.spinA_gyy_line_fit.text()),float(self.spinA_gzz_line_fit.text())])

                self.spinB['type'] = self.spinB_type_box_fit.currentText()
                self.spinB['g'] = np.array([float(self.spinB_gxx_line_fit.text()), float(self.spinB_gyy_line_fit.text()),
                                        float(self.spinB_gzz_line_fit.text())])

        def simulation():
            self.sim_settings['modes']['spc'] = int(self.sim_spec_chbox.isChecked())
            self.sim_settings['modes']['timetrace'] = int(self.sim_timetr_chbox.isChecked())
            self.sim_settings['modes']['spc_vs_theta'] = int(self.sim_specvstheta_chbox.isChecked())
            self.sim_settings['modes']['spc_vs_xi'] = int(self.sim_specvsxi_chbox.isChecked())
            self.sim_settings['modes']['spc_vs_phi'] = int(self.sim_specvsphi_chbox.isChecked())
            self.sim_settings['modes']['spc_vs_temp'] = int(self.sim_specvsT_chbox.isChecked())

            self.sim_settings['parameters']['r_mean'] = float(self.sim_r_mean_line.text())
            self.sim_settings['parameters']['r_width'] = float(self.sim_r_width_line.text())
            self.sim_settings['parameters']['xi_mean'] = const['deg2rad'] * float(self.sim_xi_mean_line.text())
            self.sim_settings['parameters']['xi_width'] = const['deg2rad'] * float(self.sim_xi_width_line.text())
            self.sim_settings['parameters']['phi_mean'] = const['deg2rad'] * float(self.sim_phi_mean_line.text())
            self.sim_settings['parameters']['phi_width'] = const['deg2rad'] * float(self.sim_phi_width_line.text())
            self.sim_settings['parameters']['temp'] = float(self.sim_temp_line.text())

            self.sim_settings['settings']['mod_depth'] = float(self.sim_moddepth_line.text())
            if self.sim_settings['modes']['spc_vs_theta']:
                self.sim_settings['settings']['theta_bins'] = np.linspace(float(self.sim_theta_min_line.text()),
                                                                 float(self.sim_theta_max_line.text()),
                                                                 int(self.sim_theta_samples_line.text()))

            if self.sim_settings['modes']['spc_vs_phi']:
                self.sim_settings['settings']['phi_bins'] = np.linspace(float(self.sim_phi_min_line.text()),
                                                                     float(self.sim_phi_max_line.text()),
                                                                     int(self.sim_phi_samples_line.text()))

            if self.sim_settings['modes']['spc_vs_xi']:
                self.sim_settings['settings']['xi_bins'] = np.linspace(float(self.sim_xi_min_line.text()),
                                                                     float(self.sim_xi_max_line.text()),
                                                                     int(self.sim_xi_samples_line.text()))

            if self.sim_settings['modes']['spc_vs_temp']:
                self.sim_settings['settings']['temp_bins'] = np.linspace(float(self.sim_Tmin_line.text()),
                                                                     float(self.sim_Tmax_line.text()),
                                                                     int(self.sim_temp_samples_line.text()))

        def calc_settings():
            self.calc_settings['Ns'] = int(self.montecarlo_line.text())
            self.calc_settings['noise_std'] = float(self.noise_sd_line.text())
            self.calc_settings['r_distr'] = self.r_distr_box.currentText()
            self.calc_settings['phi_distr'] = self.phi_distr_box.currentText()
            self.calc_settings['xi_distr'] = self.xi_distr_box.currentText()
            self.calc_settings['f_min'] = float(self.minf_line.text())
            self.calc_settings['f_max'] = float(self.maxf_line.text())
            self.calc_settings['t_min'] = float(self.mintime_line.text())
            self.calc_settings['t_max'] = float(self.maxtime_line.text())
            self.calc_settings['g_selectivity'] = int(self.g_selectivity_box.isChecked())
            if self.g_selectivity_box.isChecked():
                self.calc_settings['magnetic_field'] = float(self.magnetic_field_line.text())

            try:
                self.exp_data['f'][0]
                if self.calc_settings['f_max']:
                    self.calc_settings['spc_max'] = find_max_on_interval(self.exp_data['spc'], self.exp_data['f'], self.calc_settings['f_min'],
                                                                    self.calc_settings['f_max'])
                else:
                    self.calc_settings['f_max'] = np.amax(self.exp_data['f'])
                    self.calc_settings['spc_max'] = find_max_on_interval(self.exp_data['spc'], self.exp_data['f'], self.calc_settings['f_min'],
                                                                    self.calc_settings['f_max'])
            except IndexError:
                self.calc_settings['spc_max'] = 1.0

        def read_fitting_parameters(fitting_param_dict):
            indices = {}
            bounds = []
            fixed = {}
            count = 0
            for name in const['variable_names']:
                vopt = fitting_param_dict[name][0]
                if vopt:
                    indices[name] = count
                    count += 1
                    vmin = fitting_param_dict[name][1] * const['variable_scales'][name]
                    vmax = fitting_param_dict[name][2] * const['variable_scales'][name]
                    bounds.append([vmin, vmax])
                else:
                    indices[name] = -1
                    fixed[name] = fitting_param_dict[name][3] * const['variable_scales'][name]
            return [indices, bounds, fixed, count]

        def fitting():
            if self.fit_data_type_combox.currentText() == 'Spectrum':
                self.fit_settings['settings']['fitted_data'] = 'spectrum'
            elif self.fit_data_type_combox.currentText() == 'Time trace':
                self.fit_settings['settings']['fitted_data'] = 'timetrace'

            #creating a dictionary that can be used in a slightly modified version of read_config.read_fitting_parameters
            fitting_param_dict = {}
            for name in const['variable_names']:
                fitting_param_dict['name'] = {}
            fitting_param_dict['r_mean'] = [int(self.r_mean_opt_chbox.isChecked()), float(self.r_mean_fit_lbound_line.text()),
                                            float(self.r_mean_fit_ubound_line.text())]
            if self.r_mean_fit_input_value.text():
                fitting_param_dict['r_mean'].append(float(self.r_mean_fit_input_value.text()))

            fitting_param_dict['r_width'] = [int(self.r_width_opt_chbox.isChecked()),
                                            float(self.r_width_fit_lbound_line.text()),
                                            float(self.r_width_fit_ubound_line.text())]
            if self.r_width_fit_input_value.text():
                fitting_param_dict['r_width'].append(float(self.r_width_fit_input_value.text()))

            fitting_param_dict['phi_mean'] = [int(self.phi_mean_opt_chbox.isChecked()),
                                            float(self.phi_mean_fit_lbound_line.text()),
                                            float(self.phi_mean_fit_ubound_line.text())]
            if self.phi_mean_fit_input_value.text():
                fitting_param_dict['phi_mean'].append(float(self.phi_mean_fit_input_value.text()))

            fitting_param_dict['phi_width'] = [int(self.phi_width_opt_chbox.isChecked()),
                                              float(self.phi_width_fit_lbound_line.text()),
                                              float(self.phi_width_fit_ubound_line.text())]
            if self.phi_width_fit_input_value.text():
                fitting_param_dict['phi_width'].append(float(self.phi_width_fit_input_value.text()))

            fitting_param_dict['xi_mean'] = [int(self.xi_mean_opt_chbox.isChecked()),
                                              float(self.xi_mean_fit_lbound_line.text()),
                                              float(self.xi_mean_fit_ubound_line.text())]
            if self.xi_mean_fit_input_value.text():
                fitting_param_dict['xi_mean'].append(float(self.xi_mean_fit_input_value.text()))

            fitting_param_dict['xi_width'] = [int(self.xi_width_opt_chbox.isChecked()),
                                               float(self.xi_width_fit_lbound_line.text()),
                                               float(self.xi_width_fit_ubound_line.text())]
            if self.xi_width_fit_input_value.text():
                fitting_param_dict['xi_width'].append(float(self.xi_width_fit_input_value.text()))

            fitting_param_dict['temp'] = [int(self.temp_opt_chbox.isChecked()), float(self.temp_fit_lbound_line.text()),
                                          float(self.temp_fit_ubound_line.text())]
            if self.temp_fit_input_value.text():
                fitting_param_dict['temp'].append(float(self.temp_fit_input_value.text()))

            self.fit_settings['parameters']['indices'], self.fit_settings['parameters']['bounds'], self.fit_settings['parameters']['fixed'], self.fit_settings['parameters']['size'] = read_fitting_parameters(fitting_param_dict)


        def error_analysis_settings():

            self.err_settings = {}
            self.err_settings['Ns'] = int(self.number_of_points_line.text())
            self.err_settings['confidence_interval'] = float(self.confidence_interval_line.text())

            if self.use_fit_results_chbox.isChecked():
                if self.err_analysis_type_combox.currentText() == 'Spectrum fit':
                    self.err_settings['optimized_parameters'] = self.fit_results_spc.best_parameters
                    if self.mode['error_analysis']:
                        self.fit_settings['settings']['fitted_data'] = 'spectrum'
                elif self.err_analysis_type_combox.currentText() == 'Time trace fit':
                    self.err_settings['optimized_parameters'] = self.fit_results_timetrace.best_parameters
                    if self.mode['error_analysis']:
                        self.fit_settings['settings']['fitted_data'] = 'timetrace'
            else:
                if not (self.opt_param_line.text() == "") and (self.mode['error_analysis']):
                    self.err_settings['optimized_parameters'] = load_optimized_parameters(self.opt_param_line.text())

                elif (self.opt_param_line.text() == "") and (self.mode['error_analysis']):
                    messagebox = QMessageBox()
                    messagebox.setText(
                        "You did not enter a path to a file of optimized parameters for error analysis.")
                    messagebox.setStandardButtons(QMessageBox.Ok)
                    messagebox.setIcon(QMessageBox.Warning)
                    messagebox.exec()
                    self.do_not_proceed = 1
                    self.deactivate_widgets(1)
            #I probably made this much more complicated than necessary..
            self.err_settings['variables'] = []
            parameter_list = ['r_mean', 'r_width', 'phi_mean', 'phi_width', 'xi_mean', 'xi_width', 'temp']
            i = 0
            there_is_a_nested_list_already = 0

            for combobox in self.err_param_table_comboboxes:
                if combobox.currentIndex():
                    if not there_is_a_nested_list_already:
                        self.err_settings['variables'].append([])
                        there_is_a_nested_list_already = 1
                    self.err_settings['variables'][len(self.err_settings['variables'])-1].append(parameter_list[combobox.currentIndex() -1])
                if i == 1:
                    i = 0
                    there_is_a_nested_list_already = 0
                else:
                    i += 1
            for j in range(len(self.err_settings['variables'])):
                self.err_settings['variables'][j] = tuple(self.err_settings['variables'][j])
            self.err_settings['variables'] = tuple(self.err_settings['variables'])

        mode()
        exp_data()
        spin_system()
        simulation()
        calc_settings()
        fitting()
        error_analysis_settings()

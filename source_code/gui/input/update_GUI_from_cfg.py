import libconf
import io
from PyQt5 import QtWidgets
import sys
import traceback

def update_GUI_from_cfg(self):

    def update_general_tab():

        self.spectrumpath_line.setText(config.path_spectrum)
        self.timetracepath_line.setText(config.path_timetrace)

        self.montecarlo_line.setText(str(config.calculation_settings.Ns))
        self.noise_sd_line.setText(str(config.calculation_settings.noise_std))
        self.minf_line.setText(str(config.calculation_settings.fmin))
        self.maxf_line.setText(str(config.calculation_settings.fmax))
        self.mintime_line.setText(str(config.calculation_settings.tmin))
        self.maxtime_line.setText(str(config.calculation_settings.tmax))
        if config.calculation_settings.g_selectivity:
            self.g_selectivity_box.setChecked(True)
            self.magnetic_field_line.setText(str(config.calculation_settings.magnetic_field))
        else:
            self.g_selectivity_box.setChecked(False)

    def update_simulation_tab():

        if config.simulation_modes.timetrace:
            self.sim_timetr_chbox.setChecked(True)
        else:
            self.sim_timetr_chbox.setChecked(False)

        if config.simulation_modes.spc:
            self.sim_spec_chbox.setChecked(True)
        else:
            self.sim_spec_chbox.setChecked(False)

        if config.simulation_modes.spc_vs_theta:
            self.sim_specvstheta_chbox.setChecked(True)
        else:
            self.sim_specvstheta_chbox.setChecked(False)

        if config.simulation_modes.spc_vs_phi:
            self.sim_specvsphi_chbox.setChecked(True)
        else:
            self.sim_specvsphi_chbox.setChecked(False)

        if config.simulation_modes.spc_vs_xi:
            self.sim_specvsxi_chbox.setChecked(True)
        else:
            self.sim_specvsxi_chbox.setChecked(False)

        if config.simulation_modes.spc_vs_temp:
            self.sim_specvsT_chbox.setChecked(True)
        else:
            self.sim_specvsT_chbox.setChecked(False)

        if config.calculation_settings.r_distr == "normal":
            self.r_distr_box.setCurrentIndex(0)
            self.r_distr_fit_combox.setCurrentIndex(0)
        elif config.calculation_settings.r_distr == "uniform":
            self.r_distr_box.setCurrentIndex(1)
            self.r_distr_fit_combox.setCurrentIndex(1)
        if config.calculation_settings.phi_distr == "normal":
            self.phi_distr_box.setCurrentIndex(0)
            self.phi_distr_fit_combox.setCurrentIndex(0)
        elif config.calculation_settings.phi_distr == "uniform":
            self.phi_distr_box.setCurrentIndex(1)
            self.phi_distr_fit_combox.setCurrentIndex(1)

        if config.calculation_settings.xi_distr == "normal":
            self.xi_distr_box.setCurrentIndex(0)
            self.xi_distr_fit_combox.setCurrentIndex(0)
        elif config.calculation_settings.xi_distr == "uniform":
            self.xi_distr_box.setCurrentIndex(1)
            self.xi_distr_fit_combox.setCurrentIndex(1)

        self.sim_r_mean_line.setText(str(config.simulation_parameters.r_mean))
        self.sim_phi_mean_line.setText(str(config.simulation_parameters.phi_mean))
        self.sim_xi_mean_line.setText(str(config.simulation_parameters.xi_mean))

        self.sim_r_width_line.setText(str(config.simulation_parameters.r_width))
        self.sim_phi_width_line.setText(str(config.simulation_parameters.phi_width))
        self.sim_xi_width_line.setText(str(config.simulation_parameters.xi_width))

        self.sim_temp_line.setText(str(config.simulation_parameters.temp))
        self.sim_moddepth_line.setText(str(config.simulation_settings.mod_depth))

        self.sim_theta_min_line.setText(str(config.simulation_settings.theta_ranges[0]))
        self.sim_phi_min_line.setText(str(config.simulation_settings.phi_ranges[0]))
        self.sim_xi_min_line.setText(str(config.simulation_settings.xi_ranges[0]))
        self.sim_Tmin_line.setText(str(config.simulation_settings.temp_ranges[0]))

        self.sim_theta_max_line.setText(str(config.simulation_settings.theta_ranges[1]))
        self.sim_phi_max_line.setText(str(config.simulation_settings.phi_ranges[1]))
        self.sim_xi_max_line.setText(str(config.simulation_settings.xi_ranges[1]))
        self.sim_Tmax_line.setText(str(config.simulation_settings.temp_ranges[1]))

        self.sim_theta_samples_line.setText(str(int(config.simulation_settings.theta_ranges[2])))
        self.sim_phi_samples_line.setText(str(int(config.simulation_settings.phi_ranges[2])))
        self.sim_xi_samples_line.setText(str(int((config.simulation_settings.xi_ranges[2]))))
        self.sim_temp_samples_line.setText(str(int(config.simulation_settings.temp_ranges[2])))

        if config.spinB.type == "anisotropic":
            self.spinB_type_box.setCurrentIndex(0)
        elif config.calculation_settings.xi_distr == "isotropic":
            self.spinB_type_box.setCurrentIndex(1)

        self.spinB_gxx_line.setText(str(config.spinB.g[0]))
        self.spinB_gyy_line.setText(str(config.spinB.g[1]))
        self.spinB_gzz_line.setText(str(config.spinB.g[2]))

        self.spinA_gxx_line.setText(str(config.spinA.g[0]))
        self.spinA_gyy_line.setText(str(config.spinA.g[1]))
        self.spinA_gzz_line.setText(str(config.spinA.g[2]))

    def update_fitting_tab():
        try:
            config.fitting_settings
        except AttributeError:
            return None
        if config.fitting_settings.fitted_data == "spectrum":
            self.fit_data_type_combox.setCurrentIndex(0)
        elif config.fitting_settings.fitted_data == "timetrace":
            self.fit_data_type_combox.setCurrentIndex(1)

        self.fit_settings['settings']['num_generations'] = int(config.fitting_settings.num_generations)
        self.fit_settings['settings']['size_generation'] = int(config.fitting_settings.size_generation)
        self.fit_settings['settings']['prob_crossover'] = float(config.fitting_settings.prob_crossover)
        self.fit_settings['settings']['prob_mutation'] = float(config.fitting_settings.prob_mutation)

        if config.fitting_parameters.r_mean.opt:
            self.r_mean_opt_chbox.setChecked(True)
        else:
            self.r_mean_opt_chbox.setChecked(False)

        if config.fitting_parameters.r_width.opt:
            self.r_width_opt_chbox.setChecked(True)
        else:
            self.r_width_opt_chbox.setChecked(False)

        if config.fitting_parameters.phi_mean.opt:
            self.phi_mean_opt_chbox.setChecked(True)
        else:
            self.phi_mean_opt_chbox.setChecked(False)

        if config.fitting_parameters.phi_width.opt:
            self.phi_width_opt_chbox.setChecked(True)
        else:
            self.phi_width_opt_chbox.setChecked(False)

        if config.fitting_parameters.xi_mean.opt:
            self.xi_mean_opt_chbox.setChecked(True)
        else:
            self.xi_mean_opt_chbox.setChecked(False)

        if config.fitting_parameters.xi_width.opt:
            self.xi_width_opt_chbox.setChecked(True)
        else:
            self.xi_width_opt_chbox.setChecked(False)

        if config.fitting_parameters.temp.opt:
            self.temp_opt_chbox.setChecked(True)
        else:
            self.temp_opt_chbox.setChecked(False)

        self.r_mean_fit_lbound_line.setText(str(config.fitting_parameters.r_mean.range[0]))
        self.r_width_fit_lbound_line.setText(str(config.fitting_parameters.r_width.range[0]))
        self.phi_mean_fit_lbound_line.setText(str(config.fitting_parameters.phi_mean.range[0]))
        self.phi_width_fit_lbound_line.setText(str(config.fitting_parameters.phi_width.range[0]))
        self.xi_mean_fit_lbound_line.setText(str(config.fitting_parameters.xi_mean.range[0]))
        self.xi_width_fit_lbound_line.setText(str(config.fitting_parameters.xi_width.range[0]))
        self.temp_fit_lbound_line.setText(str(config.fitting_parameters.temp.range[0]))

        self.r_mean_fit_ubound_line.setText(str(config.fitting_parameters.r_mean.range[1]))
        self.r_width_fit_ubound_line.setText(str(config.fitting_parameters.r_width.range[1]))
        self.phi_mean_fit_ubound_line.setText(str(config.fitting_parameters.phi_mean.range[1]))
        self.phi_width_fit_ubound_line.setText(str(config.fitting_parameters.phi_width.range[1]))
        self.xi_mean_fit_ubound_line.setText(str(config.fitting_parameters.xi_mean.range[1]))
        self.xi_width_fit_ubound_line.setText(str(config.fitting_parameters.xi_width.range[1]))
        self.temp_fit_ubound_line.setText(str(config.fitting_parameters.temp.range[1]))

        self.r_mean_fit_input_value.setText(str(config.fitting_parameters.r_mean.value))
        self.r_width_fit_input_value.setText(str(config.fitting_parameters.r_width.value))
        self.phi_mean_fit_input_value.setText(str(config.fitting_parameters.phi_mean.value))
        self.phi_width_fit_input_value.setText(str(config.fitting_parameters.phi_width.value))
        self.xi_mean_fit_input_value.setText(str(config.fitting_parameters.xi_mean.value))
        self.xi_width_fit_input_value.setText(str(config.fitting_parameters.xi_width.value))
        self.temp_fit_input_value.setText(str(config.fitting_parameters.temp.value))

        if config.spinB.type == "anisotropic":
            self.spinB_type_box_fit.setCurrentIndex(0)
        elif config.calculation_settings.xi_distr == "isotropic":
            self.spinB_type_box_fit.setCurrentIndex(1)

        self.spinB_gxx_line_fit.setText(str(config.spinB.g[0]))
        self.spinB_gyy_line_fit.setText(str(config.spinB.g[1]))
        self.spinB_gzz_line_fit.setText(str(config.spinB.g[2]))

        self.spinA_gxx_line_fit.setText(str(config.spinA.g[0]))
        self.spinA_gyy_line_fit.setText(str(config.spinA.g[1]))
        self.spinA_gzz_line_fit.setText(str(config.spinA.g[2]))


    def update_error_analysis_tab():
        try:
            config.error_analysis
        except AttributeError:
            return None
        self.opt_param_line.setText(config.error_analysis.path_optimized_parameters)
        self.number_of_points_line.setText(str(config.error_analysis.Ns))
        self.confidence_interval_line.setText(str(config.error_analysis.confidence_interval))
        parameter_list = ['r_mean', 'r_width', 'phi_mean', 'phi_width', 'xi_mean', 'xi_width', 'temp']

        for combobox in self.err_param_table_comboboxes:
            combobox.setCurrentIndex(0)

        parameter_pair_number = 0
        j = 0
        combobox_number = 0
        while parameter_pair_number < len(config.error_analysis.variables):

            #try except for when there is only one parameter in a pair
            try:
                parameter = config.error_analysis.variables[parameter_pair_number][j]
                index = parameter_list.index(parameter) + 1
                self.err_param_table_comboboxes[combobox_number].setCurrentIndex(index)


            except IndexError:
                self.err_param_table_comboboxes[combobox_number].setCurrentIndex(0)


            combobox_number +=1
            if j == 1:
                j = 0
                parameter_pair_number += 1

            else:
                j += 1



    self.filedialog = QtWidgets.QFileDialog()
    filepath = self.filedialog.getOpenFileName(self.centralwidget, 'Load settings from .cfg file',"", "( *.cfg)")[0]
    if filepath == "":
        return None
    with io.open(filepath) as f:
        config = libconf.load(f)

        update_general_tab()

        self.load_timetrace_path(1)
        self.load_spectrum_path(1)

        update_simulation_tab()
        update_fitting_tab()
        update_error_analysis_tab()





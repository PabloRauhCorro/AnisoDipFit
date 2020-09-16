import libconf
import sys
from PyQt5.QtWidgets import QFileDialog

def dict_for_cfg(self):
    config_settings = {}
    if self.mode['simulation']:
        config_settings['mode'] = 0
    elif self.mode['fitting']:
        config_settings['mode'] = 1
    elif self.mode['error_analysis']:
        config_settings['mode'] = 2


    config_settings['path_spectrum'] = self.exp_data['path_spectrum']
    config_settings['path_timetrace'] = self.exp_data['path_timetrace']
    config_settings['spinA'] = {}
    config_settings['spinA']['type'] = self.spinA['type']
    config_settings['spinA']['g'] = self.spinA['g'].tolist()
    config_settings['spinB'] = {}
    config_settings['spinB']['type'] = self.spinB['type']
    config_settings['spinB']['g'] = self.spinB['g'].tolist()

    config_settings['simulation_modes'] = {}
    config_settings['simulation_modes']['spc'] = self.sim_settings['modes']['spc']
    config_settings['simulation_modes']['timetrace'] = self.sim_settings['modes']['timetrace']
    config_settings['simulation_modes']['spc_vs_theta'] = self.sim_settings['modes']['spc_vs_theta']
    config_settings['simulation_modes']['spc_vs_xi'] = self.sim_settings['modes']['spc_vs_xi']
    config_settings['simulation_modes']['spc_vs_phi'] = self.sim_settings['modes']['spc_vs_phi']
    config_settings['simulation_modes']['spc_vs_temp'] = self.sim_settings['modes']['spc_vs_temp']

    config_settings['simulation_parameters'] = {}
    config_settings['simulation_parameters']['r_mean'] = self.sim_settings['parameters']['r_mean']
    config_settings['simulation_parameters']['r_width'] = self.sim_settings['parameters']['r_width']
    config_settings['simulation_parameters']['xi_mean'] = float(self.sim_xi_mean_line.text())
    config_settings['simulation_parameters']['xi_width'] = float(self.sim_xi_width_line.text())
    config_settings['simulation_parameters']['phi_mean'] = float(self.sim_phi_mean_line.text())
    config_settings['simulation_parameters']['phi_width'] = float(self.sim_phi_width_line.text())
    config_settings['simulation_parameters']['temp'] = self.sim_settings['parameters']['temp']

    config_settings['simulation_settings'] = {}

    config_settings['simulation_settings']['theta_ranges'] = [float(self.sim_theta_min_line.text()),
                                                              float(self.sim_theta_max_line.text()),
                                                              float(self.sim_theta_samples_line.text())]
    config_settings['simulation_settings']['phi_ranges'] = [float(self.sim_phi_min_line.text()),
                                                            float(self.sim_phi_max_line.text()),
                                                            float(self.sim_phi_samples_line.text())]
    config_settings['simulation_settings']['xi_ranges'] = [float(self.sim_xi_min_line.text()),
                                                           float(self.sim_xi_max_line.text()),
                                                           float(self.sim_xi_samples_line.text())]
    config_settings['simulation_settings']['temp_ranges'] = [float(self.sim_Tmin_line.text()),
                                                             float(self.sim_Tmax_line.text()),
                                                             float(self.sim_temp_samples_line.text())]



    config_settings['simulation_settings']['mod_depth'] = self.sim_settings['settings']['mod_depth']
    config_settings['simulation_settings']['plot_3d'] = self.sim_settings['settings']['plot_3d']
    config_settings['simulation_settings']['faxis_normalized'] = self.sim_settings['settings']['faxis_normalized']

    config_settings['fitting_parameters'] = {}

    config_settings['fitting_parameters']['r_mean'] = {}
    config_settings['fitting_parameters']['r_mean']['opt'] = int(self.r_mean_opt_chbox.isChecked())
    config_settings['fitting_parameters']['r_mean']['range'] = [float(self.r_mean_fit_lbound_line.text()),
                                                                float(self.r_mean_fit_ubound_line.text())]
    if self.r_mean_fit_input_value.text():
        config_settings['fitting_parameters']['r_mean']['value'] = float(self.r_mean_fit_input_value.text())


    config_settings['fitting_parameters']['r_width'] = {}
    config_settings['fitting_parameters']['r_width']['opt'] = int(self.r_width_opt_chbox.isChecked())
    config_settings['fitting_parameters']['r_width']['range'] = [float(self.r_width_fit_lbound_line.text()),
                                                                float(self.r_width_fit_ubound_line.text())]
    if self.r_width_fit_input_value.text():
        config_settings['fitting_parameters']['r_width']['value'] = float(self.r_width_fit_input_value.text())


    config_settings['fitting_parameters']['xi_mean'] = {}
    config_settings['fitting_parameters']['xi_mean']['opt'] = int(self.xi_mean_opt_chbox.isChecked())
    config_settings['fitting_parameters']['xi_mean']['range'] = [float(self.xi_mean_fit_lbound_line.text()),
                                                                float(self.xi_mean_fit_ubound_line.text())]
    if self.xi_mean_fit_input_value.text():
        config_settings['fitting_parameters']['xi_mean']['value'] = float(self.xi_mean_fit_input_value.text())


    config_settings['fitting_parameters']['xi_width'] = {}
    config_settings['fitting_parameters']['xi_width']['opt'] = int(self.xi_width_opt_chbox.isChecked())
    config_settings['fitting_parameters']['xi_width']['range'] = [float(self.xi_width_fit_lbound_line.text()),
                                                                 float(self.xi_width_fit_ubound_line.text())]
    if self.xi_width_fit_input_value.text():
        config_settings['fitting_parameters']['xi_width']['value'] = float(self.xi_width_fit_input_value.text())


    config_settings['fitting_parameters']['phi_mean'] = {}
    config_settings['fitting_parameters']['phi_mean']['opt'] = int(self.phi_mean_opt_chbox.isChecked())
    config_settings['fitting_parameters']['phi_mean']['range'] = [float(self.phi_mean_fit_lbound_line.text()),
                                                                 float(self.phi_mean_fit_ubound_line.text())]
    if self.phi_mean_fit_input_value.text():
        config_settings['fitting_parameters']['phi_mean']['value'] = float(self.phi_mean_fit_input_value.text())


    config_settings['fitting_parameters']['phi_width'] = {}
    config_settings['fitting_parameters']['phi_width']['opt'] = int(self.phi_width_opt_chbox.isChecked())
    config_settings['fitting_parameters']['phi_width']['range'] = [float(self.phi_width_fit_lbound_line.text()),
                                                                  float(self.phi_width_fit_ubound_line.text())]
    if self.phi_width_fit_input_value.text():
        config_settings['fitting_parameters']['phi_width']['value'] = float(self.phi_width_fit_input_value.text())


    config_settings['fitting_parameters']['temp'] = {}
    config_settings['fitting_parameters']['temp']['opt'] = int(self.temp_opt_chbox.isChecked())
    config_settings['fitting_parameters']['temp']['range'] = [float(self.temp_fit_lbound_line.text()),
                                                                   float(self.temp_fit_ubound_line.text())]
    if self.temp_fit_input_value.text():
        config_settings['fitting_parameters']['temp']['value'] = float(self.temp_fit_input_value.text())





    config_settings['fitting_settings'] = {}
    config_settings['fitting_settings']['fitted_data'] = self.fit_settings['settings']['fitted_data']
    config_settings['fitting_settings']['method'] = self.fit_settings['settings']['method']
    config_settings['fitting_settings']['num_generations'] = self.fit_settings['settings']['num_generations']
    config_settings['fitting_settings']['size_generation'] = self.fit_settings['settings']['size_generation']
    config_settings['fitting_settings']['prob_crossover'] = self.fit_settings['settings']['prob_crossover']
    config_settings['fitting_settings']['prob_mutation'] = self.fit_settings['settings']['prob_mutation']


    config_settings['error_analysis'] = {}
    config_settings['error_analysis']['path_optimized_parameters'] = self.opt_param_line.text()
    config_settings['error_analysis']['Ns'] = self.err_settings['Ns']
    config_settings['error_analysis']['confidence_interval'] = self.err_settings['confidence_interval']
    config_settings['error_analysis']['variables'] = self.err_settings['variables']



    config_settings['calculation_settings'] = {}
    config_settings['calculation_settings']['Ns'] = self.calc_settings['Ns']
    config_settings['calculation_settings']['noise_std'] = self.calc_settings['noise_std']
    config_settings['calculation_settings']['r_distr'] = self.calc_settings['r_distr']
    config_settings['calculation_settings']['xi_distr'] = self.calc_settings['xi_distr']
    config_settings['calculation_settings']['phi_distr'] = self.calc_settings['phi_distr']
    config_settings['calculation_settings']['fmin'] = self.calc_settings['f_min']
    config_settings['calculation_settings']['fmax'] = self.calc_settings['f_max']
    config_settings['calculation_settings']['tmin'] = self.calc_settings['t_min']
    config_settings['calculation_settings']['tmax'] = self.calc_settings['t_max']
    config_settings['calculation_settings']['g_selectivity'] = self.calc_settings['g_selectivity']
    if self.calc_settings['g_selectivity']:
        config_settings['calculation_settings']['magnetic_field'] = self.calc_settings['magnetic_field']

    return config_settings


# optional argument open_file_dialog because a cfg file is created when saving results and there should not be another filedialog popping up
def create_cfg_file(self, MainWindow, open_file_dialog=True, filepath="" ):

    if open_file_dialog:
        self.filedialog = QFileDialog()
        filepath = self.filedialog.getSaveFileName(MainWindow, 'Save settings as .cfg file', "AnisoDipFit_settings",
                                                       "( *.cfg)")[0]
    self.dictionary_updater()
    config_settings = self.dict_for_cfg()
    if filepath:
        if not open_file_dialog:
            filepath += "/AnisoDipFit_settings.cfg"
        with open(filepath, 'w') as f:
            libconf.dump(config_settings, f)
        self.statusbar_adder("The configuration file has been saved.")

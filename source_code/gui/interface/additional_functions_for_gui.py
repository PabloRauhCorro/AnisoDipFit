


#this function deactivates or activates widgets and buttons
def deactivate_widgets(self, index = 0):
    #these things need to be done right after launching the program
    if index == 0:
        self.tab_param_sub.setTabEnabled(2, False)
        self.stop_button.setEnabled(False)
        self.fitting_tab.setTabEnabled(2, False)
        self.err_analysis_parameter_table_displayer(7)
        self.tab_error_analysis.setTabEnabled(1, False)
        self.tab_error_analysis.setTabEnabled(2, False)
        self.use_fit_results_chbox.setEnabled(False)

    elif index == 1:
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    elif index == 2:
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    elif index == 3:
        if self.use_fit_results_chbox.isChecked():
            self.label_20.setEnabled(False)
            self.opt_param_line.setEnabled(False)
            self.search_opt_param_file_button.setEnabled(False)
        else:
            self.label_20.setEnabled(True)
            self.opt_param_line.setEnabled(True)
            self.search_opt_param_file_button.setEnabled(True)


#this function changes the displayed simulation plot to match the entry in the sim_comboBox
def sim_displayed_plot_changer(self):
    self.sim_plot_stackedWidget.setCurrentIndex(self.sim_plot_comboBox.currentIndex())

    if self.sim_plot_comboBox.currentIndex() == 0 and self.timetracepath_line.text():
        self.RMSD_label.setText("The RMSD between the experimental and simulated timetrace is: %f" % self.simulation_results.RMSD_timetrace)
    elif self.sim_plot_comboBox.currentIndex() == 1 and self.spectrumpath_line.text():
        self.RMSD_label.setText("The RMSD between the experimental and simulated spectrum is: %f" % self.simulation_results.RMSD_spectrum)
    else:
        self.RMSD_label.setText("")


#this function disables a parameter selection in the error analysis table based on user selection of optimized parameters in fitting tab
def err_analysis_parameter_table_displayer(self, parameter_index):
    fitting_param_widget_list = [self.r_mean_opt_chbox, self.r_width_opt_chbox, self.phi_mean_opt_chbox, self.phi_width_opt_chbox,
                                 self.xi_mean_opt_chbox, self.xi_width_opt_chbox, self.temp_opt_chbox]

    self.err_param_table_comboboxes = [self.err_param_110_cbox, self.err_param_111_cbox, self.err_param_120_cbox, self.err_param_121_cbox,
                               self.err_param_130_cbox, self.err_param_131_cbox, self.err_param_140_cbox, self.err_param_141_cbox,
                               self.err_param_210_cbox, self.err_param_211_cbox, self.err_param_220_cbox, self.err_param_221_cbox,
                               self.err_param_230_cbox, self.err_param_231_cbox, self.err_param_240_cbox, self.err_param_241_cbox,
                               self.err_param_310_cbox, self.err_param_311_cbox, self.err_param_320_cbox, self.err_param_321_cbox,
                               self.err_param_330_cbox, self.err_param_331_cbox, self.err_param_340_cbox, self.err_param_341_cbox,
                               self.err_param_410_cbox, self.err_param_411_cbox, self.err_param_420_cbox, self.err_param_421_cbox,
                               self.err_param_430_cbox, self.err_param_431_cbox, self.err_param_440_cbox, self.err_param_441_cbox]

    if fitting_param_widget_list[parameter_index-1].isChecked():
        for combobox in self.err_param_table_comboboxes:
            combobox.model().item(parameter_index).setEnabled(True)

    else:
        for combobox in self.err_param_table_comboboxes:
            combobox.model().item(parameter_index).setEnabled(False)
            if combobox.currentIndex() == parameter_index:
                combobox.setCurrentIndex(0)


#this function deactivates a widget if its displayed plot is not selected in the simulation checkboxes, called in on_run_button_click
def sim_checkbox_comboBox_connector(self):
    if  self.sim_specvsT_chbox.isChecked():
        self.sim_plot_comboBox.model().item(5).setEnabled(True)
        self.sim_plot_comboBox.setCurrentIndex(5)
    else:
        self.sim_plot_comboBox.model().item(5).setEnabled(False)

    if  self.sim_specvsxi_chbox.isChecked():
        self.sim_plot_comboBox.model().item(4).setEnabled(True)
        self.sim_plot_comboBox.setCurrentIndex(4)
    else:
        self.sim_plot_comboBox.model().item(4).setEnabled(False)

    if  self.sim_specvsphi_chbox.isChecked():
        self.sim_plot_comboBox.model().item(3).setEnabled(True)
        self.sim_plot_comboBox.setCurrentIndex(3)
    else:
        self.sim_plot_comboBox.model().item(3).setEnabled(False)

    if  self.sim_specvstheta_chbox.isChecked():
        self.sim_plot_comboBox.model().item(2).setEnabled(True)
        self.sim_plot_comboBox.setCurrentIndex(2)
    else:
        self.sim_plot_comboBox.model().item(2).setEnabled(False)

    if  self.sim_spec_chbox.isChecked():
        self.sim_plot_comboBox.model().item(1).setEnabled(True)
        self.sim_plot_comboBox.setCurrentIndex(1)
    else:
        self.sim_plot_comboBox.model().item(1).setEnabled(False)

    if  self.sim_timetr_chbox.isChecked():
        self.sim_plot_comboBox.model().item(0).setEnabled(True)
        self.sim_plot_comboBox.setCurrentIndex(0)
    else:
        self.sim_plot_comboBox.model().item(0).setEnabled(False)


def update_parameter_fit_output_table(self, index, best_parameters):

    #changes the output table based on user selection of the parameters that should be optimized
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

    #updates the parameter table to display the results of error analysis as well as fill in the values in case they aren't filled in yet
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

    #updates the parameter table to display the reults of fitting
    if index == 2:
        pi = 3.14159
        self.r_mean_output_value.setText(str(round(best_parameters['r_mean']['value'], 2)))
        self.r_width_output_value.setText(str(round(best_parameters['r_width']['value'], 2)))
        self.phi_mean_output_value.setText(str(round(best_parameters['phi_mean']['value'] * 360/(2*pi), 2)) )
        self.phi_width_output_value.setText(str(round(best_parameters['phi_width']['value'] * 360/(2*pi), 2)) )
        self.xi_mean_output_value.setText(str(round(best_parameters['xi_mean']['value'] * 360/(2*pi), 2)) )
        self.xi_width_output_value.setText(str(round(best_parameters['xi_width']['value'] * 360/(2*pi), 2)) )
        self.temp_output_value.setText(str(round(best_parameters['temp']['value'], 2)))
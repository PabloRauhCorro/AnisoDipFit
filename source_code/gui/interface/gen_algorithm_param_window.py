# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gen_algorithm_param_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Gen_Algorithm_Parameter_Window(object):
    def __init__(self, generation_number, generation_size, prob_crossover, prob_mutation):
        self.generation_number = generation_number
        self.generation_size = generation_size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(475, 381)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.chromo_number_line = QtWidgets.QLineEdit(Dialog)
        self.chromo_number_line.setAlignment(QtCore.Qt.AlignCenter)
        self.chromo_number_line.setObjectName("chromo_number_line")
        self.gridLayout.addWidget(self.chromo_number_line, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.crossover_rate_line = QtWidgets.QLineEdit(Dialog)
        self.crossover_rate_line.setAlignment(QtCore.Qt.AlignCenter)
        self.crossover_rate_line.setObjectName("crossover_rate_line")
        self.gridLayout.addWidget(self.crossover_rate_line, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 8, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 7, 1, 1, 1)
        self.gen_number_line = QtWidgets.QLineEdit(Dialog)
        self.gen_number_line.setAlignment(QtCore.Qt.AlignCenter)
        self.gen_number_line.setObjectName("gen_number_line")
        self.gridLayout.addWidget(self.gen_number_line, 1, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 6, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.mutation_rate_line = QtWidgets.QLineEdit(Dialog)
        self.mutation_rate_line.setAlignment(QtCore.Qt.AlignCenter)
        self.mutation_rate_line.setObjectName("mutation_rate_line")
        self.gridLayout.addWidget(self.mutation_rate_line, 7, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.gen_alg_confirm_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gen_alg_confirm_button.sizePolicy().hasHeightForWidth())
        self.gen_alg_confirm_button.setSizePolicy(sizePolicy)
        self.gen_alg_confirm_button.setObjectName("gen_alg_confirm_button")
        self.horizontalLayout.addWidget(self.gen_alg_confirm_button)
        self.gen_alg_cancel_button = QtWidgets.QPushButton(Dialog)
        self.gen_alg_cancel_button.setObjectName("gen_alg_cancel_button")
        self.horizontalLayout.addWidget(self.gen_alg_cancel_button)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Genetic algorithm"))
        self.label_5.setText(_translate("Dialog", "These are the parameters of the genetic algorithm."))
        self.label_6.setText(_translate("Dialog", "It is recommended to keep the default values."))
        self.label_2.setText(_translate("Dialog", "Number of chromosones"))
        self.chromo_number_line.setText(_translate("Dialog", str(self.generation_size)))
        self.crossover_rate_line.setText(_translate("Dialog", str(self.prob_crossover)))
        self.label_3.setText(_translate("Dialog", "Crossover rate"))
        self.label_4.setText(_translate("Dialog", "Mutation rate"))
        self.gen_number_line.setText(_translate("Dialog", str(self.generation_number)))
        self.label.setText(_translate("Dialog", "Number of generations"))
        self.mutation_rate_line.setText(_translate("Dialog", str(self.prob_mutation)))
        self.gen_alg_confirm_button.setText(_translate("Dialog", "Save"))
        self.gen_alg_cancel_button.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Gen_Algorithm_Parameter_Window()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

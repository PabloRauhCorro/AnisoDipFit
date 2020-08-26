from PyQt5.QtWidgets import QMainWindow, QMessageBox

# overriding the close Event function of QMainWindow to get a "Are you sure" window when user wants to exit without saving
class QMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.results_are_not_saved = []

    def closeEvent(self, event):
        if len(self.results_are_not_saved) > 0:
            results_are_not_saved = str(self.results_are_not_saved)
            text = f"There are unsaved results of: \n\n{results_are_not_saved} \n\n Are you sure you want to exit without saving?"
            reply = QMessageBox.question(self, 'Window Close', text,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
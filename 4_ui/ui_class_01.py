import sys
from PySide6.QtWidgets import QApplication, QMessageBox

def confirm_popup():
    app = QApplication(sys.argv)  # Create application first
    
    wg_msg = QMessageBox()
    wg_msg.setStandardButtons(QMessageBox.Open | QMessageBox.Save | QMessageBox.NoToAll)
    wg_msg.setWindowTitle('Simple Save')
    wg_msg.setText('Save changes?')
    wg_msg.exec()

    sys.exit(app.exec())

confirm_popup()
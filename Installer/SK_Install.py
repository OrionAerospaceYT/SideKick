from Install import Ui_MainWindow as install
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import SK_Script
import threading
import sys

is_admin = False

class Install(qtw.QMainWindow):

    def __init__(self, parent = None):
        self.com_port = 0
        self.i = 0

        super(Install, self).__init__(parent=parent)

        # Define the gui.
        self.ui = install()
        self.ui.setupUi(self)

        image = qtg.QPixmap("Dependencies/Orion.png")
        image = image.scaled(150, 130, qtc.Qt.KeepAspectRatio, qtc.Qt.FastTransformation)
        self.ui.image.setPixmap(image)

        timer = qtc.QTimer(self)
        timer.setInterval(15)
        timer.timeout.connect(self.update)
        timer.start()

    def update(self):

        #print(SK_Script.is_admin)
        if is_admin:
            self.i += 1
            if self.i < 96:
                self.ui.progressBar.setValue(int(self.i))
            elif not len(threading.enumerate()) > 2:
                self.ui.progressBar.setValue(100)
                if self.i > 120:
                    sys.exit()

            if self.i < 20:
                self.ui.installing.setHtml("<p align=\"center\" style=\" margin-top:40px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Downloading arduino-cli...</span></p>")
            elif self.i < 40:
                self.ui.installing.setHtml("<p align=\"center\" style=\" margin-top:40px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Updating system variables...</span></p>")
            elif self.i < 50:
                self.ui.installing.setHtml("<p align=\"center\" style=\" margin-top:40px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Downloading teensy...</span></p>")
            elif self.i < 95:
                self.ui.installing.setHtml("<p align=\"center\" style=\" margin-top:40px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Downloading SideKick...</span></p>")
            else:
                self.ui.installing.setHtml("<p align=\"center\" style=\" margin-top:40px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Done!</span></p>")

if __name__ == "__main__":
    install_script = threading.Thread(target=SK_Script.install)
    install_script.start()
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet("""* {
                        font-family: monospace;
                        background-color: #32323C;
                        }
                        QTextBrowser {
                        font-size: 15px;
                        border: none;
                        padding-left: 40px;
                        color: #00f0c3;
                        }
                        QProgressBar
                        {
                        background: #252535;
                        color: #00f0c3;
                        border: none;
                        border-radius: 15px;
                        text-align: right;
                        height: 40px;
                        }
                        QProgressBar::chunk
                        {
                        background-color: #00f0c3;
                        border-radius: 15px;
                        }
                        QLabel
                        {
                        height: 20px;
                        width: 20px;
                        padding-left: 40px;
                        }
                        """)
    app_icon = qtg.QIcon("Dependencies/Orion_1.ico")
    app.setWindowIcon(app_icon)
    install = Install()
    install.show()
    app.exec_()

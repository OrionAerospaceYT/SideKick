# Graph debug

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from demo import Ui_Dialog

class GraphUI():

    def __init__(self):
        #TODO make graph
        self.graph_data_y = [1, 2, 3, 4, 5, 6, 7]

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    Dialog = qtw.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

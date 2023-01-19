import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget
from numpy import array
from stl import mesh

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.object = None

    def load_mesh(self, filename):
        self.object = mesh.Mesh.from_file(filename)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        if self.object:
            glBegin(GL_TRIANGLES)
            for face in self.object.vectors:
                for vertex in face:
                    glVertex3fv(vertex)
            glEnd()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("STL Viewer")
        self.resize(800, 600)
        self.gl_widget = GLWidget(self)
        self.setCentralWidget(self.gl_widget)
        self.open_action = QtWidgets.QAction("Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.open_action)

    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open STL file", "", "STL Files (*.stl)")
        if filename:
            self.gl_widget.load_mesh(filename)
            self.gl_widget.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
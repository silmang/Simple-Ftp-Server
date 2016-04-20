#encoding: utf-8
import os, threading, logging
##https://wiki.qt.io/PySide_Tutorials
from PySide import QtCore, QtGui
##https://pythonhosted.org/pyftpdlib/tutorial.html
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class SimpleFtpWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(415, 185)
        self.setWindowTitle('Simple FTP Server')
        
        self.Directory = QtGui.QLineEdit(self)
        self.Directory.setGeometry(10, 50, 270, 25)
        self.SetDirectory = QtGui.QPushButton(self)
        self.SetDirectory.setGeometry(285, 50, 120, 25)
        self.groupBox = QtGui.QGroupBox(self)
        self.groupBox.setGeometry(10, 90, 395, 50)
        self.OnButton = QtGui.QRadioButton(self.groupBox)
        self.OnButton.setGeometry(90, 20, 90, 15)
        self.OffButton = QtGui.QRadioButton(self.groupBox)
        self.OffButton.setGeometry(220, 20, 90, 15)
        self.Subject = QtGui.QLabel(self)
        self.Subject.setGeometry(10, 10, 395, 30)
        self.Result = QtGui.QLabel(self)
        self.Result.setGeometry(10, 150, 395, 30)
        
        self.SetDirectory.setText("Choose Directoy")
        self.groupBox.setTitle("Power")
        self.Result.setText("")
        self.OnButton.setText("On")
        self.OffButton.setText("Off")
        self.OffButton.setChecked(1)
        self.Subject.setText("Simple FTP Server")
        
        self.action()
        self.show()
        
    def action(self):
        self.SetDirectory.clicked.connect(self.openDirectoryDialog)
        self.OnButton.clicked.connect(self.on_clicked)
        self.OffButton.clicked.connect(self.off_clicked)
    
    def openDirectoryDialog(self):
        #path, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        self.flags = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        self.path = directory = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory", os.getcwd(), self.flags)
        self.Directory.setText(self.path)
        
    def on_clicked(self):
        #global server
        authorizer = DummyAuthorizer()
        try:
            authorizer.add_anonymous(self.Directory.text())
        except:
            authorizer.add_anonymous(os.getcwd())
        logging.basicConfig(filename='ftpd.log', level=logging.INFO)
        handler = FTPHandler
        handler.authorizer = authorizer
        self.server = FTPServer(('127.0.0.1', 21), handler)
        self.th = threading.Thread(target=self.server.serve_forever)
        self.th.start()
        self.Result.setText('on, 127.0.0.1:21, anonymous')
        
    def off_clicked(self):
        self.server.close_all()
        self.th.join()
        self.Result.setText('off')

if __name__ == '__main__':
    try:
        os.remove('ftpd.log')
    except OSError:
        pass
    app = QtGui.QApplication([])
    mainWin = SimpleFtpWindow()
    app.exec_()
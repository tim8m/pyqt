from PyQt5.QtCore import QObject, pyqtSignal


class Cl2(QObject):
    mySignal = pyqtSignal(float)

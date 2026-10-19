from PyQt5.QtCore import QObject, pyqtSignal


class Cl1(QObject):
    mySignal = pyqtSignal(float)


def func(data):
    newList = data.getData()
    return newList

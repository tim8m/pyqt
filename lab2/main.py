from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import cl1
import cl2


class Some(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Рубли в доллары и евро (курс ЦБ на 31.12.2007)")
        self.data = data
        self.cl1 = cl1.Cl1()
        self.cl2 = cl2.Cl2()
        self.myClsig = self.cl1.mySignal

        self.rub = QDoubleSpinBox()
        self.rub.setRange(0, 1e12)
        self.rub.setDecimals(2)
        self.rub.setSuffix(" ₽")
        self.usd = QLabel("0.00")
        self.eur = QLabel("0.00")

        form = QFormLayout()
        form.addRow("Рубли:", self.rub)
        form.addRow("Доллары:", self.usd)
        form.addRow("Евро:", self.eur)
        central = QWidget()
        central.setLayout(form)
        self.setCentralWidget(central)

        self.rub.valueChanged.connect(self.onRub)
        self.cl1.mySignal.connect(lambda v: self.usd.setText(f"{v:,.2f}"))
        self.cl2.mySignal.connect(lambda v: self.eur.setText(f"{v:,.2f}"))

    def onRub(self, rub):
        rates = self.data.getData()
        self.cl1.mySignal.emit(rub / rates["USD"])
        self.cl2.mySignal.emit(rub / rates["EUR"])


class Data:
    def __init__(self):
        self.myData = {"USD": 24.5462, "EUR": 35.9332}

    def getData(self):
        return self.myData


if __name__ == "__main__":
    data = Data()
    cl1.func(data)
    app = QApplication(sys.argv)
    window = Some(data)
    window.show()
    app.exec()

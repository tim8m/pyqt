import sys
import os
import base64
from datetime import datetime

from PyQt5.QtCore import QObject, Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_dir = os.path.join(base_dir, "saves")
        os.makedirs(self.save_dir, exist_ok=True)

    @pyqtSlot(str)
    def saveImage(self, data_url):
        _, _, b64 = data_url.partition(",")
        img = QImage.fromData(base64.b64decode(b64), "PNG")
        if img.isNull():
            print("Ошибка: не удалось прочитать изображение с доски")
            return

        result = QImage(img.size(), QImage.Format_RGB32)
        result.fill(Qt.white)
        painter = QPainter(result)
        painter.drawImage(0, 0, img)
        painter.end()   

        name = datetime.now().strftime("drawing_%Y-%m-%d_%H-%M-%S.png")
        path = os.path.join(self.save_dir, name)
        if result.save(path):
            print("Сохранено:", path)
        else:
            print("Ошибка сохранения:", path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)

    engine.load("mainWindow.qml")

    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    sys.exit(app.exec())
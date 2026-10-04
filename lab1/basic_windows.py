from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
import sys
from PyQt5.QtGui import QPixmap
#from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Пример PyQt")
window.resize(400, 300)

label = QLabel("Привет, PyQt!")
label.setAlignment(Qt.AlignCenter)
image_label = QLabel()
image_label.setAlignment(Qt.AlignCenter)

button = QPushButton("Нажми меня")

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
layout.addWidget(image_label)
window.setLayout(layout)

def on_click():
    pixmap = QPixmap("13447.jpg")
    #if pixmap.isNull():
    #label.setText("Не удалось загрузить картинку")
    #return
    # масштабируем под ширину окна
    image_label.setPixmap(
        pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )
    label.setText("Картинка показана")

button.clicked.connect(on_click)

window.show()
sys.exit(app.exec_())

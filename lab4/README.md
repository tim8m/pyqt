**Задание**   
Взять из папки lab4_template каркас для четвертой лабораторной работы:
В нём реализована логика backend (pyqt) и fronted (qml) приложения painter. В классе Inerface реализовать логику сохранения области рисования canvas по таймеру на носитель информации в файл  


**Изменения в коде**  
В файл MainWindow.qml был добавлен блок таймер, который каждые 15 секунд проверяет с помощью переменной canvas dirty изменение холста. Если изменения есть, то вызывается метод toDataURL, превращающий изображение в строку base64.  

    Timer {
        interval: 15000
        running: true
        repeat: true
        onTriggered: {
            if (canvas.dirty) {
                _backend.saveImage(canvas.toDataURL("image/png"))
                canvas.dirty = false
            }
        }
    }  

В файле main также произошли изменения. В инициализирующей функции создается папка saves для сохранения снимков.  
В функции saveImage метод QImage.fromData происводит декодирование картинки из base65 в PNG.  
Так как изображения Canvas имеют прозрачный фон, то в коде происходит создание нового рисунка с таким же размером как у изображения полученного из Canvas. Новое изображение заливается белым фоном и поверх наносится рисунок, полученный из QML.  
Далее формируется имя файла и сохраняется в папку saves


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
                print("Ошибка сохранения:", path)'

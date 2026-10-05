Задание:  
Взять из папки lab4_template каркас для четвертой лабораторной работы:
В нём реализована логика backend (pyqt) и fronted (qml) приложения painter. В классе Inerface реализовать логику сохранения области рисования canvas по таймеру на носитель информации в файл  

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

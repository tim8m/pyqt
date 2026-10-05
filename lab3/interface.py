#!/usr/bin/python

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QComboBox
import sqlite3 


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(700, 450)
        self.setWindowTitle('Мое приложение')
        self.db_conn = None 
        self.db_path = None 

        conn_action = QtWidgets.QAction('подключение к базе данных', self)
        conn_action.setStatusTip('подключение к базе данных')
        conn_action.triggered.connect(self.connect_db)

        disconn_action = QtWidgets.QAction('отключение от базы данных', self)
        disconn_action.setStatusTip('отключение от базы данных')
        disconn_action.triggered.connect(self.disconnect_db)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(conn_action)
        file_menu.addAction(disconn_action)

        self.tabs = QtWidgets.QTabWidget()

        for i in range(1, 6):
            self._create_tab(f'Вкладка {i}')

        self.btn1     = QtWidgets.QPushButton('bt1 \"SELECT * FROM sqlite_master\"')
        self.combo  = QComboBox(self)
        self.combo.addItems(["type","name", "tbl_name","rootpage", "sql"])
        self.btn3  = QtWidgets.QPushButton('bt3 \"Query3\"')
        self.btn2   = QtWidgets.QPushButton('bt2 \"Query2\"')

        self.combo.activated[str].connect(self.select_columns)
        self.btn1.clicked.connect(self.bt1)
        #self.btn_remove.clicked.connect(self.bt1)
        self.btn3.clicked.connect(self.bt3)
        self.btn2.clicked.connect(self.bt2)

        container = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()

        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.btn1)
        row1.addWidget(self.combo)
        row1.addStretch()
        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(self.btn2)
        row2.addWidget(self.btn3)
        row2.addStretch()      

        # Кнопки сверху, вкладки снизу
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addWidget(self.tabs)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.statusBar().showMessage('Ready')

    def connect_db(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Выберите файл базы данных','','SQLite DB (*.db *.sqlite *.sqlite3);;Все файлы (*)')
        if not path: 
            self.statusBar().showMessage('Выбор отменен')

        else:
            self.db_path = path 
            self.db_conn = sqlite3.connect(self.db_path)
            self.db_cur  = self.db_conn.cursor()
            self.statusBar().showMessage("Подключено")
            self.db_cur.execute('SELECT * FROM sqlite_master')
            data = self.db_cur.fetchall()
            result = " ".join(map(str,data))
            tab = self.tabs.widget(0)
            print(result)
            tab.label.setText(result)


    def disconnect_db(self):
        if self.db_conn is not None:
            try:
                self.db_conn.close()
                self.statusBar().showMessage('Успешно отключено')
            except sqlite3.Error as e :
                self.statusBar().showMessage('Ошибка закрытия')
            finally:
                self.db_conn = None

    def bt1(self):
        self.db_cur.execute('SELECT name FROM sqlite_master')
        data = self.db_cur.fetchall()
        result = " ".join(map(str,data))
        tab = self.tabs.widget(1)
        print(result)
        tab.label.setText(result)

    def select_columns(self,text):
        self.db_cur.execute(f'SELECT {text} FROM sqlite_master')
        data = self.db_cur.fetchall()
        result = "\n".join(str(r[0]) for r in data)
        tab = self.tabs.widget(2)
        tab.label.setText(result)

    def bt2(self):
        self.db_cur.execute('SELECT * FROM users')
        data = self.db_cur.fetchall()
        result = "\n".join(map(str,data))
        tab = self.tabs.widget(3)
        tab.label.setText(result)
    
    def bt3(self):
        self.db_cur.execute('SELECT * FROM users')
        data = self.db_cur.fetchall()
        result = "\n".join(map(str,data))
        tab = self.tabs.widget(4)
        tab.label.setText(result)

    def _create_tab(self, title):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(f'Содержимое: {title}')
        layout.addWidget(label)
        layout.addStretch()
        tab.setLayout(layout)
        tab.label = label
        self.tabs.addTab(tab, title)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
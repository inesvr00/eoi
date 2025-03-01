#!/usr/bin/env python3

import sys

from PyQt6.QtWidgets import (
    QWidget, 
    QPushButton,
    QApplication,
    )

class Example(QWidget):
    
    def __init__(self):
        super().__init__()        
        btn = QPushButton('Hello world', self)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)       
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QT6 - Hola, mundo')    
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())

        
if __name__ == '__main__':
    main()

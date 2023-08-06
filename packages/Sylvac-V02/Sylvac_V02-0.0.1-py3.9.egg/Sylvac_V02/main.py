# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
# import board
# import busio
# from digitalio import Direction, Pull
# from adafruit_mcp230xx.mcp23017 import MCP23017
import time
import random

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal, QObject, Property, QThread, QUrl
from PySide2.QtQml import QQmlContext


class ThreadClass(QtCore.QThread):
    signal = Signal(int)

    def __init__(self, index=0):
        super().__init__(self)
        self.index = index

    def run(self):
        # show()
        pass


class PropertyPython(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.__number = 42
        self.__max_number = 99

    @Signal
    def maxNumberChanged(self):
        pass

    @Slot(int)
    def setMaxNumber(self, val):
        self.set_max_number(val)

    def set_max_number(self, val):
        if val < 0:
            val = 0

        if self.__max_number != val:
            self.__max_number = val
            self.maxNumberChanged.emit()

        if self.__number > self.__max_number:
            self.__set_number(self.__max_number)

    def get_max_number(self):
        return self.__max_number

    def __set_number(self, val):
        if self.__number != val:
            self.__number = val

    def get_number(self):
        self.__max_number

    @Slot()
    def updateNumber(self):
        self.__set_number(random.randint(0, self.__max_number))

    maxNumber = Property(int, get_number, setMaxNumber, notify=maxNumberChanged)


class NumberGenerator(QObject):
    def __init__(self):
        QObject.__init__(self)

    nextNumber = Signal(int)

    @Slot()
    def giveNumber(self):
        self.nextNumber.emit(random.randint(0, 99))


def Run():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType(NumberGenerator, 'Generators', 1, 0, 'NumberGenerator')

    engine.load(QUrl("../Qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    Run()

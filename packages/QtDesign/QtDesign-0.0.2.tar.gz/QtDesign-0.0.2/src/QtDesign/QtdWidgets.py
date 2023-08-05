from PySide2 import QtCore, QtGui, QtWidgets

import typing


class QCard(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # Create button widget for card interactions
        self.__button = QtWidgets.QPushButton(self)
        self.__button.move(self.geometry().bottomRight() - self.__button.geometry().bottomRight())
        self.__button.setFixedSize(self.size())

    def isChecked(self) -> bool:
        return self.__button.isChecked()

    def isEnabled(self) -> bool:
        return self.__button.isEnabled()

    def setAutoDefault(self, arg__1: bool) -> None:
        return self.__button.setAutoDefault(arg__1)

    def setAutoRepeat(self, arg__1: bool) -> None:
        return self.__button.setAutoRepeat(arg__1)

    def setAutoRepeatDelay(self, arg__1: int) -> None:
        return self.__button.setAutoRepeatDelay(arg__1)

    def setAutoRepeatInterval(self, arg__1: int) -> None:
        return self.__button.setAutoRepeatInterval(arg__1)

    def setCheckable(self, arg__1: bool) -> None:
        return self.__button.setCheckable(arg__1)

    def setChecked(self, arg__1: bool) -> None:
        return self.__button.setChecked(arg__1)

    def setEnabled(self, arg__1: bool) -> None:
        return self.__button.setEnabled(arg__1)

    @property
    def clicked(self):
        return self.__button.clicked

    @property
    def pressed(self):
        return self.__button.pressed

    @property
    def released(self):
        return self.__button.released

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.__button.setFixedSize(self.size())

class QRichTabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        super().__init__(parent)

    def setTabText(self, index: int, text: str):
        label = QtWidgets.QLabel(self)
        label.setText(text)
        label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.setTabButton(index, QtWidgets.QTabBar.LeftSide, label)

    def tabText(self, index: int):
        doc = QtGui.QTextDocument()
        doc.setHtml(self.tabButton(index, QtWidgets.QTabBar.LeftSide).text())
        return doc.toPlainText()

class QRichTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._tabBar = QRichTabBar(self)
        self.setTabBar(self._tabBar)

    @typing.overload
    def addTab(self, widget: QtWidgets.QWidget, arg__2: str) -> int: ...
    @typing.overload
    def addTab(self, widget: QtWidgets.QWidget, icon: QtGui.QIcon, label: str) -> int: ...

    def addTab(self, *args, **kwargs) -> int:
        index = super().addTab(*args, **kwargs)
        text = super().tabText(index)
        super().setTabText(index, "")
        self._tabBar.setTabText(index, text)

        return index

    @typing.overload
    def insertTab(self, index: int, widget: QtWidgets.QWidget, arg__3: str) -> int: ...
    @typing.overload
    def insertTab(self, index: int, widget: QtWidgets.QWidget, icon: QtGui.QIcon, label: str) -> int: ...

    def insertTab(self, *args, **kwargs) -> int:
        index = super().insertTab(*args, **kwargs)
        text = super().tabText(index)
        super().setTabText(index, "")
        self._tabBar.setTabText(index, text)

        return index

    def setTabText(self, index: int, text: str):
        self._tabBar.setTabText(index, text)

    def tabText(self, index: int):
        return self._tabBar.tabText(index)
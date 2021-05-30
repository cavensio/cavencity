from PyQt5.QtWidgets import QLCDNumber


class CvCounter(QLCDNumber):
    def __init__(self):
        super().__init__()
        self._online: bool = None
        self._value: int = 0
        self.setMinimumWidth(150)
        self.setMinimumHeight(50)
        self.setFrameStyle(QLCDNumber.Flat)
        self.setSegmentStyle(QLCDNumber.Flat)

    def setValue(self, value, online: bool = True) -> None:
        if value != self._value:
            self._value = value
            super().display(value)

        if online != self._online:
            self._online = online
            self.setProperty('online', online)
            self.style().unpolish(self)
            self.style().polish(self)

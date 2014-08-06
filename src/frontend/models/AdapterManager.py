# -*- coding: utf-8 -*-

from launcher import app
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, Qt

from collections import OrderedDict


class AdapterManager(QObject):
    summaryUpdated = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self._adapters = OrderedDict()

    @pyqtProperty(int, notify = summaryUpdated)
    def ulSpeed(self):
        return sum(map(lambda a: a.ulSpeed, self._adapters.values()))

    @pyqtProperty(int, notify = summaryUpdated)
    def dlSpeed(self):
        return sum(map(lambda a: a.dlSpeed, self._adapters.values()))

    @pyqtProperty(int, notify = summaryUpdated)
    def runningTaskCount(self):
        return sum(map(lambda a: a.runningTaskCount, self._adapters.values()))

    def registerAdapter(self, adapter):
        ns = adapter.namespace
        assert ns not in self._adapters
        adapter.update.connect(app.taskModel.taskManager.updateMap,
                               Qt.DirectConnection)
        self._adapters[ns] = adapter

    def adapter(self, ns):
        return self._adapters[ns]

    def __getitem__(self, item):
        assert item == 0
        index = list(self._adapters.keys())
        return self._adapters[index[0]]
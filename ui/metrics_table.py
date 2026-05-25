from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class MetricsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["PID", "Completion Time", "Turnaround Time", "Waiting Time"])
        self.setMaximumHeight(200)
    
    def populate(self, completed):
        """
        Fill table with results from algorithm.
        
        Args:
            completed: dict {pid: [CT, TAT, WT]}
        """
        self.setRowCount(len(completed))
        
        for row, (pid, metrics) in enumerate(completed.items()):
            ct, tat, wt = metrics
            
            self.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.setItem(row, 1, QTableWidgetItem(str(ct)))
            self.setItem(row, 2, QTableWidgetItem(str(tat)))
            self.setItem(row, 3, QTableWidgetItem(str(wt)))
    
    def clear(self):
        self.setRowCount(0)

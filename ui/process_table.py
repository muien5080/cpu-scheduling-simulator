from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QSpinBox, QLineEdit
)
from PyQt5.QtCore import Qt


class ProcessTable(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.show_priority = False
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Setup table
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["PID", "Arrival", "Burst"])
        self.table.setMaximumHeight(250)
        
        # Add/remove buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Process")
        add_btn.clicked.connect(self.add_row)
        remove_btn = QPushButton("Remove Process")
        remove_btn.clicked.connect(self.remove_row)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(remove_btn)
        button_layout.addStretch()
        
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # PID
        pid_item = QTableWidgetItem(f"P{row + 1}")
        self.table.setItem(row, 0, pid_item)
        
        # Arrival, Burst default to 0
        for col in range(1, 3):
            item = QTableWidgetItem("0")
            self.table.setItem(row, col, item)
        
        # Priority default to 1 (if enabled)
        if self.show_priority:
            item = QTableWidgetItem("1")
            self.table.setItem(row, 3, item)
    
    def remove_row(self):
        selected = self.table.selectedIndexes()
        if selected:
            row = selected[0].row()
            self.table.removeRow(row)
    
    def set_priority_column(self, show):
        """Show or hide priority column based on algorithm"""
        self.show_priority = show
        if show and self.table.columnCount() == 3:
            self.table.insertColumn(3)
            self.table.setHorizontalHeaderLabels(["PID", "Arrival", "Burst", "Priority"])
            # Initialize priority column for existing rows
            for row in range(self.table.rowCount()):
                item = QTableWidgetItem("1")
                self.table.setItem(row, 3, item)
        elif not show and self.table.columnCount() == 4:
            self.table.removeColumn(3)
            self.table.setHorizontalHeaderLabels(["PID", "Arrival", "Burst"])
    
    def get_processes(self):
        """Returns list of tuples: (arrival_time, burst_time, pid) or (priority, pid, burst_time, arrival_time) for priority algorithms"""
        processes = []
        for row in range(self.table.rowCount()):
            try:
                pid = self.table.item(row, 0).text()
                arrival = int(self.table.item(row, 1).text())
                burst = int(self.table.item(row, 2).text())
                
                if self.show_priority:
                    priority = int(self.table.item(row, 3).text())
                    processes.append((priority, pid, burst, arrival))
                else:
                    processes.append((arrival, burst, pid))
            except (ValueError, TypeError):
                continue
        
        return processes
    
    def clear(self):
        self.table.setRowCount(0)

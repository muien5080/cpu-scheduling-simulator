from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt5.QtCore import Qt

from ui.process_table import ProcessTable
from ui.controls import Controls
from ui.gantt_chart import GanttChart
from ui.metrics_table import MetricsTable


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Scheduling Simulator")
        self.setGeometry(100, 100, 1200, 800)
        
        self.process_table = ProcessTable()
        self.controls = Controls()
        self.gantt_chart = GanttChart()
        self.metrics_table = MetricsTable()
        
        self.setup_layout()
        self.connect_signals()
    
    def setup_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left side: input and controls
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Processes"))
        left_layout.addWidget(self.process_table)
        left_layout.addWidget(self.controls)
        left_layout.addStretch()
        
        # Right side: visualization and metrics
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Gantt Chart"))
        right_layout.addWidget(self.gantt_chart)
        right_layout.addWidget(QLabel("Metrics"))
        right_layout.addWidget(self.metrics_table)
        
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        central_widget.setLayout(main_layout)
    
    def connect_signals(self):
        self.controls.run_clicked.connect(self.run_simulation)
        self.controls.reset_clicked.connect(self.reset_simulation)
        self.controls.algorithm_changed.connect(self.on_algorithm_changed)
        
        # Initial setup
        self.on_algorithm_changed()
    
    def on_algorithm_changed(self):
        """Update table when algorithm changes"""
        needs_priority = self.controls.needs_priority()
        self.process_table.set_priority_column(needs_priority)
    
    def run_simulation(self):
        processes = self.process_table.get_processes()
        algorithm = self.controls.get_selected_algorithm()
        algo_name = self.controls.combo.currentText()
        
        if not processes:
            return
        
        try:
            # Round Robin needs time quantum
            if algo_name == "Round Robin":
                time_quantum = self.controls.get_time_quantum()
                gantt_chart, completed = algorithm(processes, time_quantum)
            else:
                gantt_chart, completed = algorithm(processes)
            
            self.gantt_chart.draw(gantt_chart, completed, algo_name)
            self.metrics_table.populate(completed)
        except Exception as e:
            print(f"Error running simulation: {e}")
    
    def reset_simulation(self):
        self.process_table.clear()
        self.gantt_chart.clear()
        self.metrics_table.clear()

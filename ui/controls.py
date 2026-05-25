from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSpinBox
from PyQt5.QtCore import pyqtSignal

from algorithms.fcfs import fcfs
from algorithms.sjf_non_preemptive import sjf
from algorithms.srtf import srtf
from algorithms.round_robin import round_robin
from algorithms.priority_np import priority_non_preemptive
from algorithms.priority_preemptive import priority_preemptive


class Controls(QWidget):
    run_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    algorithm_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.algorithm_map = {
            "FCFS": fcfs,
            "SJF Non-Preemptive": sjf,
            "SRTF": srtf,
            "Round Robin": round_robin,
            "Priority Non-Preemptive": priority_non_preemptive,
            "Priority Preemptive": priority_preemptive,
        }
        self.priority_algorithms = {
            "Priority Non-Preemptive",
            "Priority Preemptive",
        }
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Algorithm selection
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Algorithm:"))
        
        self.combo = QComboBox()
        self.combo.addItems(self.algorithm_map.keys())
        self.combo.currentTextChanged.connect(self.algorithm_changed.emit)
        self.combo.currentTextChanged.connect(self.on_algorithm_changed)
        algo_layout.addWidget(self.combo)
        
        layout.addLayout(algo_layout)
        
        # Time Quantum for Round Robin (wrapped in container for visibility control)
        self.quantum_widget = QWidget()
        self.quantum_layout = QHBoxLayout()
        self.quantum_layout.addWidget(QLabel("Time Quantum:"))
        self.quantum_spinbox = QSpinBox()
        self.quantum_spinbox.setValue(2)
        self.quantum_spinbox.setMinimum(1)
        self.quantum_layout.addWidget(self.quantum_spinbox)
        self.quantum_layout.addStretch()
        self.quantum_widget.setLayout(self.quantum_layout)
        self.quantum_widget.setVisible(False)
        layout.addWidget(self.quantum_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_clicked.emit)
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_clicked.emit)
        
        button_layout.addWidget(run_btn)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_selected_algorithm(self):
        algo_name = self.combo.currentText()
        return self.algorithm_map[algo_name]
    
    def needs_priority(self):
        algo_name = self.combo.currentText()
        return algo_name in self.priority_algorithms
    
    def on_algorithm_changed(self):
        """Show time quantum field for Round Robin"""
        algo_name = self.combo.currentText()
        self.quantum_widget.setVisible(algo_name == "Round Robin")
    
    def get_time_quantum(self):
        return self.quantum_spinbox.value()

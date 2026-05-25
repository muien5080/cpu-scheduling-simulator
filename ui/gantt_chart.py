from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt


class GanttChart(QWidget):
    def __init__(self):
        super().__init__()
        self.gantt_chart = []
        self.completed = {}
        self.setMinimumHeight(150)
    
    def draw(self, gantt_chart, completed=None):
        self.gantt_chart = gantt_chart
        self.completed = completed or {}
        self.update()
    
    def get_burst_times(self):
        """Calculate burst times from gantt_chart and completed dict"""
        burst_times = {}
        
        # First, count consecutive occurrences for each PID
        consecutive_counts = {}
        current_pid = None
        count = 0
        
        for item in self.gantt_chart:
            if item == current_pid:
                count += 1
            else:
                if current_pid is not None and current_pid != "Idle":
                    consecutive_counts[current_pid] = count
                current_pid = item
                count = 1
        
        if current_pid is not None and current_pid != "Idle":
            consecutive_counts[current_pid] = count
        
        # If any PID appears multiple times consecutively, use that as burst time
        if consecutive_counts:
            burst_times.update(consecutive_counts)
        
        # Otherwise, infer from completed dict using WT = TAT - burst
        # We need to calculate burst from the metrics
        if self.completed:
            for pid, metrics in self.completed.items():
                if pid not in burst_times:
                    ct, tat, wt = metrics
                    burst = tat - wt
                    burst_times[pid] = max(1, burst)
        
        return burst_times
    
    def paintEvent(self, event):
        if not self.gantt_chart:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get burst times for all processes
        burst_times = self.get_burst_times()
        
        # Group consecutive items and calculate time
        blocks = []
        time = 0
        current_item = None
        duration = 0
        
        for item in self.gantt_chart:
            if item == current_item:
                duration += 1
            else:
                if current_item is not None:
                    # Calculate duration
                    if current_item == "Idle":
                        item_duration = duration
                    else:
                        item_duration = burst_times.get(current_item, duration)
                    blocks.append((current_item, time, time + item_duration))
                    time += item_duration
                current_item = item
                duration = 1
        
        # Add last block
        if current_item is not None:
            if current_item == "Idle":
                item_duration = duration
            else:
                item_duration = burst_times.get(current_item, duration)
            blocks.append((current_item, time, time + item_duration))
            total_time = time + item_duration
        else:
            total_time = 1
        
        # Calculate block width based on total time
        available_width = self.width() - 40
        block_width_per_unit = available_width / total_time if total_time > 0 else 1
        block_height = 40
        
        x = 20
        y = 30
        
        colors = self.get_process_colors()
        
        # Draw blocks with actual time proportions
        for item, start_time, end_time in blocks:
            duration = end_time - start_time
            width = duration * block_width_per_unit
            
            if item == "Idle":
                color = QColor(200, 200, 200)
                label = "Idle"
            else:
                color = colors.get(item, QColor(100, 150, 200))
                label = item
            
            # Draw rectangle
            painter.fillRect(int(x), int(y), int(width), block_height, color)
            painter.drawRect(int(x), int(y), int(width), block_height)
            
            # Draw label
            painter.setFont(QFont("Arial", 9))
            painter.drawText(int(x), int(y), int(width), block_height, Qt.AlignCenter, label)
            
            x += width
        
        # Draw timeline
        painter.setFont(QFont("Arial", 8))
        timeline_y = y + block_height + 10
        painter.drawLine(20, timeline_y, int(x), timeline_y)
        
        # Draw time units with actual values
        x = 20
        for item, start_time, end_time in blocks:
            duration = end_time - start_time
            width = duration * block_width_per_unit
            
            painter.drawLine(int(x), timeline_y, int(x), timeline_y + 5)
            painter.drawText(int(x) - 15, timeline_y + 8, 30, 20, Qt.AlignCenter, str(int(start_time)))
            
            x += width
        
        # Draw final time marker
        painter.drawLine(int(x), timeline_y, int(x), timeline_y + 5)
        painter.drawText(int(x) - 15, timeline_y + 8, 30, 20, Qt.AlignCenter, str(int(total_time)))
    
    def get_process_colors(self):
        colors = {}
        color_list = [
            QColor(135, 206, 250),  # light blue
            QColor(144, 238, 144),  # light green
            QColor(255, 200, 124),  # light orange
            QColor(219, 112, 147),  # pale red
            QColor(175, 238, 238),  # pale turquoise
            QColor(255, 218, 185),  # peach
            QColor(221, 160, 221),  # plum
            QColor(144, 238, 144),  # khaki
        ]
        
        for idx, item in enumerate(set(self.gantt_chart)):
            if item != "Idle":
                colors[item] = color_list[idx % len(color_list)]
        
        return colors
    
    def clear(self):
        self.gantt_chart = []
        self.update()

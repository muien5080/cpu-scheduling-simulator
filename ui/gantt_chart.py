from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt


class GanttChart(QWidget):
    def __init__(self):
        super().__init__()
        self.gantt_chart = []
        self.completed = {}
        self.algorithm_name = "FCFS"
        self.setMinimumHeight(200)
    
    def draw(self, gantt_chart, completed=None, algorithm_name="FCFS"):
        """Draw the gantt chart with given data"""
        self.gantt_chart = gantt_chart
        self.completed = completed or {}
        self.algorithm_name = algorithm_name
        self.update()
    
    def get_burst_time(self, process_id):
        """Get burst time for a process from completed metrics"""
        if process_id == "Idle":
            return 1
        
        if process_id in self.completed:
            ct, tat, wt = self.completed[process_id]
            burst_time = tat - wt
            return max(1, burst_time)
        return 1
    
    def get_blocks(self):
        """
        Build blocks with actual burst times.
        Consecutive Idle entries are combined into a single block.
        Returns: [(process_id, start_time, end_time), ...]
        """
        if not self.gantt_chart:
            return []
        
        blocks = []
        current_time = 0
        i = 0
        
        while i < len(self.gantt_chart):
            process_id = self.gantt_chart[i]
            
            # If it's Idle, combine consecutive Idles
            if process_id == "Idle":
                idle_count = 1
                j = i + 1
                while j < len(self.gantt_chart) and self.gantt_chart[j] == "Idle":
                    idle_count += 1
                    j += 1
                
                # Each idle is 1 unit, but combine them
                total_idle_time = idle_count
                end_time = current_time + total_idle_time
                blocks.append(("Idle", current_time, end_time))
                current_time = end_time
                i = j
            else:
                # Non-idle process
                burst_time = self.get_burst_time(process_id)
                end_time = current_time + burst_time
                blocks.append((process_id, current_time, end_time))
                current_time = end_time
                i += 1
        
        return blocks
    
    def get_process_colors(self):
        """Get color mapping for each process"""
        colors = {}
        color_list = [
            QColor(52, 168, 224),    # Vivid Blue
            QColor(76, 209, 55),     # Vivid Green
            QColor(255, 157, 77),    # Vivid Orange
            QColor(233, 88, 132),    # Vivid Pink
            QColor(75, 192, 192),    # Teal
            QColor(255, 193, 7),     # Amber
            QColor(156, 39, 176),    # Purple
            QColor(244, 67, 54),     # Red
            QColor(33, 150, 243),    # Blue
            QColor(76, 175, 80),     # Green
        ]
        
        # Assign colors to processes in order of appearance
        process_order = []
        for item in self.gantt_chart:
            if item != "Idle" and item not in process_order:
                process_order.append(item)
        
        for idx, pid in enumerate(process_order):
            colors[pid] = color_list[idx % len(color_list)]
        
        return colors
    
    def paintEvent(self, event):
        """Paint the gantt chart"""
        if not self.gantt_chart:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Get blocks with actual burst times
        blocks = self.get_blocks()
        if not blocks:
            return
        
        total_time = blocks[-1][2] if blocks else 1  # End time of last block
        
        # Calculate dimensions
        margin_left = 60
        margin_right = 30
        margin_top = 50
        margin_bottom = 80
        
        available_width = self.width() - margin_left - margin_right
        
        # Block dimensions
        block_height = 60
        y_block = margin_top
        
        # Calculate pixels per time unit (scale)
        pixels_per_unit = available_width / total_time if total_time > 0 else 1
        
        colors = self.get_process_colors()
        
        # Draw blocks with width proportional to burst time
        x = margin_left
        for process_id, start_time, end_time in blocks:
            duration = end_time - start_time
            width = duration * pixels_per_unit
            
            # Ensure minimum width for idle to be readable
            if process_id == "Idle":
                width = max(width, 60)  # Minimum 60 pixels for Idle
            
            # Choose color and label
            if process_id == "Idle":
                color = QColor(220, 220, 220)
                label = "Idle"
                text_color = QColor(100, 100, 100)
            else:
                color = colors.get(process_id, QColor(100, 150, 200))
                label = process_id
                text_color = QColor(255, 255, 255)
            
            # Draw block rectangle with border
            painter.fillRect(int(x), int(y_block), int(width), block_height, color)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawRect(int(x), int(y_block), int(width), block_height)
            
            # Draw process label on block
            painter.setPen(QPen(text_color, 1))
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            painter.drawText(int(x), int(y_block), int(width), block_height, 
                           Qt.AlignCenter, label)
            
            x += width
        
        # Draw timeline axis
        timeline_y = y_block + block_height + 30
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawLine(margin_left, int(timeline_y), int(x), int(timeline_y))
        
        # Draw timeline markers at block boundaries
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        
        x = margin_left
        for process_id, start_time, end_time in blocks:
            duration = end_time - start_time
            width = duration * pixels_per_unit
            
            # Apply minimum width for idle
            if process_id == "Idle":
                width = max(width, 60)
            
            # Draw vertical tick at start of block
            painter.drawLine(int(x), int(timeline_y), int(x), int(timeline_y + 8))
            
            # Draw time value (cumulative time at start)
            painter.drawText(int(x) - 25, int(timeline_y + 10), 50, 20, 
                           Qt.AlignCenter, str(int(start_time)))
            
            x += width
        
        # Draw final time marker
        painter.drawLine(int(x), int(timeline_y), int(x), int(timeline_y + 8))
        painter.drawText(int(x) - 25, int(timeline_y + 10), 50, 20, 
                       Qt.AlignCenter, str(int(total_time)))
        
        # Draw axis label
        painter.setFont(QFont("Arial", 9))
        painter.drawText(10, int(timeline_y + 35), "Time →")
        
        # Draw title with algorithm name
        painter.setFont(QFont("Arial", 13, QFont.Bold))
        title = f"{self.algorithm_name} Gantt Chart"
        painter.drawText(margin_left, 25, title)
    
    def clear(self):
        """Clear the gantt chart"""
        self.gantt_chart = []
        self.completed = {}
        self.update()

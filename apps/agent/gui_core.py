import sys
import math
import random
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QRadialGradient, QTransform
from PyQt6.QtWidgets import QApplication, QWidget
import threading

from daemon import main as daemon_main

class NeosHologram(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(400, 400)
        
        # 3D Rotating Rings state
        self.angles = [0.0] * 8
        self.speeds = [1.5, -2.0, 1.0, -1.2, 2.5, -0.8, 1.8, -1.5]
        
        # Waveform state
        self.num_bars = 72
        self.bar_heights = [random.uniform(5, 20) for _ in range(self.num_bars)]
        self.target_heights = [random.uniform(5, 30) for _ in range(self.num_bars)]
        self.pulse = 0.0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(40)
        
    def update_animation(self):
        # Update 3D Rings
        for i in range(len(self.angles)):
            self.angles[i] = (self.angles[i] + self.speeds[i]) % 360
            
        # Update Waveform
        for i in range(self.num_bars):
            diff = self.target_heights[i] - self.bar_heights[i]
            self.bar_heights[i] += diff * 0.2
            if random.random() < 0.1:
                self.target_heights[i] = random.uniform(5, 40)
                
        self.pulse = (self.pulse + 0.1) % (math.pi * 2)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 20
        pulse_radius = 45 + math.sin(self.pulse) * 4
        
        # Intense Orange Base Glow
        gradient = QRadialGradient(center, radius)
        gradient.setColorAt(0, QColor(255, 150, 0, 80))
        gradient.setColorAt(0.3, QColor(255, 100, 0, 40))
        gradient.setColorAt(0.8, QColor(255, 50, 0, 10))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius, radius)
        
        # Central glowing orb (Orange)
        orb_grad = QRadialGradient(center, 40)
        orb_grad.setColorAt(0, QColor(255, 220, 150, 255))
        orb_grad.setColorAt(0.5, QColor(255, 150, 0, 180))
        orb_grad.setColorAt(1, QColor(255, 100, 0, 0))
        painter.setBrush(orb_grad)
        painter.drawEllipse(center, pulse_radius, pulse_radius)
        
        # 3D Orbital Rings (Orange/Gold)
        rings = [
            {"radius_mult": 0.35, "rot_x": 45, "rot_y": 0, "rot_z": self.angles[0], "width": 3, "color": QColor(255, 200, 50, 255), "dash": [2, 4]},
            {"radius_mult": 0.5, "rot_x": 0, "rot_y": 60, "rot_z": self.angles[1], "width": 2, "color": QColor(255, 150, 0, 220), "dash": [10, 5, 2, 5]},
            {"radius_mult": 0.7, "rot_x": 75, "rot_y": 30, "rot_z": self.angles[2], "width": 1, "color": QColor(255, 120, 0, 200), "dash": [5, 5]},
            {"radius_mult": 0.85, "rot_x": 30, "rot_y": 75, "rot_z": self.angles[3], "width": 3, "color": QColor(255, 170, 0, 180), "dash": [15, 10]},
            {"radius_mult": 0.95, "rot_x": 90, "rot_y": 0, "rot_z": self.angles[4], "width": 2, "color": QColor(255, 100, 0, 150), "dash": [4, 8]},
        ]
        
        for ring in rings:
            t = QTransform()
            t.translate(center.x(), center.y())
            t.rotate(ring["rot_x"], Qt.Axis.XAxis)
            t.rotate(ring["rot_y"], Qt.Axis.YAxis)
            t.rotate(ring["rot_z"], Qt.Axis.ZAxis)
            painter.setTransform(t)
            
            pen = QPen(ring["color"], ring["width"])
            pen.setDashPattern(ring["dash"])
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            r = radius * ring["radius_mult"]
            painter.drawEllipse(QPointF(0, 0), r, r)
            
        painter.resetTransform()
        
        # Audio Waveform bars (Orange)
        painter.translate(center)
        bar_pen = QPen(QColor(255, 180, 0, 220), 3)
        bar_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bar_pen)
        
        base_radius = 55
        angle_step = 360 / self.num_bars
        
        for i in range(self.num_bars):
            painter.rotate(angle_step)
            h = self.bar_heights[i]
            painter.drawLine(QPointF(0, base_radius), QPointF(0, base_radius + h))

        painter.resetTransform()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        elif event.button() == Qt.MouseButton.RightButton:
            import os
            os._exit(0)
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

if __name__ == "__main__":
    t = threading.Thread(target=daemon_main, daemon=True)
    t.start()
    
    app = QApplication(sys.argv)
    window = NeosHologram()
    window.show()
    sys.exit(app.exec())

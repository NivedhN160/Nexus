# Emotion-Aware Debugging Assistant

## Overview

The Emotion-Aware Debugging Assistant is a real-time computer vision–based system designed to monitor a developer’s facial cues and behavioral patterns in order to estimate frustration levels during programming tasks. The system combines facial landmark analysis, blink detection, head pose estimation, and emotion recognition to compute a normalized frustration score. When the estimated frustration exceeds a predefined threshold, the system provides a visual intervention prompt.

This project is intended for research and educational purposes in the domains of computer vision, affective computing, and human–computer interaction.

---

## Objectives

- Detect and analyze facial features in real time using a webcam  
- Estimate emotional state using deep learning–based facial emotion recognition  
- Monitor behavioral indicators such as blink rate, head tilt, and proximity to the screen  
- Compute a continuous frustration score based on multiple signals  
- Log frustration metrics for later analysis, grouped by source code file  

---

## System Architecture

The system operates as a continuous real-time loop with the following stages:

1. Video capture using OpenCV  
2. Face landmark detection using MediaPipe Face Mesh  
3. Feature extraction (blink rate, head tilt, face size)  
4. Emotion recognition using DeepFace  
5. Frustration score computation  
6. Visualization and logging  

---

## Features

- Real-time facial landmark tracking  
- Blink detection using Eye Aspect Ratio (EAR)  
- Head pose estimation  
- Face distance approximation  
- Emotion classification using deep learning  
- Normalized frustration score (0.0 – 1.0)  
- Visual overlays for live feedback  
- Periodic JSON logging  
- File-specific frustration history  

---

## Technologies Used

- Python 3  
- OpenCV  
- MediaPipe  
- DeepFace  
- NumPy  

---

## Installation

### Prerequisites

- Python 3.8 or later  
- Functional webcam  

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/emotion-aware-debugging-assistant.git
cd emotion-aware-debugging-assistant
Install required dependencies:
pip install opencv-python mediapipe deepface numpy
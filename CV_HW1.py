import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGroupBox, 
                             QFileDialog, QLineEdit, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image1 = None  # For most functions
        self.image2 = None  # Only for 2.3 Median Filter
        
        # For edge detection
        self.sobel_x = None
        self.sobel_y = None
        self.combination = None
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('MainWindow')
        self.setGeometry(100, 100, 900, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Far Left - Load Image buttons only
        load_widget = QWidget()
        load_layout = QVBoxLayout(load_widget)
        load_layout.setSpacing(10)
        
        btn_load1 = QPushButton('Load Image 1')
        btn_load1.setFixedHeight(40)
        btn_load1.clicked.connect(self.load_image1)
        load_layout.addWidget(btn_load1)
        
        btn_load2 = QPushButton('Load Image 2')
        btn_load2.setFixedHeight(40)
        btn_load2.clicked.connect(self.load_image2)
        load_layout.addWidget(btn_load2)
        
        load_layout.addStretch()
        main_layout.addWidget(load_widget)
        
        # Left side - Function buttons
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(5)
        
        # 1. Image Processing
        group1 = QGroupBox('1. Image Processing')
        layout1 = QVBoxLayout()
        layout1.setSpacing(3)
        
        btn1_1 = QPushButton('1.1 Color Separation')
        btn1_1.clicked.connect(self.color_separation)
        layout1.addWidget(btn1_1)
        
        btn1_2 = QPushButton('1.2 Color Transformation')
        btn1_2.clicked.connect(self.color_transformation)
        layout1.addWidget(btn1_2)
        
        group1.setLayout(layout1)
        left_layout.addWidget(group1)
        
        # 2. Image Smoothing
        group2 = QGroupBox('2. Image Smoothing')
        layout2 = QVBoxLayout()
        layout2.setSpacing(3)
        
        btn2_1 = QPushButton('2.1 Gaussian Smoothing')
        btn2_1.clicked.connect(self.gaussian_blur)
        layout2.addWidget(btn2_1)
        
        btn2_2 = QPushButton('2.2 Bilateral Filter')
        btn2_2.clicked.connect(self.bilateral_filter)
        layout2.addWidget(btn2_2)
        
        btn2_3 = QPushButton('2.3 Median Filter')
        btn2_3.clicked.connect(self.median_filter)
        layout2.addWidget(btn2_3)
        
        group2.setLayout(layout2)
        left_layout.addWidget(group2)
        
        # 3. Edge Detection
        group3 = QGroupBox('3. Edge Detection')
        layout3 = QVBoxLayout()
        layout3.setSpacing(3)
        
        btn3_1 = QPushButton('3.1 Sobel X')
        btn3_1.clicked.connect(self.sobel_x_detection)
        layout3.addWidget(btn3_1)
        
        btn3_2 = QPushButton('3.2 Sobel Y')
        btn3_2.clicked.connect(self.sobel_y_detection)
        layout3.addWidget(btn3_2)
        
        btn3_3 = QPushButton('3.3 Combination and Threshold')
        btn3_3.clicked.connect(self.combination_threshold)
        layout3.addWidget(btn3_3)
        
        btn3_4 = QPushButton('3.4 Gradient Angle')
        btn3_4.clicked.connect(self.gradient_angle)
        layout3.addWidget(btn3_4)
        
        group3.setLayout(layout3)
        left_layout.addWidget(group3)
        
        left_layout.addStretch()
        main_layout.addWidget(left_widget)
        
        # Right side - Transforms and Adaptive Threshold
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(10)
        
        # 4. Transforms
        group4 = QGroupBox('4. Transforms')
        layout4 = QVBoxLayout()
        
        # Parameter inputs
        param_layout = QGridLayout()
        
        param_layout.addWidget(QLabel('Rotation:'), 0, 0)
        self.rotation_input = QLineEdit('0')
        self.rotation_input.setPlaceholderText('deg')
        param_layout.addWidget(self.rotation_input, 0, 1)
        
        param_layout.addWidget(QLabel('Scaling:'), 1, 0)
        self.scaling_input = QLineEdit('1.0')
        param_layout.addWidget(self.scaling_input, 1, 1)
        
        param_layout.addWidget(QLabel('Tx:'), 2, 0)
        self.tx_input = QLineEdit('0')
        self.tx_input.setPlaceholderText('pixel')
        param_layout.addWidget(self.tx_input, 2, 1)
        
        param_layout.addWidget(QLabel('Ty:'), 3, 0)
        self.ty_input = QLineEdit('0')
        self.ty_input.setPlaceholderText('pixel')
        param_layout.addWidget(self.ty_input, 3, 1)
        
        layout4.addLayout(param_layout)
        
        btn4 = QPushButton('4. Transforms')
        btn4.clicked.connect(self.transforms)
        layout4.addWidget(btn4)
        
        group4.setLayout(layout4)
        right_layout.addWidget(group4)
        
        # 5. Adaptive Threshold
        group5 = QGroupBox('5. Adaptive Threshold')
        layout5 = QVBoxLayout()
        layout5.setSpacing(3)
        
        btn5_1 = QPushButton('5.1 Global Threshold')
        btn5_1.clicked.connect(self.global_threshold)
        layout5.addWidget(btn5_1)
        
        btn5_2 = QPushButton('5.2 Local Threshold')
        btn5_2.clicked.connect(self.local_threshold)
        layout5.addWidget(btn5_2)
        
        group5.setLayout(layout5)
        right_layout.addWidget(group5)
        
        right_layout.addStretch()
        main_layout.addWidget(right_widget)
    
    # Load Image Functions
    def load_image1(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image files (*.jpg *.png *.bmp)')
        if fname:
            if os.path.exists(fname):
                self.image1 = cv2.imdecode(np.fromfile(fname, dtype=np.uint8), cv2.IMREAD_COLOR)
                if self.image1 is not None:
                    print(f"Image 1 loaded successfully: {fname}")
                else:
                    print(f"Failed to read image: {fname}")
            else:
                print(f"File not found: {fname}")
    
    def load_image2(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image files (*.jpg *.png *.bmp)')
        if fname:
            if os.path.exists(fname):
                self.image2 = cv2.imdecode(np.fromfile(fname, dtype=np.uint8), cv2.IMREAD_COLOR)
                if self.image2 is not None:
                    print(f"Image 2 loaded successfully: {fname}")
                else:
                    print(f"Failed to read image: {fname}")
            else:
                print(f"File not found: {fname}")
    
    # 1.1 Color Separation
    def color_separation(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        b, g, r = cv2.split(self.image1)
        zeros = np.zeros_like(b)
        
        b_image = cv2.merge([b, zeros, zeros])
        g_image = cv2.merge([zeros, g, zeros])
        r_image = cv2.merge([zeros, zeros, r])
        
        cv2.imshow('Blue Channel', b_image)
        cv2.imshow('Green Channel', g_image)
        cv2.imshow('Red Channel', r_image)
    
    # 1.2 Color Transformation
    def color_transformation(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        # Q1: Using cv2.cvtColor
        cv_gray = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        
        # Q2: Using average
        b, g, r = cv2.split(self.image1)
        avg_gray = (b/3 + g/3 + r/3).astype(np.uint8)
        
        cv2.imshow('cv2.cvtColor Gray', cv_gray)
        cv2.imshow('Average Gray', avg_gray)
    
    # 2.1 Gaussian Blur (m=5 only, no trackbar)
    def gaussian_blur(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        m = 5
        kernel_size = 2 * m + 1
        blur = cv2.GaussianBlur(self.image1, (kernel_size, kernel_size), 0, 0)
        cv2.imshow('Gaussian Blur', blur)
    
    # 2.2 Bilateral Filter (m=5 only, no trackbar)
    def bilateral_filter(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        m = 5
        d = 2 * m + 1
        bilateral = cv2.bilateralFilter(self.image1, d, 90, 90)
        cv2.imshow('Bilateral Filter', bilateral)
    
    # 2.3 Median Filter (m=5 only, no trackbar, uses image2)
    def median_filter(self):
        if self.image2 is None:
            print("Please load Image 2 first!")
            return
        
        m = 5
        kernel_size = 2 * m + 1
        median = cv2.medianBlur(self.image2, kernel_size)
        cv2.imshow('Median Filter', median)
    
    # 3.1 Sobel X
    def sobel_x_detection(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        gray = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0, 0)
        
        # Manual Sobel X
        sobel_x_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        self.sobel_x = self.apply_kernel(blur, sobel_x_kernel)
        
        # Normalize to 0-255 for display
        sobel_x_display = cv2.normalize(np.abs(self.sobel_x), None, 0, 255, cv2.NORM_MINMAX)
        sobel_x_display = np.uint8(sobel_x_display)
        
        cv2.imshow('Sobel X', sobel_x_display)
    
    # 3.2 Sobel Y
    def sobel_y_detection(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        gray = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0, 0)
        
        # Manual Sobel Y
        sobel_y_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        self.sobel_y = self.apply_kernel(blur, sobel_y_kernel)
        
        # Normalize to 0-255 for display
        sobel_y_display = cv2.normalize(np.abs(self.sobel_y), None, 0, 255, cv2.NORM_MINMAX)
        sobel_y_display = np.uint8(sobel_y_display)
        
        cv2.imshow('Sobel Y', sobel_y_display)
    
    def apply_kernel(self, image, kernel):
        h, w = image.shape
        kh, kw = kernel.shape
        pad = kh // 2
        padded = np.pad(image, pad, mode='edge')
        result = np.zeros_like(image, dtype=np.float32)
        
        for i in range(h):
            for j in range(w):
                region = padded[i:i+kh, j:j+kw]
                result[i, j] = np.sum(region * kernel)
        
        return result
    
    # 3.3 Combination and Threshold
    def combination_threshold(self):
        if self.sobel_x is None or self.sobel_y is None:
            print("Please run Sobel X and Sobel Y first!")
            return
        
        # Combination
        self.combination = np.sqrt(self.sobel_x**2 + self.sobel_y**2)
        normalized = cv2.normalize(self.combination, None, 0, 255, cv2.NORM_MINMAX)
        normalized = np.uint8(normalized)
        
        # Threshold 128
        _, thresh128 = cv2.threshold(normalized, 128, 255, cv2.THRESH_BINARY)
        
        # Threshold 28  
        _, thresh28 = cv2.threshold(normalized, 28, 255, cv2.THRESH_BINARY)
        
        # Show in separate windows
        cv2.imshow('Combination', normalized)
        cv2.imshow('Threshold 128', thresh128)
        cv2.imshow('Threshold 28', thresh28)
    
    # 3.4 Gradient Angle
    def gradient_angle(self):
        if self.sobel_x is None or self.sobel_y is None:
            print("Please run Sobel X and Sobel Y first!")
            return
        
        # Calculate gradient angle
        angle = np.arctan2(self.sobel_y, self.sobel_x) * 180 / np.pi
        angle[angle < 0] += 360
        
        # Mask 1: 170-190 degrees
        mask1 = np.zeros_like(angle, dtype=np.uint8)
        mask1[(angle >= 170) & (angle <= 190)] = 255
        
        # Mask 2: 260-280 degrees
        mask2 = np.zeros_like(angle, dtype=np.uint8)
        mask2[(angle >= 260) & (angle <= 280)] = 255
        
        # Get normalized combination
        normalized = cv2.normalize(self.combination, None, 0, 255, cv2.NORM_MINMAX)
        normalized = np.uint8(normalized)
        
        # Apply masks to get results
        result1 = cv2.bitwise_and(normalized, normalized, mask=mask1)
        result2 = cv2.bitwise_and(normalized, normalized, mask=mask2)
        
        # Show in separate windows
        cv2.imshow('Gradient Angle 170-190', result1)
        cv2.imshow('Gradient Angle 260-280', result2)
    
    # 4. Transforms
    def transforms(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        try:
            angle = float(self.rotation_input.text())
            scale = float(self.scaling_input.text())
            tx = float(self.tx_input.text())
            ty = float(self.ty_input.text())
        except ValueError:
            print("Please enter valid numbers!")
            return
        
        h, w = self.image1.shape[:2]
        center = (240, 200)  # Center of burger in original image (as specified in homework)
        
        # Create transformation matrices (3x3 for homogeneous coordinates)
        angle_rad = angle * np.pi / 180
        
        # Rotation matrix (corrected for counter-clockwise rotation in image coordinates)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        M_rot = np.array([[cos_a, sin_a, 0],
                          [-sin_a, cos_a, 0],
                          [0, 0, 1]], dtype=np.float32)
        
        # Scale matrix
        M_scale = np.array([[scale, 0, 0],
                            [0, scale, 0],
                            [0, 0, 1]], dtype=np.float32)
        
        # Translation matrix
        M_trans = np.array([[1, 0, tx],
                            [0, 1, ty],
                            [0, 0, 1]], dtype=np.float32)
        
        # Translation to origin
        M_to_origin = np.array([[1, 0, -center[0]],
                                [0, 1, -center[1]],
                                [0, 0, 1]], dtype=np.float32)
        
        # Translation back from origin
        M_from_origin = np.array([[1, 0, center[0]],
                                  [0, 1, center[1]],
                                  [0, 0, 1]], dtype=np.float32)
        
        # Combined transformation: Translation * From_Origin * Scale * Rotation * To_Origin
        M = M_trans @ M_from_origin @ M_scale @ M_rot @ M_to_origin
        
        # Extract 2x3 matrix for cv2.warpAffine
        M_2x3 = M[:2, :]
        
        # Apply transformation with original image size or specified output size
        output_w, output_h = 1920, 1080
        result = cv2.warpAffine(self.image1, M_2x3, (w, h))
        
        cv2.imshow('Transformed', result)
    
    # 5.1 Global Threshold
    def global_threshold(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        gray = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        _, threshold_img = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
        
        # Show original and result in separate windows
        cv2.imshow('Original Image', self.image1)
        cv2.imshow('Global Threshold', threshold_img)
    
    # 5.2 Local Threshold
    def local_threshold(self):
        if self.image1 is None:
            print("Please load Image 1 first!")
            return
        
        gray = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                              cv2.THRESH_BINARY, 19, -1)
        
        # Show original and result in separate windows
        cv2.imshow('Original Image', self.image1)
        cv2.imshow('Local Threshold', threshold_img)

def main():
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
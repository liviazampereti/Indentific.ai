# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 23:27:17 2022

@author: Livia1
"""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import torch
import numpy as np
from datetime import datetime
import os

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.25

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("main_dialog.ui",self)
        self.frame = None
        self.start_button.clicked.connect(self.gotovideo)
        stylesheet = '''
    QDialog {
        background-image: url(main.png);
        background-repeat: no-repeat;
        background-position: center;
    }
'''        
        self.setStyleSheet(stylesheet)
        self.setWindowTitle('Identific.ai')
    def gotovideo(self):
        video=Video()
        widget.addWidget(video)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Video(QDialog):
    def __init__(self):
        super(Video,self).__init__()
        loadUi("video_dialog.ui",self)
        self.sair_button.clicked.connect(self.gotomain)
        self.salvar_button.clicked.connect(self.savephoto)
        self.startVideo()
        
        stylesheet = '''
    QDialog {
        background-image: url(video.png);
        background-repeat: no-repeat;
        background-position: center;
    }
'''        
        self.setStyleSheet(stylesheet)
    def savephoto(self):
        path = r'../saved_images'
        date_time = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        cv2.imwrite(os.path.join(path, date_time + '.png'), self.result)
    def gotomain(self):
        main=Main()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.timer.stop()

    def startVideo(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,353)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,455)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
    
    def update_frame(self):
        ret,self.frame = self.capture.read()
        dim = (455,353)
        self.frame = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)
        self.frame = cv2.flip(self.frame, 1)
        results = model(self.frame)
        self.result = results.render()
        self.result = np.array(self.result)
        self.result = np.squeeze(self.result)
        self.displayImage(self.result, 1)
        
    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        
        if window==1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
        
app=QApplication(sys.argv)
mainwindow=Main()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec_()

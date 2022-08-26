import sys
import requests
import json
import base64
import io

from PIL import Image
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap

from new_case import NewCase

class AppWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.title = "Application"
        self.width = 800
        self.height = 600
        self.user = user

        self.initialize()

    def initialize(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        button_upload = QPushButton("New Case", self)
        button_upload.move(370, 170)
        button_upload.resize(150, 50)
        button_upload.clicked.connect(self.new_case)
        self.label = QLabel(self)

        button_upload1 = QPushButton("About", self)
        button_upload1.move(370, 250)
        button_upload1.resize(150, 50)
        button_upload1.clicked.connect(self.about)
        # loading image
        self.pixmap = QPixmap('OIP.jpeg')
 
        # adding image to label
        self.label.setPixmap(self.pixmap)
        self.label.move(75,120)
        self.label.resize(self.pixmap.width(),self.pixmap.height())

        self.show()

    def new_case(self):
        self.new_case = NewCase(self.user)

    def about(self):
        QMessageBox.about(self,"About","The public can click the photographs of suspicious child and upload them into a portal with details. If you don't know the details fill it with any letters but address must be filled correctly. This photo will be compared automatically with the photos of the registered missing child cases present in the repository \n The input child image is classified with photo having best match and the details are displayed")
    def decode_base64(self, img: str):
        """
        Image is converted ot numpy array.
        """
        img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
        return img

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = AppWindow("admin")
    sys.exit(app.exec())

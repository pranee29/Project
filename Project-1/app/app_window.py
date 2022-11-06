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
from guest_case import Guest
from check_status import Status
class AppWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.title = "Application1"
        self.width = 800
        self.height = 800
        self.user = user

        self.initialize()

    def initialize(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        
        button_upload = QPushButton("Parent User", self)
        button_upload.move(400, 250)
        button_upload.resize(150, 50)
        button_upload.clicked.connect(self.new_case)
        
        self.label = QLabel(self)
        self.label2=QLabel(self)

        button_upload2 = QPushButton("Guest User", self)
        button_upload2.move(400, 330)
        button_upload2.resize(150, 50)
        button_upload2.clicked.connect(self.guest_case)


        button_upload1 = QPushButton("About", self)
        button_upload1.move(400, 490)
        button_upload1.resize(150, 50)
        button_upload1.clicked.connect(self.about)

        button_upload3 = QPushButton("Check Status", self)
        button_upload3.move(400, 410)
        button_upload3.resize(150, 50)
        button_upload3.clicked.connect(self.status)
        # loading image

        self.pixmap = QPixmap('OIP.jpeg')
 
        # adding image to label
        self.label.setPixmap(self.pixmap)
        self.label.move(75,240)
        self.label.resize(self.pixmap.width(),self.pixmap.height())


        self.pixmap1 = QPixmap('Missing.jpeg')
        # adding image to label
        self.label2.setPixmap(self.pixmap1)
        self.label2.move(170,100)
        self.label2.resize(self.pixmap1.width(),self.pixmap1.height())


        

        self.show()

    def new_case(self):
        self.new_case = NewCase(self.user)

    def guest_case(self):
        self.guest_case = Guest(self.user)

    def about(self):
        QMessageBox.about(self,"About","The public can click the photographs of suspicious child and upload them into a portal with details. If you don't know the details fill it with any letters but address must be filled correctly. This photo will be compared automatically with the photos of the registered missing child cases present in the repository \n The input child image is classified with photo having best match and the details are displayed")
    
    def status(self):
        self.check_status=Status(self.user)

    def decode_base64(self, img: str):
        """
        Image is converted ot numpy array.
        """
        img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
        return img
style = """
        QWidget{
            background: #262D37;
        }
        QLabel{
            color: #fff;
        }
        QListView
        {
            background: #7e959e;
        }
        QLabel#round_count_label, QLabel#highscore_count_label{
            border: 1px solid #fff;
            border-radius: 8px;
            padding: 2px;
        }
        QPushButton
        {
            color: white;
            background: #0577a8;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none;
        }
        QPushButton:hover{
            border: 1px #C6C6C6 solid;
            color: #fff;
            background: #0892D0;
        }
        QLineEdit {
            padding: 1px;
            color: #fff;
            border-style: solid;
            border: 2px solid #fff;
            border-radius: 8px;
        }
    """

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    w = AppWindow("admin")
    sys.exit(app.exec())

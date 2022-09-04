import sys
import requests
import base64
import json
import dlib
import io
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage, QImageReader
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QApplication
from PyQt5.QtWidgets import QInputDialog, QLabel, QLineEdit, QMessageBox

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import  QIcon
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QListView,
    QBoxLayout,
)
import numpy as np
from utils import generate_uuid
from match_faces1 import match1
from train_model import train
class NewCase(QMainWindow):
    """
    This class is a subpart of main window.
    The purpose of this class is to register a new case and
    save it in Firebase Database.

    After selecting the image you'll see in left side of window.
    If you are able to see image that means algo is able to find
    facial points in image. Otherwise you'll get error.

    If you encounter any error while saving the image, check the logs
    which are being printed.
    """

    def __init__(self, user: str):
        """
        We are initializing few things we would need.
            name -> Name of person whose case has to be registered.
            age -> Age of the person
            mob -> Mobile number that will be contacted after the person is found.
            father_name -> Father's name of the person
            image -> image of the person

        Args:
            user: str
                The logged in user
        """
        super().__init__()
        self.title = "Register New Case"
        self.name = None
        self.age = None
        self.mob = None
        self.father_name = None
        self.image = None
        self.loc=None
        self.encoded_image = None
        self.key_points = None
        self.user = user
        self._x_axis = 500
        self.initialize()

    def initialize(self):
        """
        This method contains button to select the image and
        also register the case.

        The select image button is connected to openFileNameDialog method.

        The save button is connected to save method (within the class).

        -> If you are chaning the window size make sure to align the buttons
            correctly.
        """
        self.setFixedSize(800, 800)
        self.setWindowTitle(self.title)

        upload_image_button = QPushButton("Upload Image", self)
        upload_image_button.resize(150, 50)
        upload_image_button.move(self._x_axis, 20)
        upload_image_button.clicked.connect(self.openFileNameDialog)

        save_button = QPushButton("Save", self)
        save_button.resize(150, 50)
        save_button.move(self._x_axis, 350)
        save_button.clicked.connect(self.save)

        self.get_name()
        self.get_age()
        self.get_fname()
        self.get_mob()
        self.get_loc()
        self.show()
    
    def get_loc(self):
        """
        This method reads the input Location from text field in GUI.
        """
        self.loc_label = QLabel(self)
        self.loc_label.setText("Address:")
        self.loc_label.move(self._x_axis-50,150 )
        self.loc = QLineEdit(self)
        self.loc.move(self._x_axis,150 )

    def get_name(self):
        """
        This method reads the input name from text field in GUI.
        """
        self.name_label = QLabel(self)
        self.name_label.setText("Name:")
        self.name_label.move(self._x_axis-50, 100)
        self.name = QLineEdit(self)
        self.name.move(self._x_axis, 100)

    def get_age(self):
        """
        This method reads the age from text field in GUI.
        """
        self.age_label = QLabel(self)
        self.age_label.setText("Age:")
        self.age_label.move(self._x_axis-50, 200)

        self.age = QLineEdit(self)
        self.age.move(self._x_axis, 200)

    def get_fname(self):
        """
        This method reads Father's name from text field in GUI.
        """
        self.fname_label = QLabel(self)
        self.fname_label.setText("Father's\n Name:")
        self.fname_label.move(self._x_axis-50, 250)

        self.father_name = QLineEdit(self)
        self.father_name.move(self._x_axis, 250)

    def get_mob(self):
        """
        This method reads mob number from text field in GUI.
        """
        self.mob_label = QLabel(self)
        self.mob_label.setText("Parent \n Mobile:")
        self.mob_label.move(self._x_axis-50, 300)

        self.mob = QLineEdit(self)
        self.mob.move(self._x_axis, 300)

    def get_facial_points(self, image_url) -> list:
        """
        This method passes the base64 form iamge to get facialkey points.

        Returns
        -------
         list
        """
        URL = "http://localhost:8002/image"
        f = [("image", open(image_url, "rb"))]
        try:
            result = requests.post(URL, files=f)
            if result.status_code == 200:
                return json.loads(result.text)["encoding"]
            else:
                QMessageBox.about(self, "Error", "Couldn't find face in Image")
                return None
        except Exception as e:
            QMessageBox.about(self, "Error", "Couldn't connect to face encoding API")
            return None

    def openFileNameDialog(self):
        """
        This method is triggered on button click to select image.

        When an image is selected its local URL is captured.
        After which it is passed through read_image method.
        Then it is converted to base64 format and facial keypoints are
        generated for it.

        If keypoints are not found in the image then you'll get a dialogbox.
        """
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "jpeg file (*.jpeg)",
            options=options,
        )
        
        if self.fileName:
            self.key_points = self.get_facial_points(self.fileName)
            

    def get_entries(self):
        """
        A check to make sure empty fields are not saved.
        A case will be uniquely identified by these fields.
        """
        entries = {}
        if (
            self.age.text() != ""
            and self.mob.text() != ""
            and self.name != ""
            and self.father_name != ""
            and self.loc != ""
        ):
            entries["age"] = self.age.text()
            entries["name"] = self.name.text()
            entries["father_name"] = self.father_name.text()
            entries["loc"] = self.loc.text()
            entries["mobile"] = self.mob.text()
            return entries
        else:
            return None

    def save_to_db(self, entries):
        URL = "http://localhost:8000/new_case"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        byte_content = open(self.fileName, "rb").read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode("utf-8")
        entries["image"] = base64_string
        
        try:
            res = requests.post(URL, json.dumps(entries), headers=headers)
            if res.status_code == 200:
                QMessageBox.about(self, "Success", "Saved successfully")
            else:
                QMessageBox.about(self, "Error", "Something went wrong while saving")
        except Exception as e:
            QMessageBox.about(self, "Error", "Couldn't connect to database")

    def save(self):
        """
        Save method is triggered with save button on GUI.
        All the parameters are passed to a db methods whose task is to save
        them in db.
        If the save operation is successful then you'll get True as output and
        a dialog message will be displayed other False will be returned and
        you'll get appropriate message.
        """
        entries = self.get_entries()
        if entries:
            entries["face_encoding"] = self.key_points
            entries["submitted_by"] = self.user
            entries["case_id"] = generate_uuid()
            self.save_to_db(entries)
            output1 = train(self.user)
            output = match1()
            if output["status"]:
                result = output["result"]
                self.view_cases(result)
                
        else:
            QMessageBox.about(self, "Error", "Please fill all entries")

    def view_cases(self, result):
        list_ = QListView(self)
        list_.setIconSize(QSize(96, 96))
        list_.setMinimumSize(400, 380)
        list_.move(40, 40)
        model = QStandardItemModel(list_)
        item = QStandardItem("Matched")
        model.appendRow(item)
        
        for case_id, submission_list in result.items():
            # Change status of Matched Case
            requests.get(
                f"http://localhost:8000/change_found_status?case_id='{case_id}'"
            )
            case_details = self.get_details(case_id, "case")
            for submission_id in submission_list:
                submission_details = self.get_details(
                    submission_id, "public_submission"
                )
                image = self.decode_base64(submission_details[0][3])

                
                item = QStandardItem(
                    
                    " Name: "
                    + submission_details[0][0]
                    + "\n Father's Name: "
                    + submission_details[0][1]
                    + "\n Phone number: "
                    + str(submission_details[0][4])
                    + "\n Address: "
                    + str(submission_details[0][2])
                    
                    # "\n Matched Date" + submission_details[0][1]
                )
                image = QtGui.QImage(
                    image,
                    image.shape[1],
                    image.shape[0],
                    image.shape[1] * 3,
                    QtGui.QImage.Format_RGB888,
                )
                icon = QPixmap(image)
                item.setIcon(QIcon(icon))
                model.appendRow(item)

        list_.setModel(model)
        list_.show()
    def get_details(self, case_id: str, type: str):
        URL = f"http://localhost:8000/get_case_details?case_id='{case_id}'"
        try:
            result = requests.get(URL)
            if result.status_code == 200:
                return json.loads(result.text)
            else:
                pass
        except Exception as e:
            raise e
    def decode_base64(self, img: str):
        """
        Image is converted ot numpy array.
        """
        img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
        return img

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = NewCase("admin")
    sys.exit(app.exec())

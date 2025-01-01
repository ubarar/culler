import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt, QTimer, QByteArray
from PIL import Image, ExifTags

from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox
import rawpy
import os
import io
import time

def rotate_image_based_on_exif(image):
    try:
        exif = image.getexif()
        exif = {
            ExifTags.TAGS.get(k, k): v
            for k, v in exif.items()
        }

        orientation = exif.get('Orientation')
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Error processing EXIF data: {e}")
    return image

def getPreview(path):
    with rawpy.imread(path) as raw:
        thumb = raw.extract_thumb()
        if thumb.format == rawpy.ThumbFormat.JPEG:
            img = Image.open(io.BytesIO(thumb.data))
            img = rotate_image_based_on_exif(img)
            output = io.BytesIO()
            img.save(output, format='JPEG')
            w, h = img.size
            return (output.getvalue(), w, h)
        else:
            return None

def deleteFiles(files):
    for file in files:
        os.remove(file)
    QApplication.quit()


class Reviewer(QtWidgets.QWidget):
    def __init__(self, images):
        super().__init__()

        self.images = images
        self.current = -1

        self.setWindowTitle("Cull Images")
        
        # Create a label to hold the image
        self.image_label = QLabel()

        # Instructions
        self.text_label = QLabel("Press D to delete the current image, press any other key to continue")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAlignment(Qt.AlignCenter)
        

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.toDelete = set()

        self.advance()

    def setImage(self, index):
        pixmap = QPixmap()
        img, w, h = getPreview(self.images[index])
        pixmap.loadFromData(img)
        newHeight = 750
        scaled = pixmap.scaled(QSize((w/h)*newHeight,newHeight), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image_label.setPixmap(scaled)


    def advance(self):
        if self.current == len(self.images) - 1:
            return False

        self.current += 1
        self.setImage(self.current)

        if self.images[self.current] in self.toDelete:
            self.setStyleSheet("background-color: red;")
        else:
            QTimer.singleShot(50, lambda : self.setStyleSheet(""))

        return True

    def previous(self):
        if self.current == 0:
            return False

        self.current -= 1
        self.setImage(self.current)

        if self.images[self.current] in self.toDelete:
            self.setStyleSheet("background-color: red;")
        else:
            QTimer.singleShot(50, lambda : self.setStyleSheet(""))

        return True

    def redo(self):
        self.current = 0
        self.setImage(self.current)

    def showConfirmationDialog(self):
        self.setStyleSheet("")
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText(f"You're choosing to delete {len(self.toDelete)} files. Proceed?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg_box.exec()

        if response == QMessageBox.Yes:
            deleteFiles(self.toDelete)

    def flashRedBackground(self):
        self.setStyleSheet("background-color: red;")
        QTimer.singleShot(50, lambda : self.setStyleSheet(""))

    def flashGreenBackground(self):
        self.setStyleSheet("background-color: green;")
        QTimer.singleShot(100, lambda : self.setStyleSheet(""))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_D:
            self.flashRedBackground()
            self.toDelete.add(self.images[self.current])
        if event.key() == Qt.Key.Key_K:
            self.flashGreenBackground()
            if self.images[self.current] in self.toDelete:
                self.toDelete.remove(self.images[self.current])
            pass

        if event.key() in [Qt.Key.Key_D, Qt.Key.Key_K, Qt.Key.Key_Right] and not self.advance():
            self.showConfirmationDialog()
            self.redo()
            return

        if event.key() == Qt.Key.Key_Left:
            self.previous()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    diag = QtWidgets.QFileDialog()
    diag.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
    if diag.exec():
        chosen_files = diag.selectedFiles()
        chosen_files.sort(reverse=True)

        reviewer  = Reviewer(chosen_files)
        reviewer.show()

    sys.exit(app.exec())
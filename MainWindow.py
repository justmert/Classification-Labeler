# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import os
from posix import listdir
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from os.path import isfile, join
from PyQt5.QtGui import QPixmap, QIcon
from functools import partial


class Volume():
    def __init__(self, volume, jpgs):
        self.volume = volume
        self.jpgs = jpgs


class Manga():
    def __init__(self, manga, volumes):
        self.manga = manga
        self.volumes = volumes


class Ui_MainWindow(object):

    def __init__(self, old_root, new_root):
        super().__init__()
        self.mangas = []
        self.current_img = None
        self.old_root = old_root
        self.new_root = new_root
        self.current_icon = None
        self.volume_count = 0
        self.manga_count = 0
        self.jpg_count = 0
        self.undo = []
        self.is_undo = False
        self.waitlist = []

    def set_info_labels(self, manga_name, volume_name, jpg_name):
        self.manga_name_label.setText(
            os.path.join(manga_name, volume_name, jpg_name))
        self.percent_label.setText(
            f'{self.jpg_count + 1}/{len(self.mangas[self.manga_count].volumes[self.volume_count].jpgs)}')
        self.manga_name_label.adjustSize()

    def button_clicked_undo(self):
        self.is_undo = True
        self.waitlist.insert(-1, self.undo[-1])
        self.listWidget.takeItem(0)
        pixmap = QPixmap(self.undo[-1])
        self.img_label.setPixmap(pixmap)
        self.img_label.resize(150, 150)
        self.undo.pop()

    def button_clicked(self, sending_button):
        if self.waitlist:
            try:
                old_root, manga_name, volume_name, label_name, jpg_name = self.waitlist[0].split(
                    '/')
                self.current_img = self.waitlist[0]
                del self.waitlist[0]
                self.is_undo = True
            except:
                print('split errorqqqq')
        else:
            try:
                old_root, manga_name, volume_name, jpg_name = self.current_img.split(
                    '/')
            except:
                print('split erroreeee')

        middle = os.path.join(manga_name, volume_name)
        funcname = sending_button.text().lower()
        upped = funcname.upper()

        if funcname == 'shock/surprised':
            funcname = 'shock'

        elif funcname == 'delete':
            funcname = 'deformed'

        elif funcname == "don't know":
            funcname = 'pass'

        elif funcname == 'any of these':
            funcname = 'unclassified'

        item = QtWidgets.QListWidgetItem(f"{jpg_name} • {upped}")
        item.setIcon(QIcon(self.current_img))
        self.listWidget.insertItem(-1, item)

        img_new_path = os.path.join(self.new_root, middle, funcname, jpg_name)
        os.rename(self.current_img, img_new_path)

        if self.is_undo:
            pass
        else:
            self.jpg_count += 1

            if self.manga_count == len(self.mangas):
                print('ALL COMPLETED')
                return

            if len(self.mangas[self.manga_count].volumes[self.volume_count].jpgs) == self.jpg_count:
                self.jpg_count = 0
                self.volume_count += 1

            if len(self.mangas[self.manga_count].volumes) == self.volume_count:
                self.jpg_count = 0
                self.manga_count += 1
        try:
            if self.waitlist:
                next_pic = self.waitlist[0]
            else:
                next_pic = self.mangas[self.manga_count].volumes[self.volume_count].jpgs[self.jpg_count]

            self.current_img = next_pic
            if not self.waitlist:
                old_root, manga_name, volume_name, jpg_name = self.current_img.split('/')
                self.set_info_labels(manga_name, volume_name, jpg_name)
        except:
            print('YOUR FUNCTION IS ERRORIUS')
        pixmap = QPixmap(next_pic)
        self.img_label.setPixmap(pixmap)
        self.img_label.resize(150, 150)
        self.undo.append(img_new_path)
        self.is_undo = False
        print('new_path', img_new_path)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(590, 570)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupbox.setGeometry(QtCore.QRect(20, 40, 551, 271))
        self.groupbox.setObjectName("groupbox")
        self.button_happy = QtWidgets.QPushButton(self.groupbox)
        self.button_happy.setGeometry(QtCore.QRect(20, 50, 131, 34))
        self.button_happy.setObjectName("button_happy")
        self.button_happy.clicked.connect(
            partial(self.button_clicked, self.button_happy))

        self.button_pleased = QtWidgets.QPushButton(self.groupbox)
        self.button_pleased.setGeometry(QtCore.QRect(20, 170, 131, 34))
        self.button_pleased.setObjectName("button_pleased")
        self.button_pleased.clicked.connect(
            partial(self.button_clicked, self.button_pleased))

        self.button_agry = QtWidgets.QPushButton(self.groupbox)
        self.button_agry.setGeometry(QtCore.QRect(20, 110, 131, 34))
        self.button_agry.setObjectName("button_agry")
        self.button_agry.clicked.connect(
            partial(self.button_clicked, self.button_agry))

        self.button_shock = QtWidgets.QPushButton(self.groupbox)
        self.button_shock.setGeometry(QtCore.QRect(390, 50, 131, 34))
        self.button_shock.setObjectName("button_shock")
        self.button_shock.clicked.connect(
            partial(self.button_clicked, self.button_shock))

        self.button_embarrassed = QtWidgets.QPushButton(self.groupbox)
        self.button_embarrassed.setGeometry(QtCore.QRect(390, 110, 131, 34))
        self.button_embarrassed.setObjectName("button_embarrassed")
        self.button_embarrassed.clicked.connect(
            partial(self.button_clicked, self.button_embarrassed))

        self.button_unclassified = QtWidgets.QPushButton(self.groupbox)
        self.button_unclassified.setGeometry(QtCore.QRect(350, 220, 111, 34))
        self.button_unclassified.setObjectName("button_unclassified")
        self.button_unclassified.clicked.connect(
            partial(self.button_clicked, self.button_unclassified))

        self.button_pass = QtWidgets.QPushButton(self.groupbox)
        self.button_pass.setGeometry(QtCore.QRect(215, 220, 111, 34))
        self.button_pass.setObjectName("button_pass")
        self.button_pass.clicked.connect(
            partial(self.button_clicked, self.button_pass))

        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(20, 480, 111, 34))
        self.button_start.setObjectName("button_start")
        self.button_start.clicked.connect(
            partial(self.button_clicked, self.button_start))
        self.button_start.setHidden(True)

        self.button_deformed = QtWidgets.QPushButton(self.groupbox)
        self.button_deformed.setGeometry(QtCore.QRect(80, 220, 111, 34))
        self.button_deformed.setObjectName("button_deformed")
        self.button_deformed.clicked.connect(
            partial(self.button_clicked, self.button_deformed))

        self.button_neutral = QtWidgets.QPushButton(self.groupbox)
        self.button_neutral.setGeometry(QtCore.QRect(150, 10, 111, 34))
        self.button_neutral.setObjectName("button_neutral")
        self.button_neutral.clicked.connect(
            partial(self.button_clicked, self.button_neutral))

        self.button_crying = QtWidgets.QPushButton(self.groupbox)
        self.button_crying.setGeometry(QtCore.QRect(280, 10, 111, 34))
        self.button_crying.setObjectName("button_crying")
        self.button_crying.clicked.connect(
            partial(self.button_clicked, self.button_crying))

        self.button_sad = QtWidgets.QPushButton(self.groupbox)
        self.button_sad.setGeometry(QtCore.QRect(390, 170, 131, 34))
        self.button_sad.setObjectName("button_sad")
        self.button_sad.clicked.connect(
            partial(self.button_clicked, self.button_sad))

        self.button_undo = QtWidgets.QPushButton(self.centralwidget)
        self.button_undo.setGeometry(QtCore.QRect(440, 525, 131, 34))
        self.button_undo.setObjectName("button_undo")
        self.button_undo.clicked.connect(self.button_clicked_undo)

        self.img_label = QtWidgets.QLabel(self.groupbox)
        self.img_label.setGeometry(QtCore.QRect(195, 55, 58, 18))
        self.img_label.setObjectName("img_label")
        self.img_label.setScaledContents(True)
        self.img_label.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.img_label.setFixedSize(QtCore.QSize(150, 150))
        self.manga_name_label = QtWidgets.QLabel(self.centralwidget)
        self.manga_name_label.setGeometry(QtCore.QRect(20, 10, 58, 18))
        self.manga_name_label.setObjectName("manga_name_label")
        self.percent_label = QtWidgets.QLabel(self.centralwidget)
        self.percent_label.setGeometry(QtCore.QRect(510, 5, 100, 50))
        self.percent_label.setObjectName("percent_label")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 320, 551, 200))
        self.listWidget.setObjectName("listWidget")
        # self.listWidget.setHorizontalScrollMode()
        self.listWidget.setIconSize(QtCore.QSize(40, 40))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.groupbox.setTitle(_translate("MainWindow", "Labels"))
        self.button_happy.setText(_translate("MainWindow", "Happy"))
        self.button_pleased.setText(_translate("MainWindow", "Pleased"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.button_sad.setText(_translate("MainWindow", "Sad"))
        self.button_undo.setText(_translate("MainWindow", "Undo"))
        self.button_crying.setText(_translate("MainWindow", "Crying"))
        self.button_agry.setText(_translate("MainWindow", "Angry"))
        self.button_neutral.setText(_translate("MainWindow", "Neutral"))
        self.button_shock.setText(_translate("MainWindow", "Shock/Surprised"))
        self.button_embarrassed.setText(
            _translate("MainWindow", "Embarrassed"))
        self.button_unclassified.setText(
            _translate("MainWindow", "any of these"))
        self.button_pass.setText(_translate("MainWindow", "don't know"))
        self.button_deformed.setText(_translate("MainWindow", "DELETE"))
        self.img_label.setText(_translate("MainWindow", "TextLabel"))
        self.manga_name_label.setText(_translate("MainWindow", "TextLabel"))
        self.percent_label.setText(_translate("MainWindow", "TextLabel"))

    def create_dir_structure(self, input_path, output_path):
        for dirpath, dirnames, filenames in os.walk(input_path):
            structure = os.path.join(
                output_path, os.path.relpath(dirpath, input_path))
            if not os.path.isdir(structure):
                Path(structure).mkdir(parents=True, exist_ok=True)

    def create_label_directories(self, output_path):
        list_subfolders_with_paths = [
            f.path for f in os.scandir(output_path) if f.is_dir()]
        for manga in list_subfolders_with_paths:
            volumes = [f.path for f in os.scandir(manga) if f.is_dir()]
            if volumes:
                for volume in volumes:
                    for label in ['happy', 'sad', 'neutral', 'crying',
                                  'angry', 'pleased', 'deformed', 'pass', 'unclassified', 'shock', 'embarrassed']:
                        Path(os.path.join(volume, label)).mkdir(
                            parents=True, exist_ok=True)

    def manga_dirs(self, input_path):
        list_subfolders_with_paths = [
            f.path for f in os.scandir(input_path) if f.is_dir()]
        for manga in list_subfolders_with_paths:
            volumes = [f.path for f in os.scandir(manga) if f.is_dir()]
            if volumes:
                all_volumes = []
                for volume in volumes:
                    filelist = [os.path.join(volume, file)
                                for file in os.listdir(volume)]
                    if not filelist:
                        continue
                    vol = Volume(volume, filelist)
                    all_volumes.append(vol)

            if not all_volumes:
                continue
            man = Manga(manga, all_volumes)
            self.mangas.append(man)

    def process(self):
        try:
            for item in self.mangas[self.manga_count].volumes:
                print(item.volume)
            picture = self.mangas[self.manga_count].volumes[self.volume_count].jpgs[self.jpg_count]
            self.current_img = picture
        except:
            print('INDEX ERROR, ARE THERE ANY IMAGE IN CONTENT DIR ?')
        pixmap = QPixmap(picture)
        self.img_label.setPixmap(pixmap)
        self.img_label.resize(60, 60)
        try:
            old_root, manga_name, volume_name, jpg_name = self.current_img.split(
                '/')
        except:
            print('split error')
        self.set_info_labels(manga_name, volume_name, jpg_name)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow('content', 'destination')
    ui.setupUi(MainWindow)
    ui.create_dir_structure('content', 'destination')
    ui.create_label_directories('destination')
    ui.manga_dirs('content')
    MainWindow.show()
    ui.process()
    sys.exit(app.exec_())

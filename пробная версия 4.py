from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
from PyQt5.uic import loadUi
import sys
import numpy
from numpy import dot
from numpy.linalg import norm 
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Программа для автоматической классификации состояния сложных технических систем")
        Dialog.resize(830,420)
        Dialog.setMaximumSize(830,420)
        Dialog.setMinimumSize(830,420)
        
        self.filename = QtWidgets.QLineEdit(Dialog)
        self.filename.setGeometry(QtCore.QRect(50, 60, 200, 30))

        self.second_filename = QtWidgets.QLineEdit(Dialog)
        self.second_filename.setGeometry(QtCore.QRect(480, 60, 200, 30))

        self.browse = QtWidgets.QPushButton(Dialog)
        self.browse.setGeometry(QtCore.QRect(270, 60, 80, 30))

        self.browse2 = QtWidgets.QPushButton(Dialog)
        self.browse2.setGeometry(QtCore.QRect(700, 60, 80, 30))

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(375, 110, 90, 30))

        self.filename_2 = QtWidgets.QLineEdit(Dialog)
        self.filename_2.setGeometry(QtCore.QRect(215, 215, 400, 25)) 

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(220, 213, 400, 30)) 

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(500, 300, 200, 35))

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 300, 200, 35))
        
        self.filename.raise_()
        self.second_filename.raise_()
        self.browse.raise_()
        self.browse2.raise_()
        self.pushButton_3.raise_()
        self.filename_2.raise_()
        self.label_2.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Программа для автоматической классификации состояния сложных технических систем")) #менять название
        self.browse.setText(_translate("Dialog", "Найти"))
        self.browse2.setText(_translate("Dialog", "Найти"))
        self.pushButton_3.setText(_translate("Dialog", "Рассчитать"))
        self.label_2.setText(_translate("Dialog", "Результат:"))
        self.pushButton.setText(_translate("Dialog", "Подробнее о результате"))
        self.pushButton_2.setText(_translate("Dialog", "Показать в пространстве"))

class Program(QMainWindow):
    def __init__(self):
        self.Error1 = True
        self.Error2 = True
        super().__init__()

    def get(self, mode):
        try:
            list=QFileDialog.getOpenFileName()[0]
            df=pd.read_excel(list, sheet_name=0, header=None)
            matrix=df.to_numpy()
            if mode == 0:
                self.A = numpy.array(matrix)
                self.label1=ui.filename.setText(list)
                self.Error1 = False
            elif (mode == 1):
                self.B = numpy.array(matrix)
                self.label2=ui.second_filename.setText(list)
                self.Error2 = False
            
        except ValueError:
            if mode == 0:
                self.A=numpy.array([0,0,0])
                self.label1=ui.filename.setText("Неверный формат файла")
                self.Error1= True
            elif (mode == 1):
                self.B=numpy.array([0,0,0])
                self.label2=ui.second_filename.setText("Неверный формат файла")
                self.Error2 = True
        except FileNotFoundError:
            if mode == 0:
                self.A=numpy.array([0,0,0])
                self.Error1= True
            elif (mode == 1):
                self.B=numpy.array([0,0,0])
                self.Error2 = True

    def schet(self):
        if self.checkErrors():
            U, self.D, VT=numpy.linalg.svd(self.A)
            U2, self.D2, VT2=numpy.linalg.svd(self.B)
            print("D", self.D)
            print("D2", self.D2)
            self.result = dot(self.D, self.D2)/(norm(self.D)*norm(self.D2))
            self.result2 = norm(self.D2)-norm(self.D)
            self.result3 = norm(self.D-self.D2)
            print(self.result, self.result2, self.result3)
            self.defec()    

    def paint(self):
        if self.checkErrors():
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

            ax.set_xlim3d(-15,15)
            ax.set_ylim3d(-15,15)
            ax.set_zlim3d(-15,15)

            Point = numpy.array([self.result,self.result2,self.result3])
            start=[0,0,0]

            plt.plot(Point[0], Point[1], Point[2], 'or')
            ax.quiver(start[0],start[1],start[2],self.D[0],self.D[1],self.D[2])
            ax.quiver(start[0],start[1],start[2],self.D2[0],self.D2[1],self.D2[2],color="r")
            plt.show()

    def defec(self):
        defect=""
        if self.result<=0.85 and self.result>=0.7 and self.result2<=4.5 and self.result2>=3 and self.result3<=10 and self.result3>=5 :
            defect="Дефект 1"
        elif self.result<=0.85 and self.result>=0.7 or self.result2<=4.5 and self.result2>=3 or self.result3<=10 and self.result3>=5:
            defect='Дефект 1 зарождается'
        elif self.result>=0.985 and self.result<=1.1 and self.result2<=0.6 and self.result3<=1:
            defect="Идеально исправен"
        else:
            defect="Исправен с незначительным дефектом"
        self.label3=ui.filename_2.setText(f"                   {defect}")
        print(defect)

    def butt(self):
        self.temp=ui.browse.clicked.connect(lambda: self.get(0))
        self.address= ui.browse2.clicked.connect(lambda: self.get(1))
        self.but3=ui.pushButton_3.clicked.connect(self.schet)
        self.but2=ui.pushButton_2.clicked.connect(self.paint)
        self.but5=ui.pushButton.clicked.connect(self.show_new_window)

    def show_new_window(self, checked):
        if self.checkErrors():
            self.w = AnotherWindow()
            self.defec()
            self.w.show()

    def checkErrors(self):
        if not(self.Error1 or self.Error2):
            return True
        else:
            self.label3=ui.filename_2.setText("                   Ошибка")
            return False

class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("C:\dont_reload\photo.jpg"))) #установить путь к фону
    Dialog.setPalette(palette)
    Dialog.show()
    program = Program()
    program.butt()
    sys.exit(app.exec())
#from PyQt5 import QtCore, QtGui, QtWidgets
import typing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5.uic import loadUi
import sys
import numpy
from numpy import dot
from numpy.linalg import norm 
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import math

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт")
        self.setGeometry(100,100,704,367)
        self.UiComponents()
        self.show()
    
    
    def UiComponents(self):
        global filename
        global filename2
        global filename_2

        label=QLabel(self)
        pixmap=QPixmap("sheep.jpg")
        label.setGeometry(-130, -57, 901, 961)
        label.setPixmap(pixmap)
        
        filename=QLineEdit(self)
        filename.setGeometry(30, 60, 201, 31)        
        
        browse=QPushButton("Найти",self)
        browse.setGeometry(250, 60, 61, 21)
        browse.clicked.connect(self.get)

        filename2=QLineEdit(self)
        filename2.setGeometry(340, 60, 201, 31)

        browse2=QPushButton("Найти",self)
        browse2.setGeometry(560, 60, 61, 21)
        browse2.clicked.connect(self.get2)

        pushButton_3=QPushButton("Рассчитать",self)
        pushButton_3.setGeometry(300, 120, 141, 41)
        pushButton_3.clicked.connect(self.schet)
        pushButton_3.clicked.connect(self.defec)

        filename_2=QLineEdit("Результат:",self)
        filename_2.setGeometry(240, 190, 260, 51)

        pushButton_2=QPushButton("Показать в пространстве",self)
        pushButton_2.setGeometry(130, 300, 201, 31)
        pushButton_2.clicked.connect(self.paint)

        pushButton=QPushButton("Подробнее о результате",self)
        pushButton.setGeometry(370, 300, 221, 31)
        pushButton.clicked.connect(self.show_Window2)
        

    def get (self):
        global A
        global list1
        list1=QFileDialog.getOpenFileName()[0]
        df=pd.read_excel(list1, sheet_name=0, header=None)
        matrix=df.to_numpy()
        A = numpy.array(matrix)
        filename.setText(list1)


    def get2 (self):
        global B
        global list2
        list2=QFileDialog.getOpenFileName()[0]
        second_df=pd.read_excel(list2, sheet_name=0, header=None)
        second_matrix=second_df.to_numpy()
        B = numpy.array(second_matrix)
        filename2.setText(list2)

    def schet(self):
        global result
        global result2
        global result3
        global D
        global D2
        U, D, VT=numpy.linalg.svd(A)
        U2, D2, VT2=numpy.linalg.svd(B)
        print("D", D)
        print("D2", D2)
        result = dot(D, D2)/(norm(D)*norm(D2))
        result2 = norm(D2)-norm(D)
        result3 = norm(D-D2)
        print(result, result2, result3)
    
    
    def paint(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        ax.set_xlim3d(-15,15)
        ax.set_ylim3d(-15,15)
        ax.set_zlim3d(-15,15)

        Point = numpy.array([result,result2,result3])
        start=[0,0,0]

        plt.plot(Point[0], Point[1], Point[2], 'or')
        ax.quiver(start[0],start[1],start[2],D[0],D[1],D[2])
        ax.quiver(start[0],start[1],start[2],D2[0],D2[1],D2[2],color="r")
        plt.show()
    
    def show_Window2(self):
        self.window2=Window2()
        self.window2.show()
    
    def defec(self):
        global defect
        defect=""
        if result<=0.85 and result>=0.7 and result2<=4.5 and result2>=3 and result3<=10 and result3>=5 :
            defect="Дефект 1"
        elif result<=0.85 and result>=0.7 or result2<=4.5 and result2>=3 or result3<=10 and result3>=5:
            defect='Дефект 1 зарождается'
        elif result>=0.985 and result<=1.1 and result2<=0.6 and result3<=1:
            defect="Идеально исправен"
        else:
            defect="Исправен с незначительным дефектом"
        filename_2.setText(f"Результат: {defect}")

class Window2(QWidget):
    def __init__(self):
        global filename_3

        super().__init__()
        self.setWindowTitle("Подробный результат")

        """label=QLabel(self)
        pixmap=QPixmap("sheep.jpg")
        label.setGeometry(-130, -57, 901, 961)
        label.setPixmap(pixmap)"""

        filename_3=QLineEdit(self)
        filename_3.setGeometry(240, 190, 300, 40)
        filename_3.setText(f"cos {result}")

        filename_32=QLineEdit(self)
        filename_32.setGeometry(240, 230, 300, 40)
        filename_32.setText(f"разница длин {result2}")

        filename_33=QLineEdit(self)
        filename_33.setGeometry(240, 270, 300, 40)
        filename_33.setText(f"расстояние {result3}")

        
if __name__ == "__main__":
    App=QApplication(sys.argv)
    window=Window()
    window.show()
    sys.exit(App.exec())
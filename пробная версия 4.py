import PyQt5
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
import sys
import numpy
from numpy import dot
from numpy.linalg import norm 
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x=loadUi('C:\dont_reload\gui.ui')
        self.x.show()
        

    def get(self):
        list1=QFileDialog.getOpenFileName()[0]
        df=pd.read_excel(list1, sheet_name=0, header=None)
        matrix=df.to_numpy()
        self.A = numpy.array(matrix)
        self.label1=self.x.filename.setText(list1)
     
    def get2(self):
        list2=QFileDialog.getOpenFileName()[0]
        second_df=pd.read_excel(list2, sheet_name=0, header=None)
        second_matrix=second_df.to_numpy()
        self.B = numpy.array(second_matrix)
        self.label2=self.x.file2.setText(list2)

    def schet(self):
        U, self.D, VT=numpy.linalg.svd(self.A)
        U2, self.D2, VT2=numpy.linalg.svd(self.B)
        print("D", self.D)
        print("D2", self.D2)
        self.result = dot(self.D, self.D2)/(norm(self.D)*norm(self.D2))
        self.result2 = norm(self.D2)-norm(self.D)
        self.result3 = norm(self.D-self.D2)
        print(self.result, self.result2, self.result3)

    def paint(self):
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
        self.label3=self.x.filename_2.setText(f"Результат: {defect}")
        print(defect)


    def butt(self):
        self.temp=self.x.browse.clicked.connect(self.get)
        self.address= self.x.browse2.clicked.connect(self.get2)
        self.but3=self.x.pushButton_3.clicked.connect(self.schet)
        self.but3=self.x.pushButton_3.clicked.connect(self.defec)
        self.but2=self.x.pushButton_2.clicked.connect(self.paint)
        self.but4=self.x.pushButton.clicked.connect(self.defec)
        # self.but5=self.x.pushButton.clicked.connect(self.second_window)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = Program()
    temp = ''
    destination = ''
    # program.show()
    program.butt()
    sys.exit(app.exec())
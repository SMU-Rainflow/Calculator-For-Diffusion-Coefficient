import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from target import *
import PyQt5.sip
import pandas as pd
import math

df=pd.read_excel(".\扩散系数.xlsx")

def get_Info(name):
    return list(map(float,[df[df["种类"]==name]["A"],df[df["种类"]==name]["E"],df[df["种类"]==name]["M"]]))
def OMG_D(k,T,Eij):
    x1=1.06036/(((k*T)/Eij)**0.1561)
    x2=0.193/math.exp((0.47635*k*T)/Eij)
    x3=1.03587/math.exp((1.52996*k*T)/Eij)
    x4=1.76474/math.exp((3.89411*k*T)/Eij)
    return x1+x2+x3+x4

def E_ij(E1,E2):
    Eij=(E1*E2)**0.5
    return Eij
    
def Dij(P,T,M1,M2,A1,A2,E1,E2):
    #P=P*(10**5)
    #A1=A1*(10**-8)
    #A2=A2*(10**-8)
    k=1
    #k=1.380649e-23
    Eij=E_ij(E1,E2)
    OMGd=OMG_D(k,T,Eij)
    
    w1=0.00266
    TT=T**1.5
    FenZi=w1*TT

    FenMu=(((2*M1*M2)/(M1+M2))**0.5)*(((A1+A2)/2)**2)*P*OMGd
    result=FenZi/FenMu
    print("OMGD=",OMGd)
    print("OMGD=",((2*M1*M2)/(M1+M2))**0.5)#排除
    print("OMGD=",((A1+A2)/2)**2)
    return result

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("二元扩散系数计算")
        self.BTN1.clicked.connect(self.BTN1_click)
        self.BTN2.clicked.connect(self.BTN2_click)

    def BTN1_click(self):
        T1n=float(self.T1.toPlainText())
        P1n=float(self.P1.toPlainText())
        M1n=float(self.M1.toPlainText())
        A1n=float(self.A1.toPlainText())
        E1n=float(self.E1.toPlainText())
        M2n=float(self.M2.toPlainText())
        A2n=float(self.A2.toPlainText())
        E2n=float(self.E2.toPlainText())
        result=Dij(P1n,T1n,M1n,M2n,A1n,A2n,E1n,E2n)
        self.RES1.setPlainText(str(result))

    def BTN2_click(self):
        T2n=float(self.T2.toPlainText())
        P2n=float(self.P2.toPlainText())
        name1=self.NAME1.toPlainText()
        name2=self.NAME2.toPlainText()
        TEMP1=get_Info(name1)
        TEMP2=get_Info(name2)
        M1n=float(float(TEMP1[2]))
        A1n=float(float(TEMP1[0]))
        E1n=float(float(TEMP1[1]))
        M2n=float(float(TEMP1[2]))
        A2n=float(float(TEMP1[0]))
        E2n=float(float(TEMP1[1]))

        result=Dij(P2n,T2n,M1n,M2n,A1n,A2n,E1n,E2n)
        self.RES2.setPlainText(str(result))


    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

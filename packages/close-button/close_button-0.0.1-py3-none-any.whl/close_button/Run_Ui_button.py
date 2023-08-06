""" import sys
import button 
from PyQt5.Qtwidgets import QApplication,QMainwindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Mainwindow = QMainwindow()
    ui = button.ui_Mainwindow()
    ui.setupui(Mainwindow)
    Mainwindow.show()
    sys.exit(app.exec_()) """
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from Ui_button import Ui_MainWindow  #导入你写的界面类
 
 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    button = MyMainWindow()
    button.show()
    sys.exit(app.exec_())    
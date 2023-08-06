'''
这是实现将各种图片转化为pdf的功能
NowFile为判断程序是否执行完毕的

'''
# -*- coding: utf-8 -*-
import os
try:
    from Ui.PicToPdfUi import Ui_PicToPdf
except:
    from .Ui.PicToPdfUi import Ui_PicToPdf
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import  *
try:
    from Function.imgToPdf import img2pdf_all2one, img2pdf_all2all
except:
    from .Function.imgToPdf import img2pdf_all2one, img2pdf_all2all
from PyQt5 import QtCore, QtGui, QtWidgets
from clazz import demo


style =  '''
    QPushButton#btn1 {
    height: 50px;
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #8a9195, stop: 1 balck);
    color: white;
    border-radius: 5px;
    font-size: 20px;
    font-weight:bold;
}

QPushButton#btn1:hover {
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #7d8488, stop: 1 balck);
}

QPushButton#btn1:pressed {
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #6a7073, stop: 1 balck);
}

QPushButton#btn2 {
    height: 50px;
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #47a7ed, stop: 1 #a967b2);
    color: white;
    border-radius: 25px;
    font-size: 20px;
    font-weight:bold;

}

QPushButton#btn2:hover {
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #459ee0, stop: 1 #995da1);
}

QPushButton#btn2:pressed {
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #4093d1, stop: 1 #87538e);
}
'''

class PicToPdf(QWidget, Ui_PicToPdf, demo.TableObject):
    NowFile  = pyqtSignal(str)
    ProBarSignal = pyqtSignal(float)
    def __init__(self, communication=None, token = ""):
        super(PicToPdf, self).__init__(communication)
        self.setupUi(self)
        self.NowFile.connect(self.isFinish)
        self.StartBtn.clicked.connect(self.printFileName)
        self.PdfDisVisible()
        self.FilePathBtn.clicked.connect(self.setFilePath)
        self.PdfSaveBtn.clicked.connect(self.setFilePath)
        self.OnePdfcheckBox.clicked.connect(self.SaveOnePdf)
        self.ProBarSignal.connect(self.ProcessBarFun)
        self.HideTip()
        self.pic_name_list = ['.jpg', '.png', '.bmp', '.jpeg', '.JPG', '.PNG', '.JPEG', ".tiff", ".fit"]
        self.setStyleSheet(style)
        self.FunctionName = "将图片文件转化为pdf文件"
        self.describetion = '''
    =================================================
    这是将图片文件转化为pdf文件的功能
    =================================================
        '''

    #进度条
    def ProcessBarFun(self, num):
        print("进度条进度值",end="")
        print(num)
        if num < 1.1:
            self.progressBar.setValue(int(num * 100))
        else:
            # self.BarText.setVisible(True)
            self.progressBar.setValue(100)
            self.progressBar.setTextVisible(False)

    #隐藏路径提示的框信息
    def HideTip(self):
        self.pdfPathTip.setVisible(False)
        self.picPathTip.setVisible(False)
        self.pdfNameTip.setVisible(False)
        self.BarFinish.setVisible(False)

    def setFilePath(self):
        FileBtnName = self.sender().text()
        print(FileBtnName)
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")
        if download_path:
            if FileBtnName == "...":
                self.PdfSaveEdit.clear()
                self.PdfSaveEdit.setText(download_path)
            else:
                self.filePathEdit.clear()
                self.filePathEdit.setText(download_path)

    def SaveOnePdf(self):
        print("验证CheckBox的点击事件")
        if self.OnePdfcheckBox.isChecked():
            self.PdfVisible()
        else:
            self.PdfDisVisible()

    #设置PDF名字的label和PDF的Edit不可见
    def PdfDisVisible(self):
        self.PdfName.setVisible(False)
        self.PdfNameEdit.setVisible(False)
        self.StartBtn.setGeometry(QtCore.QRect(180, 375, 331, 31))
        self.progressBar.setGeometry(QtCore.QRect(100, 440, 521, 23))
        self.BarFinish.setGeometry(QtCore.QRect(340, 440, 421, 20))


    #设置PDF名字的label和PDF的Edit可见
    def PdfVisible(self):
        self.PdfName.setVisible(True)
        self.PdfNameEdit.setVisible(True)
        self.StartBtn.setGeometry(QtCore.QRect(180, 410, 331, 31))
        self.progressBar.setGeometry(QtCore.QRect(100, 470, 521, 23))
        self.BarFinish.setGeometry(QtCore.QRect(340, 470, 421, 20))

    def isFinish(self, fileName):
        print("这是主函数")
        print(fileName)
        if fileName == "执行完成":
            self.BarFinish.setVisible(True)
            self.progressBar.setTextVisible(False)

    def printFileName(self):

        self.HideTip()
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.PicPath = self.filePathEdit.text()
        self.PdfPath = self.PdfSaveEdit.text()
        if not self.PicPath:
            print("图片文件路径为空!")
            self.picPathTip.setText("请输入图片所在路径!")
            self.picPathTip.setVisible(True)
            return

        if not os.path.exists(self.PicPath):
            print("图片路径不存在!")
            self.picPathTip.setText("图片路径不存在!")
            self.picPathTip.setVisible(True)
            return

        if not self.PdfPath:
            self.PdfPath = self.PicPath
            print("这是图片所在位置!")
            print(self.PdfPath)
        else:
            if not os.path.exists(self.PdfPath):
                self.pdfPathTip.setText("保存PDF文件的路径不存在!")
                self.pdfPathTip.setVisible(True)
                return

        #判断保存为单个PDF勾选框，是否处于勾选状态。且设置要保存的单个PDF文件的名字
        if self.OnePdfcheckBox.isChecked():
            OnePdfName = self.PdfNameEdit.text()
            if not OnePdfName:
                self.pdfNameTip.setText("请输入保存为PDF的名字!")
                self.pdfNameTip.setVisible(True)
            else:
                print("保存的PDF的名字")
                print(OnePdfName)
                PdfPathLen = len(os.path.join(self.PdfPath, OnePdfName))
                print(PdfPathLen)
                print(os.path.join(self.PdfPath, OnePdfName))
                #判断保存PDF文件名的长度是否大于255
                if PdfPathLen > 250:
                    QMessageBox.information(self, "warning" , "文件路径过长")
                else:
                    self.runThread = RunThread(self, self.PicPath, self.PdfPath, self.pic_name_list, OnePdfName)
                    self.runThread.start()

        else:
            print("保存成为多个PDF")

            self.runThread = RunThread(self, self.PicPath, self.PdfPath, self.pic_name_list)
            self.runThread.start()

    #获取路径
    # def getCantList(self, path, NewLen):



#这是运行的主线程
class RunThread(QThread):
    ThreadSignal = pyqtSignal(str)
    PBarSignal = pyqtSignal(float)
    def __init__(self, communication, img_path, pdf_path, pic_name_list, pdfName = ""):
        super(RunThread, self).__init__()
        self.communication = communication
        self.ThreadSignal.connect(self.ReturnPdfPath)
        self.img_path = img_path
        self.pdf_path = pdf_path
        self.pic_name_list = pic_name_list
        self.pdfName = pdfName
        self.PBarSignal.connect(self.PBarFun)

    def PBarFun(self, num):
        self.communication.ProBarSignal.emit(num)

    # ProBarSignal
    def run(self):
        # img_path = r"F:\20210917\下载完\新建文件夹 - 副本\2019-1至2019-17"
        # # 图片输出文件夹路径
        # pdf_path = r"F:\20210917\下载完\新建文件夹 - 副本\2019-1至2019-17"
        # pic_name_list = ['.jpg', '.png', '.bmp', '.jpeg', '.JPG', '.PNG', '.JPEG']
        img_path = self.img_path
        # 图片输出文件夹路径
        pdf_path = self.pdf_path
        pic_name_list = self.pic_name_list
        print(self.pdfName)
        if self.pdfName:
            print("——————————————————————————————————————————————————————————————————————")
            print("保存为多个")
            img2pdf_all2one(img_path, pic_name_list, pdf_path, self.pdfName + ".pdf", self)
        else:
            print("——————————————————————————————————————————————————————————————————————")
            print("保存为单个")
            img2pdf_all2all(img_path, pic_name_list, pdf_path, self)

    def ReturnPdfPath(self, filePath):
        self.communication.NowFile.emit(filePath)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = PicToPdf()
    myWin.show()
    sys.exit(app.exec_())
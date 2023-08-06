#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtWidgets
try:
    from Ui.WordToPdfUi import Ui_Form
except:
    from .Ui.WordToPdfUi import Ui_Form
from PyQt5.QtWidgets import *
import os,time,shutil
from win32com import client as wc
from PyQt5.QtCore import *
import traceback
import requests
import json
import sqlite3
import random
import pythoncom
from clazz import demo
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] =r'E:\000工作\NewPDfSplit\pyhton3864\Lib\site-packages\PyQt5\Qt5\plugins'
def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print(srcfile+'not exist!')
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
    return

def get_now():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))

class WordToPdf(QtWidgets.QWidget,Ui_Form, demo.TableObject):
    warningSignal = pyqtSignal(str, str)
    reloadSignal = pyqtSignal()
    ProBarSignal = pyqtSignal(float)
    def __init__(self,communication = None):
        super(WordToPdf,self).__init__()
        self.setupUi(self)
        self.communication = communication
        self.token = ""
        self.user = ""
        self.run_code = 1
        self.StartBtn.clicked.connect(self.StartWork)
        self.WordPathBtn.clicked.connect(self.setFilePath)
        self.HideFun()
        self.warningSignal.connect(self.showmsg)
        self.reloadSignal.connect(self.ReloadBtn)
        self.ProBarSignal.connect(self.ProcessBarFun)

    #进度条信号函数
    def ProcessBarFun(self, num):
        print("进度条进度值",end="")
        print(num)
        if num < 1:
            self.progressBar.setValue(int(num * 100))
        else:
            # self.BarText.setVisible(True)
            self.progressBar.setValue(100)
            self.progressBar.setTextVisible(False)
            self.Finishlabel.setVisible(True)

    #执行初始化，隐藏路径信息提示,以及执行完成信息提示。
    def HideFun(self):
        self.WordPathTip.setVisible(False)
        self.Finishlabel.setVisible(False)
        self.StartBtn.setText("开始转换")
        self.StartBtn.setEnabled(True)

    def setFilePath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览", "./")
        if download_path:
            self.WordPathEdit.clear()
            self.WordPathEdit.setText(download_path)

    def showmsg(self,t,msg):
        if(t == "warning"):
            # QMessageBox.warning(self,"Warining","没有需要保存的内容",QMessageBox.Ok)
            QMessageBox.warning(self,"Warining",msg,QMessageBox.Ok)
        if(t == "info"):
            QMessageBox.information(self,"info",msg,QMessageBox.Yes,QMessageBox.Yes)

    def getparam(self):
        # print("get params")
        self.根目录 = self.WordPathEdit.text()

    def get_url(self,urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    #开始执行时传递的id，和所需要记录的文本
    def checkToken(self,id,comments):
        try:
            self.urldb = os.path.join("./database", "url.db")
            if not os.path.exists(self.urldb):
                self.showmsg("warning","保存URl表不存在")
                self.run_code = 0
                return False

            headers = {
                "token": self.token
            }
            dbText = self.get_url("commit")
            print(1111111111111111)
            print(dbText)
            if dbText:
                url = dbText[0][1]

                body = {
                    "id": id,
                    "comments": "【开始执行：】  {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                if response.status_code != 200:

                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break

                        if num == 2:
                            self.communication.token_singal.emit()
                            self.run_code = 0
                        num += 1
                else:
                    print("更新成功")

            else:
                self.run_code = 0
                self.showmsg("warning", "保存OCR信息链接不存在")
        except:
            traceback.print_exc()

    # 完成执行时传递的id，和所需要记录的文本
    def checkToken1(self,id,comments):
        try:
            self.urldb = os.path.join("./database", "url.db")
            if not os.path.exists(self.urldb):
                self.showmsg("warning", "保存URl表不存在")
                self.run_code = 0
                return False
            headers = {
                "token": self.token
            }
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": id,
                    "comments": "【执行完成：】 {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)

                #判断响应的状态码是否为200， 不为200会进行三次尝试
                if response.status_code != 200:
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            self.communication.token_singal.emit()
                            self.run_code = 0
                        num += 1
                else:
                    print("更新成功")

        except:
            traceback.print_exc()


    #实现StartWork()函数，textEdit是我们放上去的文本框的id
    def StartWork(self):
        # self.checkToken(11, "PDF转Word")
        if self.run_code:
            self.true_run()

    def seTRuning(self):
        self.StartBtn.setText("正在执行")
        self.StartBtn.setDisabled(True)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.Finishlabel.setVisible(False)

    def true_run(self):
        self.seTRuning()
        # self.HideFun()
        self.textEdit.clear()
        self.getparam()

        print(self.根目录)
        if not self.根目录:
            self.WordPathTip.setText("请输入Word文件所在的文件夹！")
            self.WordPathTip.setVisible(True)
            self.StartBtn.setText("开始转换")
            self.StartBtn.setEnabled(True)
            return False

        if  not os.path.exists(self.根目录):
            self.WordPathTip.setText("文件夹位置不存在！")
            self.WordPathTip.setVisible(True)
            # self.textEdit.insertPlainText("Word文件路劲不存在\n")
            self.StartBtn.setText("开始转换")
            self.StartBtn.setEnabled(True)
            return False

        if not os.path.exists("./logg"):
            os.mkdir("./logg")

        self.textEdit.insertPlainText("正在执行！\n")

        self.thread1 = RunThread(self)
        self.thread1.start()

    def ReloadBtn(self):
        self.StartBtn.setText("开始转换")
        self.StartBtn.setEnabled(True)

class RunThread(QThread):
    def __init__(self, communication):
        super(RunThread, self).__init__()
        self.communication = communication

    def run(self):
        rootdir = self.communication.根目录  # 文件夹路径
        print(rootdir)
        start_time = get_now()
        words_to_pdfs_name = './logg/word批量转换pdf运行日志_' + str(start_time)
        with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
            file.write('[开始处理]' + str(get_now()) + "\n")
        pythoncom.CoInitialize()
        word = wc.Dispatch('Word.Application')  # 首先将doc转换成docx

        FinalSuccess = True
        try:
            f_list = []
            for parent, dirnames, filenames in os.walk(rootdir):
                for filename in filenames:
                    self.communication.ProBarSignal.emit(filenames.index(filename)/len(filenames))
                    print(filename)
                    with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                        file.write('[正在处理]读取到'+filename + str(get_now()) + "\n")
                    if u'.docx' in filename and u'~$' not in filename:
                        print('$$$$$$$$$$$$$$$$')
                        title = filename[:-5]  # 删除.docx
                        #                print(title)
                        f_list.append(filename)
                        print('PPPPPPPP')
                        ###########################问题所在##################################
                        # word.Visible = 0
                        ###########################问题所在##################################
                        print('A')
                        doc = word.Documents.Open(os.path.join(parent, filename))
                        print('B')
                        doc.SaveAs(os.path.join(parent, title + '.pdf'), 17)  # 直接保存为PDF文件
                        print('C')
                        doc.Close()
                        print('D')
                        os.remove(os.path.join(parent, filename))
                        print('E')
                        with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                            file.write('[正在处理]处理完成' + filename + str(get_now()) + "\n")
                        continue
                    if u'.doc' in filename and u'~$' not in filename:
                        title = filename[:-4]  # 删除.doc
                        #                print(title)
                        f_list.append(filename)
                        word.Visible = 0
                        doc = word.Documents.Open(os.path.join(parent, filename))
                        doc.SaveAs(os.path.join(parent, title + '.pdf'), 17)  # 直接保存为PDF文件
                        doc.Close()
                        os.remove(os.path.join(parent, filename))
                        with open(words_to_pdfs_name + '.txt', "a", encoding="utf8" ) as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                            file.write('[正在处理]处理完成' + filename + str(get_now()) + "\n")
            word.Quit()
            with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[处理完成]' + str(get_now()) + "\n")
        except Exception as e:
            traceback.print_exc()
            FinalSuccess = False
            word = wc.Dispatch('kwps.Application')
            with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[Error]' + str(get_now()) + "\n")
                file.write('[报错内容]' + str(e) + "\n")
                file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
            try:
                f_list = []
                os_dict = {root: [dirs, files] for root, dirs, files in os.walk(rootdir)}
                for parent, dirnames, filenames in os.walk(rootdir):
                    for filename in filenames:
                        print(filename)
                        self.communication.ProBarSignal.emit(filenames.index(filename) / len(filenames))
                        with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                            file.write('[正在处理]读取到'+filename + str(get_now()) + "\n")
                        if u'.docx' in filename and u'~$' not in filename:
                            print('$$$$$$$$$$$$$$$$')
                            title = filename[:-5]  # 删除.docx
                            #                print(title)
                            f_list.append(filename)
                            print('PPPPPPPP')
                            ###########################问题所在##################################
                            # word.Visible = 0
                            ###########################问题所在##################################
                            print('A')
                            doc = word.Documents.Open(os.path.join(parent, filename))
                            print('B')
                            doc.SaveAs(os.path.join(parent, title + '.pdf'), 17)  # 直接保存为PDF文件
                            print('C')
                            doc.Close()
                            print('D')
                            os.remove(os.path.join(parent, filename))
                            print('E')
                            with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                                file.write('[正在处理]处理完成' + filename + str(get_now()) + "\n")
                            continue
                        if u'.doc' in filename and u'~$' not in filename:
                            title = filename[:-4]  # 删除.doc
                            #                print(title)
                            f_list.append(filename)
                            word.Visible = 0
                            doc = word.Documents.Open(os.path.join(parent, filename))
                            doc.SaveAs(os.path.join(parent, title + '.pdf'), 17)  # 直接保存为PDF文件
                            doc.Close()
                            os.remove(os.path.join(parent, filename))
                            with open(words_to_pdfs_name + '.txt', "a", encoding="utf8" ) as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                                file.write('[正在处理]处理完成' + filename + str(get_now()) + "\n")
                word.Quit()
                FinalSuccess = True
                with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                    file.write('[处理完成]' + str(get_now()) + "\n")
            except Exception as Two:
                self.communication.reloadSignal.emit()
                self.communication.warningSignal.emit("warning", "未知错误")
                with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                    file.write('[Error]' + str(get_now()) + "\n")
                    file.write('[报错内容]' + str(Two) + "\n")
                    file.write('[报错源文件位置]' + str(Two.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                    file.write('[报错源码行数]' + str(Two.__traceback__.tb_lineno) + "\n")

        if not FinalSuccess:
            self.communication.reloadSignal.emit()
            self.communication.warningSignal.emit("warning", "Wps软件的word转pdf，和OfficeWord的word转pdf都发生错误，请确定是否安装wps和office")
        else:
            self.communication.ProBarSignal.emit(1)
            self.communication.reloadSignal.emit()
            self.communication.textEdit.insertPlainText("处理完成！\n")
            with open(words_to_pdfs_name + '.txt', "a", encoding="utf8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write('[处理完成]' + str(get_now()) + "\n")


        # self.checkToken1(11, "Word转PDf")

        # except:
        #     self.showmsg("warning", "参数不对，程序报错，请重新输入")
        #
        # else:
        #     self.textEdit.setPlainText('word替换为pdf可能成功了')
    # self.textEdit.insertPlainText("你点击了按钮\n")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = WordToPdf()
    my_pyqt_form.show()
    sys.exit(app.exec_())
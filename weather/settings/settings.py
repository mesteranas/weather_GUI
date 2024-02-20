import guiTools,update
import zipfile
import sys
import os,shutil
from . import settings_handler
from . import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class settings (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("settings"))
        layout=qt.QVBoxLayout()
        self.sectian=guiTools.listBook(layout,_("select sectian"))
        label=qt.QLabel(_("language"))
        self.language=qt.QComboBox()
        self.language.setAccessibleName(_("language"))
        self.language.addItems(language.lang().keys())
        languages = {index:language for language, index in enumerate(language.lang().values())}
        try:
            self.language.setCurrentIndex(languages[settings_handler.get("g","lang")])
        except Exception as e:
            self.language.setCurrentIndex(0)
        self.ExitDialog=qt.QCheckBox(_("Show exit dialog when exiting the program"))
        self.ExitDialog.setChecked(self.cbts(settings_handler.get("g","exitDialog")))
        UpdateLayout=qt.QVBoxLayout()
        self.update_autoDect=qt.QCheckBox(_("Automatically check for update when program start"))
        self.update_autoDect.setChecked(self.cbts(settings_handler.get("update","autoCheck")))
        UpdateLayout.addWidget(self.update_autoDect)
        self.update_beta=qt.QCheckBox(_("download beta updates"))
        self.update_beta.setChecked(self.cbts(settings_handler.get("update","beta")))
        UpdateLayout.addWidget(self.update_beta)
        self.update_check=qt.QPushButton(_("check for update"))
        self.update_check.clicked.connect(lambda:update.check(self))
        UpdateLayout.addWidget(self.update_check)
        self.ok=qt.QPushButton(_("OK"))
        self.ok.clicked.connect(self.fok)
        self.defolt=qt.QPushButton(_("default"))
        self.defolt.clicked.connect(self.default)
        self.cancel=qt.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.fcancel)
        layout1=qt.QVBoxLayout()
        layout1.addWidget(label)
        layout1.addWidget(self.language)
        layout1.addWidget(self.ExitDialog)
        self.sectian.add(_("general"),layout1)
        self.sectian.add(_("update"),UpdateLayout)
        restoar=Restoar(self)
        self.sectian.add(_("Backup and restoar"),restoar)
        layout.addWidget(self.ok)
        layout.addWidget(self.defolt)
        layout.addWidget(self.cancel)
        self.setLayout(layout)
    def fok(self):
        aa=0
        if settings_handler.get("g","lang")!=str(language.lang()[self.language.currentText()]):
            aa=1
        settings_handler.set("g","lang",str(language.lang()[self.language.currentText()]))
        settings_handler.set("g","exitDialog",str(self.ExitDialog.isChecked()))
        settings_handler.set("update","autoCheck",str(self.update_autoDect.isChecked()))
        settings_handler.set("update","beta",str(self.update_beta.isChecked()))
        if aa==1:
            mb=qt.QMessageBox(self)
            mb.setWindowTitle(_("settings updated"))
            mb.setText(_("you must restart the program to apply changes \n do you want to restart now?"))
            rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
            rn.setText(_("restart now"))
            rl=mb.addButton(qt.QMessageBox.StandardButton.No)
            rl.setText(_("restart later"))
            mb.exec()
            ex=mb.clickedButton()
            if ex==rn:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif ex==rl:
                self.close()
        else:
            self.close()
    def default(self):
        mb=qt.QMessageBox(self)
        mb.setWindowTitle(_("alert"))
        mb.setText(_("do you wanna reset your settings ? \n if you click reset , the program will restart to complete reset."))
        rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
        rn.setText(_("reset and restart"))
        rl=mb.addButton(qt.QMessageBox.StandardButton.No)
        rl.setText(_("cancel"))
        mb.exec()
        ex=mb.clickedButton()
        if ex==rn:
            os.remove(settings_handler.cpath)
            os.execl(sys.executable, sys.executable, *sys.argv)

    def fcancel(self):
        self.close()
    def cbts(self,string):
        if string=="True":
            return True
        else:
            return False

class Restoar(qt.QVBoxLayout):
    def __init__(self,p):
        super().__init__()
        self.createCopy=qt.QPushButton(_("backup"))
        self.addWidget(self.createCopy)
        self.createCopy.clicked.connect(self.onbackup)
        self.restoar=qt.QPushButton(_("restoar"))
        self.addWidget(self.restoar)
        self.restoar.clicked.connect(self.onrestoar)
        self.p=p
    def onbackup(self):
        file=qt.QFileDialog(self.p)
        file.setFileMode(qt.QFileDialog.FileMode.Directory)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            with zipfile.ZipFile(os.path.join(file.selectedFiles()[0],settings_handler.appName + ".zip"),"w") as zipf:
                for root,ders,files in os.walk(os.path.join(os.getenv('appdata'),settings_handler.appName)):
                    for ffiles in files:
                        ffile=os.path.join(root,ffiles)
                        zipf.write(ffile,os.path.relpath(ffile,os.path.join(os.getenv('appdata'),settings_handler.appName)))
    def onrestoar(self):
        file=qt.QFileDialog(self.p)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            shutil.rmtree(os.path.join(os.getenv('appdata'),settings_handler.appName))
            with zipfile.ZipFile(file.selectedFiles()[0]) as zfile:
                zfile.extractall(os.path.join(os.getenv('appdata'),settings_handler.appName))
            mb=qt.QMessageBox(self.p)
            mb.setWindowTitle(_("settings updated"))
            mb.setText(_("you must restart the program to apply changes \n do you want to restart now?"))
            rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
            rn.setText(_("restart now"))
            rl=mb.addButton(qt.QMessageBox.StandardButton.No)
            rl.setText(_("restart later"))
            mb.exec()
            ex=mb.clickedButton()
            if ex==rn:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif ex==rl:
                self.p.close()
        
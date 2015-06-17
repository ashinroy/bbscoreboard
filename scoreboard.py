#!/usr/bin/python

#This CopyRight information should not be removed without confirmation from the author
# Copyright (C) 2014 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------
#  Appname: ScoreBoard UI
#  Author :Muraleekrishna G <muraleekrishnagc@gmail.com>,Ashin Roy
#  Created on: 19 Mar 2014
#  Latest edit on: 19 Mar 2014
#-------------------------------------------------------

from PyQt4 import QtCore, QtGui
import serial
import fnmatch
import pygame
import thread
import time
import os
import sys
euid = os.geteuid()
if euid != 0:
    print "Script not started as root. Running sudo.."
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # the next line replaces the currently-running process with the sudo
    os.execlpe('sudo', *args)
def auto_detect_serial_unix(preferred_list=['*']):
    '''try to auto-detect serial ports on win32'''
    import glob
    glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')+glob.glob("COM*")
    ret = []

    # try preferred ones first
    for d in glist:
        for preferred in preferred_list:
            if fnmatch.fnmatch(d, preferred):
                ret.append(d)
    if len(ret) > 0:
        return ret
    # now the rest
    for d in glist:
        ret.append(d)
    return ret
available_ports = auto_detect_serial_unix()
s= serial.Serial(available_ports[0], 9600,timeout=1)

class Score(object):
	def __init__(self):
		self.team1=0
		self.team2=0
		self.initTimeMin=60
		self.initTimeSec=0
		self.timeMin=0
		self.timeSec=0
		self.period=1
	
score=Score()
class Ui_MainWindow(object):
	def __init__(self):
		self.clear=False
		self.timerStarted = False
		self.timerPaused= False
		self.sent="0000"
	def setupUi(self, MainWindow):
		
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(801, 655)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.scoreTwo = QtGui.QLCDNumber(self.centralwidget)
		self.scoreTwo.setGeometry(QtCore.QRect(520, 50, 261, 301))
		font = QtGui.QFont()
		font.setPointSize(26)
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		self.scoreTwo.setFont(font)
		self.scoreTwo.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
		self.scoreTwo.setToolTip("")
		self.scoreTwo.setAutoFillBackground(False)
		self.scoreTwo.setLineWidth(2)
		self.scoreTwo.setSmallDecimalPoint(False)
		self.scoreTwo.setDigitCount(2)
		self.scoreTwo.setMode(QtGui.QLCDNumber.Dec)
		self.scoreTwo.setSegmentStyle(QtGui.QLCDNumber.Filled)
		self.scoreTwo.setObjectName("scoreTwo")
		self.progressBar = QtGui.QProgressBar(self.centralwidget)
		self.progressBar.setGeometry(QtCore.QRect(0, 630, 801, 23))
		self.progressBar.setMinimum(0)
		self.progressBar.setMaximum(100)
		self.progressBar.setProperty("value", 0)
		self.progressBar.setTextVisible(True)
		self.progressBar.setObjectName("progressBar")
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(10, 20, 61, 21))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.sendButton = QtGui.QPushButton(self.centralwidget)
		self.sendButton.setGeometry(QtCore.QRect(330, 380, 121, 51))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.sendButton.setFont(font)
		self.sendButton.setObjectName("sendButton")
		self.frame = QtGui.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(-10, 0, 411, 371))
		self.frame.setFrameShape(QtGui.QFrame.WinPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName("frame")
		self.scoreOne = QtGui.QLCDNumber(self.frame)
		self.scoreOne.setGeometry(QtCore.QRect(30, 50, 261, 301))
		font = QtGui.QFont()
		font.setPointSize(26)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.scoreOne.setFont(font)
		self.scoreOne.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
		self.scoreOne.setToolTip("")
		self.scoreOne.setLineWidth(2)
		self.scoreOne.setSmallDecimalPoint(False)
		self.scoreOne.setDigitCount(2)
		self.scoreOne.setMode(QtGui.QLCDNumber.Dec)
		self.scoreOne.setSegmentStyle(QtGui.QLCDNumber.Filled)
		self.scoreOne.setProperty("value", 0.0)
		self.scoreOne.setObjectName("scoreOne")
		self.textEdit = QtGui.QTextEdit(self.frame)
		self.textEdit.setGeometry(QtCore.QRect(90, 10, 291, 31))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		self.textEdit.setFont(font)
		self.textEdit.setObjectName("textEdit")
		self.spinBox = QtGui.QSpinBox(self.frame)
		self.spinBox.setGeometry(QtCore.QRect(300, 190, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		
		font.setBold(True)
		font.setWeight(75)
		self.spinBox.setFont(font)
		self.spinBox.setObjectName("spinBox")
		self.frame_2 = QtGui.QFrame(self.centralwidget)
		self.frame_2.setGeometry(QtCore.QRect(400, 0, 401, 371))
		self.frame_2.setFrameShape(QtGui.QFrame.WinPanel)
		self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
		self.frame_2.setObjectName("frame_2")
		self.label_2 = QtGui.QLabel(self.frame_2)
		self.label_2.setGeometry(QtCore.QRect(20, 20, 61, 21))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.label_2.setFont(font)
		self.label_2.setObjectName("label_2")
		self.textEdit_2 = QtGui.QTextEdit(self.frame_2)
		self.textEdit_2.setGeometry(QtCore.QRect(90, 10, 291, 31))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		self.textEdit_2.setFont(font)
		self.textEdit_2.setObjectName("textEdit_2")
		self.spinBox_2 = QtGui.QSpinBox(self.frame_2)
		self.spinBox_2.setGeometry(QtCore.QRect(30, 190, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.spinBox_2.setFont(font)
		self.spinBox_2.setObjectName("spinBox_2")
		self.frame_3 = QtGui.QFrame(self.centralwidget)
		self.frame_3.setGeometry(QtCore.QRect(460, 370, 341, 261))
		self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
		self.frame_3.setObjectName("frame_3")
		self.timerStartButton = QtGui.QPushButton(self.frame_3)
		self.timerStartButton.setGeometry(QtCore.QRect(210, 10, 121, 41))
		self.timerStartButton.setObjectName("timerStartButton")
		self.loadMin = QtGui.QTextEdit(self.frame_3)
       
		
		self.loadMin.setGeometry(QtCore.QRect(10, 110, 101, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.loadMin.setFont(font)
		self.loadMin.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.loadMin.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.loadMin.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.loadMin.setObjectName("loadMin")
		
		self.loadSec = QtGui.QTextEdit(self.frame_3)
		self.loadSec.setGeometry(QtCore.QRect(120, 110, 81, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.loadSec.setFont(font)
		self.loadSec.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.loadSec.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.loadSec.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.loadSec.setObjectName("loadSec")
		self.timerClearButton = QtGui.QPushButton(self.frame_3)
		self.timerClearButton.setGeometry(QtCore.QRect(210, 60, 121, 41))
		self.timerClearButton.setFocusPolicy(QtCore.Qt.NoFocus)
		self.timerClearButton.setObjectName("timerClearButton")
		self.timerMinDown = QtGui.QPushButton(self.frame_3)
		self.timerMinDown.setGeometry(QtCore.QRect(210, 180, 121, 41))
		self.timerMinDown.setFocusPolicy(QtCore.Qt.NoFocus)
		self.timerMinDown.setObjectName("timerMin")
		self.timerSec = QtGui.QLCDNumber(self.frame_3)
		self.timerSec.setGeometry(QtCore.QRect(110, 10, 91, 71))
		self.timerSec.setNumDigits(2)
		self.timerSec.setMode(QtGui.QLCDNumber.Dec)
		self.timerSec.setSegmentStyle(QtGui.QLCDNumber.Flat)
		self.timerSec.setProperty("intValue", score.initTimeSec)
		self.timerSec.setObjectName("timerSec")
		self.label_4 = QtGui.QLabel(self.frame_3)
		self.label_4.setGeometry(QtCore.QRect(170, 80, 31, 16))
		self.label_4.setObjectName("label_4")
		self.timerMin = QtGui.QLCDNumber(self.frame_3)
		self.timerMin.setGeometry(QtCore.QRect(10, 10, 91, 71))
		self.timerMin.setDigitCount(2)
		self.timerMin.setProperty("intValue", score.initTimeMin)
		self.timerMin.setSegmentStyle(QtGui.QLCDNumber.Flat)
		self.timerMin.setObjectName("timerMin")
		self.label_3 = QtGui.QLabel(self.frame_3)
		self.label_3.setGeometry(QtCore.QRect(70, 80, 31, 16))
		self.label_3.setObjectName("label_3")
		self.timerPauseButton = QtGui.QPushButton(self.frame_3)
		self.timerPauseButton.setGeometry(QtCore.QRect(10, 150, 181, 101))
		self.timerPauseButton.setObjectName("pauseButton")
		self.loadButton = QtGui.QPushButton(self.frame_3)
		self.loadButton.setGeometry(QtCore.QRect(210, 110, 51, 31))
		self.loadButton.setFocusPolicy(QtCore.Qt.NoFocus)
		self.loadButton.setObjectName("loadButton")
		self.period = QtGui.QLCDNumber(self.centralwidget)
		self.period.setGeometry(QtCore.QRect(90, 390, 141, 131))
		self.period.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
		self.period.setDigitCount(1)
		self.period.setObjectName("period")
		self.period.setProperty("intValue",1)
		self.label_5 = QtGui.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(30, 390, 58, 15))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.label_5.setFont(font)
		self.label_5.setObjectName("label_5")
		self.frame_4 = QtGui.QFrame(self.centralwidget)
		self.frame_4.setGeometry(QtCore.QRect(0, 370, 321, 161))
		self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
		self.frame_4.setObjectName("frame_4")
		self.spinBox_3 = QtGui.QSpinBox(self.frame_4)
		self.spinBox_3.setGeometry(QtCore.QRect(240, 70, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.spinBox_3.setFont(font)
		self.spinBox_3.setMinimum(1)
		self.spinBox_3.setMaximum(5)
		self.spinBox_3.setObjectName("spinBox_3")
		self.retranslateUi(MainWindow)
		
		self.sendButton.clicked.connect(self.Send)
		self.timerStartButton.clicked.connect(self.TimerStart)
		self.timerClearButton.clicked.connect(self.TimerClear)
		self.timerMinDown.clicked.connect(self.TimerDown)
		self.timerPauseButton.clicked.connect(self.TimerPause)
		self.loadButton.clicked.connect(self.LoadTimer)
		self.spinBox.valueChanged.connect(self.Team1Score)
		self.spinBox_2.valueChanged.connect(self.Team2Score)
		self.spinBox_3.valueChanged.connect(self.Period)
		
		
	def Period(self):
		score.period=int(self.spinBox_3.value())
		self.period.setProperty("value", score.period)
		
	def Team1Score(self):
		score.team1=int(self.spinBox.value())
		self.scoreOne.setProperty("value", score.team1)
    
	def Team2Score(self):
		score.team2=int(self.spinBox_2.value())
		self.scoreTwo.setProperty("value", score.team2)    
    
     
	def Send(self):
		self.sent = ""
		if score.team1<10:
			self.sent=self.sent+'0'
		self.sent=self.sent+str(score.team1)
		if score.team2<10:
			self.sent=self.sent+'0'
		self.sent=self.sent+str(score.team2)
		if self.timerStarted==False or self.timerPaused==True: 
				self.Send_value(score.timeMin,score.timeSec)
    	
	def TimerStart(self):
		if not self.timerStarted:
			self.TimerClear()
			self.timerStarted = True
			thread.start_new_thread( self.Timer,(0,0) )
			
	def Timer(self,ints,i):
		self.clear=False
		score.timeMin=score.initTimeMin
		score.timeSec=score.initTimeSec
		
		while self.clear==False:
			if not self.timerPaused:
				
				score.timeSec=(score.timeSec-1)
				
				if score.timeSec<0:
					if score.timeMin==0:
						if score.timeSec==-1:
							score.timeSec=0								
						self.timerSec.setProperty("intValue",score.timeSec)
						#self.Send_value(score.timeMin,score.timeSec)
						self.timerPaused=True
						return 
					score.timeSec=59
				if score.timeSec==59:
					score.timeMin=(score.timeMin-1)
					if score.timeMin<0:
						score.timeMin=0
				if score.timeMin==0 and score.timeSec<6 and score.timeSec>0:
					pygame.init()
					pygame.mixer.music.load("beep.mp3")
					pygame.mixer.music.play()
				if score.timeMin==0 and score.timeSec==0:
					pygame.init()
					pygame.mixer.music.load("buzzer.mp3")
					pygame.mixer.music.play()

				self.Send_value(score.timeMin,score.timeSec)
				self.timerSec.setProperty("intValue",score.timeSec)
				self.timerMin.setProperty("intValue",score.timeMin)
			time.sleep(1)
	def TimerDown(self):
		score.timeMin=(score.timeMin-1)
		if score.timeMin<0:
			score.timeMin=0
	def TimerClear(self):
		score.timeMin=score.initTimeMin
		score.timeSec=score.initTimeSec
		self.timerSec.setProperty("intValue",score.initTimeSec)
		self.timerMin.setProperty("intValue",score.initTimeMin)
		self.timerStarted = False
		self.timerPauseButton.setText("PAUSE")
		self.timerPaused=False
		if self.clear==False:	 
			self.Send_value(score.timeMin,score.timeSec)
		self.clear=True
	def Send_value(self,mins=score.timeMin,sec=score.timeSec):
			sents=self.sent
			if mins<10:
				sents=sents+'0'
			sents=sents+str(mins)
			if sec<10:
				sents=sents+'0'
			sents=sents+str(sec)+str(score.period)
			s.write(sents)
			s.flush()
			print sents
		
	def TimerPause(self):
		if self.timerStarted:
			if not self.timerPaused:
				self.timerPauseButton.setText("RESUME")
				self.timerPaused=True
			else :
				self.timerPauseButton.setText("PAUSE")
				self.timerPaused=False
	def LoadTimer(self):
		score.initTimeMin=int(self.loadMin.toPlainText())
		score.initTimeSec=int(self.loadSec.toPlainText())
		self.timerSec.setProperty("intValue",score.initTimeSec)
		self.timerMin.setProperty("intValue",score.initTimeMin)
		
		
		
		
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "BB Score Board", None, QtGui.QApplication.UnicodeUTF8))
		self.progressBar.setFormat(QtGui.QApplication.translate("MainWindow", "%p%", None, QtGui.QApplication.UnicodeUTF8))
		self.label.setText(QtGui.QApplication.translate("MainWindow", "Team 1:", None, QtGui.QApplication.UnicodeUTF8))
		self.sendButton.setText(QtGui.QApplication.translate("MainWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))
		self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Team 2:", None, QtGui.QApplication.UnicodeUTF8))
		self.timerStartButton.setText(QtGui.QApplication.translate("MainWindow", "START", None, QtGui.QApplication.UnicodeUTF8))
		self.timerClearButton.setText(QtGui.QApplication.translate("MainWindow", "CLEAR", None, QtGui.QApplication.UnicodeUTF8))
		self.timerMinDown.setText(QtGui.QApplication.translate("MainWindow", "-1 Min", None, QtGui.QApplication.UnicodeUTF8))
		self.label_4.setText(QtGui.QApplication.translate("MainWindow", "SEC", None, QtGui.QApplication.UnicodeUTF8))
		self.label_3.setText(QtGui.QApplication.translate("MainWindow", "MIN", None, QtGui.QApplication.UnicodeUTF8))
		self.loadButton.setText(QtGui.QApplication.translate("MainWindow", "LOAD", None, QtGui.QApplication.UnicodeUTF8))
		self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Period", None, QtGui.QApplication.UnicodeUTF8))
		self.timerPauseButton.setText(QtGui.QApplication.translate("MainWindow", "PAUSE", None, QtGui.QApplication.UnicodeUTF8))
def main():
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QDialog()
	ui = Ui_MainWindow()
	ui.setupUi(Dialog)
	Dialog.show()
	sys.exit(app.exec_())
	

if __name__ == "__main__":	
	main()

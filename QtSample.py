from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QFrame,QScrollArea,QApplication,
                             QHBoxLayout,QStackedLayout,QGridLayout, QVBoxLayout, QMainWindow,QAction)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic
from functools import partial

import sys

class node:
	def __init__(self,label,x,y):
		self.x_pos=x
		self.y_pos=y
		self.label_pos=label

class widget(QWidget):
	def __init__(self, parent=None, flags=Qt.WindowFlags()):
		super().__init__(parent=parent, flags=flags)
		self.edges=list()
	def getEdges(self):
		file1=open("ex.txt")
		list1=file1.read().split('\n')
		for each in list1:
			values=each.split(',')
			if(len(values)!=0):
				self.edges.append(values)
		

	def getNodes(self):
		file1=open("ex.txt")
		list1=file1.read().split('\n')
		nodes=dict()
		for each in list1:
			values=each.split(',')
			for e in values:
				nodes[e]=1
		return nodes

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.setRenderHint(painter.Antialiasing)
		label_coord=dict()
		nodesList=self.getNodes()
		valueX=20
		valueY=20
		nodes=list()
		for each in nodesList:
			v=(valueY+30)%600
			if v<valueY:
				valueX+=30
			valueY=v
			nodes.append(node(each,valueX,valueY))
		
		for each in nodes:
			label_coord[each.label_pos]=[each.x_pos,each.y_pos]
		self.getEdges()
		for edge in self.edges:
			try:
				point1=QPoint(label_coord[edge[0]][0],label_coord[edge[0]][1])
				point2=QPoint(label_coord[edge[1]][0],label_coord[edge[1]][1])
				painter.drawLine(point1,point2)
			except Exception as e:
				pass
			

class NodeButton(QPushButton):

	def __init__(self, str, str1, values):
		super().__init__(str, values)
		self.name=str1
		

	def HoverEnter(self):
		self.setStyleSheet("color:white; background: blue;padding: 10px;")
		

		text=self.text()
		v=""
		length=len(text)
		value=0
		while True:
			if(value<length):
				v+=text[value:value+8]+"\n"
				value+=8
			else:
				v+=text[value:]
				break
		vX=self.x()
		vY=self.y()
		self.setGeometry(vX-70,vY-70,100,100)
		self.setText(v)
		# self.HoverBox.setGeometry(100,100,100,100)
		# self.HoverBox.setStyleSheet("color:white; background: yellow;padding: 10px;")
		
		
	def HoverLeave(self):
		self.setStyleSheet("color:white; background: red;padding: 10px;")
		self.setGeometry(self.x()+70,self.y()+70,20,20)

	

	# def clicked1(self):
	# 	pass
	def event(self, QEvent):
		if QEvent.type() == QEvent.Type.HoverEnter:
			self.HoverEnter()
		if QEvent.type() == QEvent.Type.HoverLeave:
			self.HoverLeave()
		# if QEvent.type() == QEvent.Type.MouseButtonPress:
		# 	self.clicked1()
		return super().event(QEvent)

	
		 
	
		





class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def getAdjacencyList(self):
		file1=open("ex.txt")
		list1=file1.read().split('\n')
		adjList=dict()
		for each in list1:
			values=each.split(',')
			if len(values) !=2:
				continue
			try:
				adjList[values[0]].append(values[1])
			except Exception as e:
				adjList[values[0]]=list()
		return adjList

	def clickLabel(self,name):
		try:
			print(name)
			list1=self.adjacency[name]
			print("Step1")
			for each in list1:
				label1=self.nodeMap[each].label_pos
				label1.setStyleSheet('color:white; background: green')
				print("Step2")
		except Exception as e:
			print("Errorororor")
		
	def searchAndHighlight(self):
		searchText=self.search.text()
		for each in self.nodesList:
			# print(each.label_pos.text())
			if searchText==each.label_pos.text():
				each.label_pos.setStyleSheet('background:green')
				# print

	def initUI(self):
		self.adjacency=self.getAdjacencyList()
		self.widget=widget()
		self.search=QLineEdit('Enter search class',self)
		self.searchbutton=QPushButton('SEARCH',self)
		self.searchbutton.clicked.connect(self.searchAndHighlight)
		self.search.setGeometry(100,650,200,50)
		self.searchbutton.setGeometry(320,650,100,50)
		self.setGeometry(300,100,1000,900)
		self.nodesList=list()
		
		self.scroll=QScrollArea()
		self.setCentralWidget(self.scroll)
		self.scroll.setFixedSize(1300,620)
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.widget)
		
		nodesList=self.getNodes()
		valueX=20
		valueY=20
		for each in nodesList:
			label=NodeButton(each,each,self.widget)
			
			label.setGeometry(valueX,valueY,20,20)
			v=(valueY+30)%600
			if v<valueY:
				valueX+=30
			valueY=v
			
			label.setObjectName(each)
			label.setStyleSheet("color:white; background: red;padding: 10px;")
			label.clicked.connect(partial(self.clickLabel,each))
			self.nodesList.append(node(label,valueX,valueY))


		self.nodeMap=dict()	
		for each in self.nodesList:
			self.nodeMap[each.label_pos.text()]=each
			# self.vbox.addWidget(label)
		
		# self.widget.setLayout(self.vbox)
		
		
		self.setWindowTitle('Extended Classes')
		self.show()
		
		return


	def getNodes(self):
		file1=open("ex.txt")
		list1=file1.read().split('\n')
		nodes=dict()
		for each in list1:
			values=each.split(',')
			for e in values:
				nodes[e]=1

		return nodes

def main():
	app=QtWidgets.QApplication(sys.argv)
	main=MainWindow()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
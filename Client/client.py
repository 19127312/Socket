import sys
import sqlite3
import socket
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication,QPushButton
from PyQt5.uic import loadUi

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client -sever here
class QueryClientTable(QtWidgets.QMainWindow,QPushButton):
    def __init__(self,query,type):
        super(QueryClientTable, self).__init__()
        uic.loadUi("QueryClientTable.ui", self).show()
        self.loadtable(query,type)
#client-sever here
    def loadtable(self,query,type):
        #this is done at server

        s.sendall(b'sqlQuery')
        stringServer=query+" "+type
        s.sendall(bytes(stringServer, "utf8"))

        size = s.recv(1024)
        size = size.decode('utf-8')

        data = s.recv(int(size))
        data = data.decode('utf-8')

        #client receive string
        myTuple=data.split("|")
        number=myTuple[len(myTuple)-1]
        myTuple.remove(number)
        self.tableWidget.setRowCount(int(number))
        tableIndex = 0
        for row in myTuple:
            line=row.split()
            self.tableWidget.setItem(tableIndex, 0, QtWidgets.QTableWidgetItem(line[0]))
            self.tableWidget.setItem(tableIndex, 1, QtWidgets.QTableWidgetItem(line[1]))
            self.tableWidget.setItem(tableIndex, 2, QtWidgets.QTableWidgetItem(line[2]))
            self.tableWidget.setItem(tableIndex, 3, QtWidgets.QTableWidgetItem(line[3]))
            self.tableWidget.setItem(tableIndex, 4, QtWidgets.QTableWidgetItem(line[4]))
            tableIndex += 1

#client -sever here
class QueryClient(QDialog):
    def __init__(self):
        super(QueryClient,self).__init__()
        loadUi("QueryClient.ui",self)
        self.SearchButton.clicked.connect(self.SearchFunction)
        self.ViewButton.clicked.connect(self.ViewFunction)

    def ViewFunction(self):
        pass
    def SearchFunction(self):
        command=self.Command.text()
        comSplit=command.split(' ', 1)
        if(len(comSplit)!=0):
            if (comSplit[0] != "F_ID" and comSplit[0] != "F_Name" and comSplit[0] != "F_Author" and comSplit[0] != "F_Type") :
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Wrong input")
                retval = msg.exec_()
                return False
            else:
                if(comSplit[0]=="F_ID"):
                    ID = comSplit[1]
                    if ID.isdigit():
                       self.IDfunct(ID)
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("ID must be number")
                        retval = msg.exec_()
                else:
                    query=comSplit[1]
                    if(comSplit[0]=="F_Name"):
                        type="name"
                    elif(comSplit[0]=="F_Author"):
                        type="author"
                    else:
                        type = "type"
                    self.table=QueryClientTable(query,type)
                    self.table.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Wrong input")
            retval = msg.exec_()
            return False

    def IDfunct(self,ID):
        # send to sever here
        s.sendall(b'sqlQueryID')
        sqlcom = "SELECT * ,count (*) FROM book where ID=" + ID
        s.sendall(bytes(sqlcom, "utf8"))

        # receive text here
        size = s.recv(1024)
        size = size.decode('utf-8')

        data = s.recv(int(size))
        data = data.decode('utf-8')

        text=data.split(" ",1)
        if (int(text[0])):
            self.DemoView.setText(text[1])
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Can't find file in library")
            retval = msg.exec_()
            return 0

#client-server here
class Connect(QDialog):
    def __init__(self):
        super(Connect,self).__init__()
        loadUi("ConnectServer.ui",self)
        self.ConnectButton.clicked.connect(self.ConnectFunction)

    def ConnectFunction(self):
        #Input here
        HOST = self.InputIP.text()
        PORT = self.InputPort.text()
        if (HOST == "" or PORT == ""):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("IP and Port must be filled!")
            retval = msg.exec_()
            return
        if(not PORT.isdigit()):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Port must be number!")
            retval = msg.exec_()
            return
        PORT=int(PORT)
        try:
            s.connect((HOST, PORT))
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Connect failed !")
            retval = msg.exec_()
            return
        #if pass
        queryClient = QueryClient()
        msg = QtWidgets.QMessageBox()
        msg.setText("Established connection successfully!")
        retval = msg.exec_()
        login=Login()
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#Create Login action
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        s.sendall(b'login')

        user=self.user.text()
        password=self.password.text()
        tk = user + ' ' + password

        s.sendall(bytes(tk, "utf8"))
        try:
            data = s.recv(1024)
            data = data.decode('utf-8')
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Login failed !")
            retval = msg.exec_()
            return
        Switcher(int(data))


    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


#Create Create Account Action
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        s.sendall(b'create')
        user = self.user.text()
        password = self.password.text()
        confirm = self.confirmpass.text()
        tk = user + ' ' + password + ' ' + confirm
        s.sendall(bytes(tk, "utf8"))

        try:
            data = s.recv(1024)
            data = data.decode('utf-8')
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Create account failed !")
            retval = msg.exec_()
            return

        if int(data) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Existed User")
            retval = msg.exec_()
        if int(data) == 1:
            msg = QtWidgets.QMessageBox()
            msg.setText("Registered Successfully !")
            retval = msg.exec_()
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)


#Switch to different dialog
def Switcher(i):
    if i==-1:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Invalid login")
        retval = msg.exec_()
        return False
    elif i==0:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Wrong Password")
        retval = msg.exec_()
        return False
    elif i==1:
        queryClient=QueryClient()
        msg = QtWidgets.QMessageBox()
        msg.setText("Login Success")
        retval = msg.exec_()
        widget.addWidget(queryClient)
        widget.setFixedWidth(660)
        widget.setFixedHeight(600)
        widget.setCurrentIndex(widget.currentIndex() + 1)


#main

app=QApplication(sys.argv)
mainwindow=Connect()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(347)
widget.setFixedHeight(190)
widget.show()
app.exec_()
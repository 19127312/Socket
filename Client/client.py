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
        connection = sqlite3.connect("serverBook.db")
        cur = connection.cursor()
        query = "'" + query + "'"

        if type == "name":
            sqlcom = "SELECT *,COUNT(*) FROM book where Name=" + query
        elif type == "type":
            sqlcom = "SELECT *,COUNT(*) FROM book where type=" + query
        elif type == "author":
            sqlcom = "SELECT *,COUNT(*) FROM book where author=" + query
        for line in (cur.execute(sqlcom)):
            number = line[5]
        #send number for client to display
        if(number==0):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Can't find file in library")
            retval = msg.exec_()
            return 1
        if type == "type":
            sqlcom = "SELECT * FROM book where type=" + query
        elif type == "author":
            sqlcom = "SELECT * FROM book where author=" + query
        else:
            sqlcom = "SELECT * FROM book where name=" + query
        #send tuple here for client
        tableTup = cur.execute(sqlcom)
        self.tableWidget.setRowCount(number)
        tableIndex = 0
        myString=""
        for row in tableTup:
            myString=myString+row[0]+" "+row[1]+" "+row[2]+" "+row[3]+" "+str(row[4])+" "
            print(myString)
            self.tableWidget.setItem(tableIndex, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tableIndex, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tableIndex, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableIndex, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tableIndex, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            tableIndex += 1

#client -sever here
class QueryClient(QDialog):
    def __init__(self):
        super(QueryClient,self).__init__()
        loadUi("QueryClient.ui",self)
        self.SearchButton.clicked.connect(self.SearchFucntion)

    def SearchFucntion(self):
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
        connection = sqlite3.connect("serverBook.db")
        cur = connection.cursor()
        sqlcom = "SELECT * ,count (*) FROM book where ID=" + ID
        check = 1
        # receive text here
        for line in (cur.execute(sqlcom)):
            print(line)
            if (line[5] == 0):
                check = 0
                break
            id = line[0]
            name = line[1]
            type = line[2]
            author = line[3]
            year = line[4]
        text = "ID: " + id + "\nName: " + name + "\nType: " + type + "\nAuthor: " + author +"\nYear: " +str(year)+ "\n\n"
        filename = "File\\" + id + "-demo.txt"
        try:
            file = open(filename, "r")
        except:
            msg = QtWidgets.QMessageBox()
            msg.setText("Can't find required file")
            retval = msg.exec_()
            return
        text += file.read()
        file.close()
        #send text to client here for displaying
        if (check):
            self.DemoView.setText(text)
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
        msg.setText("Connect Success!")
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

        data = s.recv(1024)
        data = data.decode('utf-8')
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

        data = s.recv(1024)
        data = data.decode('utf-8')

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
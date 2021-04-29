import socket
import sqlite3
import sys
from sys import getsizeof
from _thread import *
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication,QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QCoreApplication, QThread)
import os
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(3) #Maximum number of client in queue


def checkExist(user):
    accfile = open("account.txt", "r")
    for line in accfile.readlines():
        values = line.split(" ")
        if user == values[0]:
            accfile.close()
            return 1
    accfile.close()
    return 0

def addAccount(user,password):
    accfile = open("account.txt", "a")
    newAcc="\n"+user+" "+password
    accfile.write(newAcc)
    accfile.close()

def CheckAccount(user,password):

    accfile=open( "account.txt" , "r")
    for line in accfile.readlines():
        values=line.split(" ")
        if values[1][len(values[1])-1:len(values[1])]=="\n":
            values[1]=values[1][0:len(values[1])-1]
        if user==values[0]:
            if password==values[1]:
                accfile.close()
                return 1
            else:
                accfile.close()
                return 0
    accfile.close()
    return -1

def Login(conn):
    try:
        data = conn.recv(1024)
        data = data.decode('utf-8')
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

    user = data.split()
    if (CheckAccount(user[0], user[1]) == True):
        check = '1'
        try:
            conn.sendall(bytes(check, 'utf8'))
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Connect failed!")
            retval = msg.exec_()
            return 0
    else:
        check = '0'
        try:
            conn.sendall(bytes(check, 'utf8'))
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Connect failed!")
            retval = msg.exec_()
            return 0

def CreateAccount(conn):
    try:
        data = conn.recv(1024)
        data = data.decode('utf-8')
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0
    create = data.split()
    if checkExist(create[0]) == True:
        check = '0'
        try:
            conn.sendall(bytes(check, 'utf8'))
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Connect failed!")
            retval = msg.exec_()
            return 0
    else:
        check = '1'
        addAccount(create[0], create[1])
        try:
            conn.sendall(bytes(check, 'utf8'))
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Connect failed!")
            retval = msg.exec_()
            return 0

def SQL(conn):
    try:
        data = conn.recv(1024)
        data = data.decode('utf-8')
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0
    com = data.split()
    query = com[0]
    type = com[1]
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
    # send number for client to display

    if type == "type":
        sqlcom = "SELECT * FROM book where type=" + query
    elif type == "author":
        sqlcom = "SELECT * FROM book where author=" + query
    else:
        sqlcom = "SELECT * FROM book where name=" + query
    # send tuple here for client
    myString = ""
    for row in cur.execute(sqlcom):
        myString = myString + row[0] + " " + row[1] + " " + row[2] + " " + row[3] + " " + str(
            row[4]) + "|"
    myString += str(number)

    sizeString = getsizeof(myString)
    try:
        conn.sendall(bytes(str(sizeString), 'utf8'))
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

    try:
        conn.sendall(bytes(myString, 'utf8'))
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

def SQL_ID(conn):
    try:
        data = conn.recv(1024)
        data = data.decode('utf-8')
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0
    connection = sqlite3.connect("serverBook.db")
    cur = connection.cursor()
    check = 1
    text = ""
    for line in (cur.execute(data)):
        print(line)
        if (line[5] == 0):
            check = 0
            break
        id = line[0]
        name = line[1]
        type = line[2]
        author = line[3]
        year = line[4]
        text = "ID: " + id + "\nName: " + name + "\nType: " + type + "\nAuthor: " + author + "\nYear: " + str(
            year) + "\n\n"
    sentback = str(check) + " " + text
    sizeString = getsizeof(sentback)

    try:
        conn.sendall(bytes(str(sizeString), 'utf8'))
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

    try:
        conn.sendall(bytes(sentback, 'utf8'))
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

def View(conn):
    try:
        filename = conn.recv(1024)
        filename = filename.decode('utf-8')
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0
    filename = "File//" + filename
    try:
        file = open(filename, "r")
        myText = file.read()
        file.close()
    except:
        myText = ""

    sizeString = getsizeof(myText)

    try:
        conn.sendall(bytes(str(sizeString), 'utf8'))
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

    try:
        conn.sendall(bytes(myText, 'utf8'))
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Connect failed!")
        retval = msg.exec_()
        return 0

def multi_threaded_client(conn):
    while True:

        try:
            data = conn.recv(1024)
            print(data)
            data = data.decode('utf-8')
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Connect failed!")
            retval = msg.exec_()
            break
        try:
            if test == 0:
                print('b')
                break
        except:
            pass
        if not data:
            break
        if data == 'login':
            if Login(conn)==0:
                break

        if data == 'create':
            if CreateAccount(conn)==0:
                break

        if data == 'sqlQuery':
            if SQL(conn)==0:
                break

        if data == 'sqlQueryID':
            if(SQL_ID(conn)==0):
                break

        if data == 'View' or data=='Download':
            if View(conn)==0:
                break

        if data == 'Disconnect':
            (client, ap) = s.accept()
            start_new_thread(multi_threaded_client, (client,))

    conn.close()

class Task(QThread):
    def run(self):
        v = ''
        vlock = allocate_lock()
        nclientlock = allocate_lock()
        for i in range(MaxClient):
            try:
                (client, ap) = s.accept()
                start_new_thread(multi_threaded_client, (client,))
            except:
                s.close()


class Server(QDialog):
    def __init__(self):
        super(Server,self).__init__()
        loadUi("DisconnectALL.ui",self)
        self.do_task()
        self.DiconnectButton.clicked.connect(self.DisconnectFunction)
    def do_task(self):
        self.thread = Task()
        self.thread.start()

    def DisconnectFunction(self):

        s.close()
        global test
        test = 0
        print('a')

class InitServer(QDialog):
    def __init__(self):
        super(InitServer,self).__init__()
        loadUi("ServerCreate.ui",self)
        self.IP.setText(socket.gethostbyname(socket.gethostname()))
        self.CreateButton.clicked.connect(self.CreateServer)
        self.setWindowTitle("Create Server")
    def CreateServer(self):
       if(int(self.spinBox.value())==0):
           msg = QtWidgets.QMessageBox()
           msg.setIcon(QtWidgets.QMessageBox.Critical)
           msg.setText("Cannot create!")
           retval = msg.exec_()
       else:
            global  MaxClient
            MaxClient=int(self.spinBox.value())
            server = Server()
            msg = QtWidgets.QMessageBox()
            msg.setText("Create Server Successfully")
            retval = msg.exec_()
            widget.addWidget(server)
            widget.setFixedWidth(321)
            widget.setFixedHeight(133)
            widget.setCurrentIndex(widget.currentIndex() + 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = InitServer()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(203)
    widget.setFixedHeight(156)
    widget.show()
    app.exec_()







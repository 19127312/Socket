import socket
import sqlite3
from sys import getsizeof
import os
from _thread import *

HOST = '127.0.0.1'
PORT = 8000

ThreadCount = 0
def main () :

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) # lắng nghe
    s.listen(3)
    conn, addr = s.accept()
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(main, (conn,))
    ThreadCount += 1
    with conn:
        try:
            print('Connected by', addr)

            while True:
                data = conn.recv(1024)
                data = data.decode('utf-8')
                if data == 'login':
                     data = conn.recv(1024)
                     data = data.decode('utf-8')
                     user = data.split()
                     if (CheckAccount(user[0],user[1]) == True) :
                        check = '1'
                        conn.sendall(bytes(check,'utf8'))
                     else:
                         check = '0'
                         conn.sendall(bytes(check, 'utf8'))

                if data == 'create':
                     data = conn.recv(1024)
                     data = data.decode('utf-8')
                     create = data.split()
                     if checkExist(create[0]) == True:
                         check = '0'
                         conn.sendall(bytes(check, 'utf8'))
                     else:
                         check = '1'
                         addAccount(create[0], create[1])
                         conn.sendall(bytes(check, 'utf8'))

                     break

                if data=='sqlQuery':
                    data = conn.recv(1024)
                    data = data.decode('utf-8')
                    com = data.split()
                    query=com[0]
                    type=com[1]
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
                    if (number == 0):
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
                    # send tuple here for client
                    myString = ""
                    for row in cur.execute(sqlcom):
                        myString = myString + row[0] + " " + row[1] + " " + row[2] + " " + row[3] + " " + str(
                            row[4]) + "|"
                    myString += str(number)

                    sizeString=getsizeof(myString)
                    conn.sendall(bytes(str(sizeString), 'utf8'))
                    conn.sendall(bytes(myString, 'utf8'))

                if data == 'sqlQueryID':
                    data = conn.recv(1024)
                    data = data.decode('utf-8')
                    connection = sqlite3.connect("serverBook.db")
                    cur = connection.cursor()
                    check=1
                    text=""
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
                        text = "ID: " + id + "\nName: " + name + "\nType: " + type + "\nAuthor: " + author + "\nYear: " + str(year) + "\n\n"
                    sentback=str(check) +" "+ text
                    sizeString = getsizeof(sentback)
                    conn.sendall(bytes(str(sizeString), 'utf8'))
                    conn.sendall(bytes(sentback, 'utf8'))

                if data=='View':
                    filename = conn.recv(1024)
                    filename = filename.decode('utf-8')
                    filename="File//"+filename
                    try:
                        file=open(filename,"r")
                        myText=file.read()
                        file.close()
                    except:
                        myText = ""
                    sizeString = getsizeof(myText)

                    conn.sendall(bytes(str(sizeString), 'utf8'))
                    conn.sendall(bytes(myText, 'utf8'))


        finally:
            s.close()
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

if __name__ == '__main__':
    main()

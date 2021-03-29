import socket



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

HOST = '127.0.0.1'
PORT = 8000

def main () :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) # lắng nghe
    s.listen(1)
    conn, addr = s.accept()
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

        finally:
            s.close()

if __name__ == '__main__':
    main()

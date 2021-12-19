import socket
import time
import os
from _thread import *
from funct import *

BBS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 8818
UsersCount = 0

try:
    BBS.bind((host, port))
    BBS.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,True)
except socket.error as e:
    print("error de conexion detectado ->", str(e))

print('SERVER > Waiting for a Connection..\r')

BBS.listen(8)

def do_welcome(connection):

         #CLEAR SCREEN
         connection.send(cbmcursor("clear"))
         connection.send(cbmcursor("home"))

         #Abre archivo encabezado
         # print ("STATUS > enviar el head")
         send_file(connection, "headbbs.seq")

         #Envia encabezado
         connection.send(cbmcursor("red"))
         connection.send(cbmencode("\n\nBienvenido"))
         connection.send(cbmcursor("blue"))
         connection.send(cbmencode(" a "))
         connection.send(cbmcursor("purple"))
         connection.send(cbmencode("MNGBBS\n\n"))
         connection.send(cbmcursor("grey"))
         welcome2="This is a text is a text"
         connection.send(cbmencode(welcome2))
         cursorxy(connection,1,1)
         connection.send(cbmencode("en 1,1"))
         cursorxy(connection,1,25)
         connection.send(cbmencode("en 1,25"))
         time.sleep(2)

def do_login(connection):

         #CLEAR SCREEN
         connection.send(cbmcursor("clear"))
         connection.send(cbmcursor("home"))
         cursorxy(connection,1,3)

         #Login
         connection.send(cbmencode("Username (new): "))
         namex=input_line(connection)
         print("decoded name: ",cbmdecode(namex))

         connection.send(cbmencode("Password: "))
         pword=input_pass(connection)
         print("decoded pass: ",cbmdecode(pword))

         uname=cbmdecode(namex)

         return uname

def do_bucle(connection,namex):

         while True:
           print("Hola, ",namex)
           connection.send(cbmencode("\n\nTYPE CHAR: "))
           #bucl=input_line(connection)
           bucl=get_char(connection)
           print(bucl)
           print("decoded: ",cbmdecode(bucl))


###########################################
# AQUI SE EJECUTA EL BBS 
###########################################

def user_session(connection):
      time.sleep(3)
      while True:

         #inicializa el terminal
         #connection.send(b'\xff\xfe\x22\xff\xfe\x01\xff\xfd\x00\xff\xfb\x01')

         do_welcome(connection)

         userx = do_login(connection)

         do_bucle(connection,userx)

#############################################################################

# Funcion de hilos (threads)
def threaded_client(connection):
    global UsersCount
    try:
       connection.settimeout(30) #30 secs timeout
       user_session(connection)
       connection.close()
       print('user exit closed connection',connection)
       UsersCount -= 1
    except Exception:
       connection.close()
       print('timeout   closed connection',connection)
       UsersCount -= 1

#LOOP Principal aqui espera las llamadas
while True:
    Client, address = BBS.accept()
    print('New call from: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    UsersCount += 1
    print('Connected Users: ' + str(UsersCount))

print('bye.')
BBS.close()

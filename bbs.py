import socket
import time
import os
from _thread import *
from funct import *

BBS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '' # leave empty for any IP
port = 8818 # you can change the incoming port to any desired
UsersCount = 0

try:
    BBS.bind((host, port))
    BBS.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,True)
except socket.error as e:
    print("Connection error detected ->", str(e))

print('SERVER > Waiting for a Connection..\r')

BBS.listen(8)

def do_welcome(connection):

         #CLEAR SCREEN
         connection.send(cbmcursor("clear"))
         connection.send(cbmcursor("home"))

         #SEND HEADER FILE (.SEQ)
         # print ("STATUS > will send seq")
         send_file(connection, "headbbs.seq")

         #THIS SECTION SENDS RANDOM THINGS (FOR YOU TO LEARN HOW)
         connection.send(cbmcursor("red")) #cbmcursor sends color red code
         connection.send(cbmencode("\n\nWelcome")) #cbmencode sends message
         connection.send(cbmcursor("blue"))
         connection.send(cbmencode(" a "))
         connection.send(cbmcursor("purple"))
         connection.send(cbmencode("CBMBBS\n\n"))
         connection.send(cbmcursor("grey"))
         welcome2="This is a text is a text" #You can also declare a string
         connection.send(cbmencode(welcome2)) #and send it after cbmencode it
         cursorxy(connection,1,1) #cursorxy positions cursor on x,y on screen
         connection.send(cbmencode("i am at 1,1"))
         cursorxy(connection,1,25)
         connection.send(cbmencode("i am at  1,25"))
         time.sleep(2)

def do_login(connection):

         #CLEAR SCREEN
         connection.send(cbmcursor("clear"))
         connection.send(cbmcursor("home"))
         cursorxy(connection,1,3)

         #Login (not finished)
         connection.send(cbmencode("Username (new): "))
         namex=input_line(connection) #input_line function reads a line
         print("decoded name: ",cbmdecode(namex)) # this is displayed on system side

         connection.send(cbmencode("Password: "))
         pword=input_pass(connection) #input_pass reads a line but shows '*'
         print("decoded pass: ",cbmdecode(pword)) # this is displayed on system side

         uname=cbmdecode(namex) #receives the name of the user

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
# MAIN BBS FUNCTIONS
###########################################

def user_session(connection):
      time.sleep(3)
      while True:

         #initializes terminal 

         do_welcome(connection)

         userx = do_login(connection)

         do_bucle(connection,userx)

#############################################################################

# (threads)
def threaded_client(connection):
    global UsersCount
    try:
       connection.settimeout(30) #30 secs timeout (HANGS UP CALL if stalled)
       user_session(connection)
       connection.close()
       print('user exit closed connection',connection)
       UsersCount -= 1
    except Exception:
       connection.close()
       print('timeout   closed connection',connection)
       UsersCount -= 1

#MAIN LOOP waits for the calls

while True:
    Client, address = BBS.accept()
    print('New call from: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    UsersCount += 1
    print('Connected Users: ' + str(UsersCount))

print('bye.')
BBS.close()

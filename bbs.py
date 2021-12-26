import mysql.connector
import socket
import time
import os
from _thread import *
from funct import *

#DEFINE LISTENING HOST AND PORT
BBS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '' # leave empty for any IP
port = 8818 # you can change the incoming port to any desired
UsersCount = 0

# Conect to mysql (to make it work: pip install mysql-connector)
mydb = mysql.connector.connect(
  host="localhost", #mysql server address
  user="bbs", #bbs user you created on mysql
  password="bbspass",
  database="cbmbbs"
)

# Define a database cursor to make the queries
mycursor = mydb.cursor(dictionary=True)

try:
    BBS.bind((host, port))
    BBS.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,True)
except socket.error as e:
    print("Connection error detected ->", str(e))

print('SERVER > Waiting for a Connection..\r')

BBS.listen()

def do_welcome(connection):

         #CLEAR SCREEN
         connection.send(cbmcursor("clear"))
         connection.send(cbmcursor("home"))

         #SEND HEADER FILE (.SEQ)
         # print ("STATUS > will send seq")
         connection.send(cbmencode("\n\n"))
         send_file(connection, "welcome.seq")

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
         time.sleep(8)

def do_login(connection):

       #CLEAR SCREEN
       connection.send(cbmcursor("clear"))
       connection.send(cbmcursor("home"))
       cursorxy(connection,1,3) #positions cursor on third line
       imf=0 #sets a flag for an infinite loop in while
       maxtries=3 #max tries
       attempts=0

       while True:
         #Login (not finished)
         connection.send(cbmencode("Username (new): "))
         namex=input_line(connection) #input_line function reads a line
         print("decoded name: ",cbmdecode(namex)) # this is displayed on system side
         uname=cbmdecode(namex) #receives the name of the user

         if (uname=="new"):
             uname,realid = do_newuser(connection)
             print("new user created")
             break

         connection.send(cbmencode("Password: "))
         pword=input_pass(connection) #input_pass reads a line but shows '*'
         print("decoded pass: ",cbmdecode(pword)) # this is displayed on system side
         upass=cbmdecode(pword) #receives the password  of the user

         # Define QUERY
         query="SELECT id,username,password FROM accounts WHERE username='%s'"
         query=query % (uname)

         # Execute QUERY
         mycursor.execute(query)
         myresult = mycursor.fetchone()

         if (myresult == None):
            connection.send(cbmencode("\n\nIncorrect username or password.\n\n"))
            attempts=attempts+1
         else:
            realpass = myresult['password']
            realid = myresult['id']

            # Check if there is a match
            if(realpass==upass):
               print("match!!")
               break
            else:
               connection.send(cbmencode("\n\nIncorrect username or password.\n\n"))
               attempts=attempts+1
         if (attempts>=maxtries):
               connection.send(cbmencode("\n\nSorry maximum number of attempts reached..\n\n"))
               connection.close()
       print("ok")
       print("uname->",uname,"realid->",realid)
       return uname,realid;

def do_newuser(connection):
       #CLEAR SCREEN
       connection.send(cbmcursor("clear"))
       connection.send(cbmcursor("home"))
       cursorxy(connection,1,3) #positions cursor on third line
       connection.send(cbmencode("Welcome new user!\nLet's create a new username.\n\n"))

       #DEFINE Variables to control loop
       maxtries=3 #max tries
       attempts=0

       while True:
         connection.send(cbmencode("Type your username: "))
         namex=input_line(connection) #input_line function reads a line
         uname=cbmdecode(namex)

         # Define QUERY
         query="SELECT id,username,password FROM accounts WHERE username='%s'"
         query=query % (uname)

         # Execute QUERY
         mycursor.execute(query)
         myresult = mycursor.fetchone()

         if(myresult == None):
            connection.send(cbmencode("Your username is: "+uname+"\nAre you sure? (y/n): "))
            letter=cbmdecode(get_char(connection))
            print("letra: ",letter)
            connection.send(cbmencode("\n\n"))
            attempts=attempts+1
            if(letter=="y" or letter=="Y"):
               print("YES!")
               break
         else:
            connection.send(cbmencode("\nError: User already exists.\n"))
            attempts=attempts+1

         if attempts >=maxtries:
            connection.send(cbmencode("Sorry, maximum number of attempts.\nConnection closed. "))
            connection.close()

       attempts=0

       #Asks for password
       while True:
         connection.send(cbmencode("\nType your password: "))
         pass1=input_pass(connection) #input_line function reads a line
         pass1=cbmdecode(pass1)
         connection.send(cbmencode("\nRepeat your password: "))
         pass2=input_pass(connection) #input_line function reads a line
         pass2=cbmdecode(pass2)
         if(pass2==pass1):
           print("->"+pass1+"<-")
           break
         attempts=attempts+1
         if attempts >= maxtries:
            connection.send(cbmencode("Sorry, maximum number of attempts.\nConnection closed. "))
            connection.close()
         connection.send(cbmencode("\nError: Passwords don't match.\nTry Again.\n\n"))

       attempts=0

       #Asks for email
       while True:
         connection.send(cbmencode("\nType your email: "))
         mail1=input_line(connection) #input_line function reads a line
         mail1=cbmdecode(mail1)
         connection.send(cbmencode("\nRepeat your email: "))
         mail2=input_line(connection) #input_line function reads a line
         mail2=cbmdecode(mail2)
         if(mail2==mail1):
           print("email matches!")
           break
         attempts=attempts+1
         if attempts >= maxtries:
            connection.send(cbmencode("Sorry, maximum number of attempts.\nConnection closed. "))
            connection.close()
         connection.send(cbmencode("\nError: Emails don't match.\nTry Again.\n\n"))

       print("Creating account:",uname)
       ## Creates user here
       query="INSERT INTO accounts (username, password, email, active, level) VALUES ('%s','%s','%s',1,1)"
       query=query % (uname,pass1,mail1)
       mycursor.execute(query)
       mydb.commit() #imperative
       realid=mycursor.lastrowid
       print("new id:",realid)
       return uname,realid;

def do_bucle(connection,namex,idx):

         while True:
           #Borra Pantalla y ENVIA MENU
           print("Hola, ",namex,"->",idx)
           connection.send(cbmencode("\n\nSelecciona Opcion: "))
           bucl=get_char(connection)
           print(bucl)
           print("decoded: ",cbmdecode(bucl))


###########################################
# MAIN BBS FUNCTIONS
###########################################

def user_session(connection):

      while True:

         #initializes terminal 

         do_welcome(connection)
         time.sleep(2)

         userx,idx = do_login(connection)

         do_bucle(connection,userx,idx)

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

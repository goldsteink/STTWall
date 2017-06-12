'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *





VERBOSE = False
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 7002 # Arbitrary non-privileged port



 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if VERBOSE:
    print ("Socket created")
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    if VERBOSE:
        print ("Socket bound to:{}".format(PORT)) 
except socket.error as msg:
    print "Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1]
    sys.exit()
     
if VERBOSE:
    print ("Socket bind complete")
 
s.listen(10)
if VERBOSE:
    print ("Socket now listening")
    






#Function for handling connections. This will be used to create threads
def clientthread(conn):
    words = {}
    buffer = ""
    while True:
        data = conn.recv(1)
        if not data: 
            break
        elif data == ';':
            handleWordUpdate(buffer, words)
            buffer = ""
        else:
            buffer += data
                 
    conn.close()



def handleWordUpdate(wordcountpair, words):
    word=""
    count="0"
    try:
        word,count=wordcountpair.split(":")
    except:
        print ("Bad split! {}".format(msg[0]))
        return
        
        
    try:
        theVal = words[word]
        incrInSize = 1 + int(count) # if this is 0, then it will increase it's count
        theVal += incrInSize
        words[word] = theVal
        #if ( VERBOSE ):
        print ("Updated {} to:{}".format(word, theVal))
    except:
        #print("Word {} does not exist in dictionary!".format(word))
        words[word] = 0
        print ("{}->{}".format(word,count))
        return
    

# 
#now keep talking with the client
#
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    if VERBOSE:
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))


s.close()

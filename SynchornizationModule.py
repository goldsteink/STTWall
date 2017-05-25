import SocketServer
from collections import defaultdict
import time

print_phrases=False
glbl_words = defaultdict()
target_file = open ('/tmp/machida.log', 'w')



class MyTCPHandler(SocketServer.BaseRequestHandler):        
    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024).strip()
            #print "{} wrote:".format(self.client_address[0])
            if ( len(self.data) > 0 ):
                self.updateWordCount(self.data)
                self.writeFile()
            else:
                break
    
            
    def updateWordCount(self, data_):
        #
        # be verbse
        #
        if ( print_phrases ):
            print "------------------------"
            print data_
        
        
        #
        # split up the tokens    
        #
        tokens = data_.split(";")
        for t in tokens:
            try:
                word,count=t.split(":")
                delta = int(count)
                if ( delta > 0 ):
                    try:
                        oldcount = glbl_words[word]
                    except:
                        oldcount = 0
                    newcount = delta + oldcount
                    glbl_words[word] = newcount
                    print ("Word:{}, Old-Count:{}, Delta:{}, New-Count:{}".format(word, oldcount, delta, newcount))
            except Exception as inst:
                #print ("Unexpected error:{}".format(inst))
                break


    def writeFile(self):
        strval = ""
        target_file.seek(0)
        target_file.truncate()
        
        target_file.write("\nLast update: " + time.strftime("%H:%M:%S"))
        target_file.write("\n\n");
        for key in glbl_words:
            strval = "{}\t{}\n".format(key, glbl_words[key])
            target_file.write(strval)
        target_file.flush()

if __name__ == "__main__":
    HOST, PORT = "localhost", 7002

    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    #server.socket.setsockopt(level, option, value)
    server.allow_reuse_address = True
    server.serve_forever()

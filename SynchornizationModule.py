import SocketServer
from collections import defaultdict
import time

print_phrases=False
glbl_words = defaultdict()
glbl_list = []
target_file = open ('/tmp/machida.log', 'w')




class Word:
    def __init__(self, word_, count_):
        self._word = word_
        self._count = count_
        
    def update_count(self, delta_):
        self._count += delta_
        
    def get_count(self):
        return self._count

    def __str__(self):
        if ( len(self._word)<8 ):
            return "{}\t\t{}\n".format(self._word, self._count)
        return "{}\t{}\n".format(self._word, self._count)
    
    def __lt__(self, other):
        return self._count > other._count
    

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

                if word.strip(): 
                    try:
                        wordObject = glbl_list[word]
                        oldcount = wordObject.get_count()
                    except:
                        oldcount = 0
                        wordObject = Word(word,oldcount)
                        glbl_list.append(wordObject)
                        
                    newcount = delta + wordObject.get_count()
                    wordObject.update_count(delta)
                    glbl_words[word] = newcount
                    print ("Word:{}, Old-Count:{}, Delta:{}, New-Count:{}".format(word, oldcount, delta, newcount))
            except Exception as inst:
                #print ("Unexpected error:{}".format(inst))
                break


    def writeFile(self):
        strval = ""
        target_file.seek(0)
        target_file.truncate()
        
        target_file.write("\nLast update: " + time.strftime("%H:%M:%S") + "\n\n")
        glbl_list.sort()
        for t in glbl_list:
            target_file.write(str(t))
        target_file.flush()

if __name__ == "__main__":
    HOST, PORT = "localhost", 7002

    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    #server.socket.setsockopt(level, option, value)
    server.allow_reuse_address = True
    server.serve_forever()

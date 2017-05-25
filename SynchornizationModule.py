import SocketServer
from collections import defaultdict
import time

print_phrases=False
glbl_words = defaultdict()
glbl_list = []
target_file = open ('/tmp/machida.log', 'w')




class InstanceCount:
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
                self.updateInstanceCount(self.data)
                self.writeFile()
            else:
                break
    
            
    def updateInstanceCount(self, data_):
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
        if ( tokens == False ):
            pass
        
        for t in tokens:
            if t.strip(): 
                try:
                    word,count=t.split(":")
                    delta = int(count)
                    if word.strip(): 
                        try:
                            wordObject = glbl_words[word]
                            oldcount = wordObject.get_count()
                            newcount = delta + wordObject.get_count()
                            wordObject.update_count(delta)
                            print ("InstanceCount:{}, Old-Count:{}, Delta:{}, New-Count:{}".format(word, oldcount, delta, newcount))
                        except:
                            print ("Not handeling:{}".format(word))
                            pass
                except Exception as inst:
                    print ("Unexpected error:{}".format(inst))
                    #break




    #
    # write stats to a file
    #
    def writeFile(self):
        strval = ""
        target_file.seek(0)
        target_file.truncate()
        
        
        
        glbl_list.sort()
        
        
        #
        # file header
        #
        new_total = 0
        target_file.write("\nLast update: " + time.strftime("%H:%M:%S") + "\n")
        for t in glbl_list:
            new_total += t.get_count()
        target_file.write("Total words found: {}\n\n".format(str(new_total)))    
        
        
        
        #
        # file contents
        #
        for t in glbl_list:
            target_file.write(str(t))
        total_words_counted = new_total
        target_file.flush()









if __name__ == "__main__":
    #
    # populate list of words I want to keep track of
    #
    with open ("./wordlist.txt") as infile:
        for line in infile:
            strword = line.strip()
            w = InstanceCount(strword,0) 
            glbl_words[strword] = w
            glbl_list.append(w)
            print ("Tracking:{}".format(str(w)))
        

    #
    # run server
    #
    HOST, PORT = "localhost", 7002
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.allow_reuse_address = True
    server.serve_forever()

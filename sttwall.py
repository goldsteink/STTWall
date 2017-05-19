import struct
import wallaroo

#import recognize
import sys
sys.argv = ['']
from recog import Recognize

from textblob import TextBlob



def application_setup(args):
    ab = wallaroo.ApplicationBuilder("Computation_SpeechToText")
    ab.new_pipeline("sttw", Decoder())
    ab.to(Computation_SpeechToText)
    ab.to(Computation_SpellCorrect)
    ab.to_sink(Encoder())
    return ab.build()




#
# each message is a file name
#
class Decoder(object):
    def header_length(self):
        #print "header_length"
        return 4

    def payload_length(self, bs):
        #print "payload_length", bs
        return struct.unpack(">I", bs)[0]

    def decode(self, bs):
        #print "decode", bs
        return bs.decode("utf-8")





#
# send text of some sort
#
class Encoder(object):
    def encode(self, data):
        # data is a string
        #print "encode", data
        return data + "\n"




#
# should lookup file, and handle speech to text
#
class Computation_SpeechToText(object):
    def __init__(self):
        self.rec = None

    def name(self):
        return "Computation_SpeechToText"

    def compute(self, data):
        if self.rec == None:
            self.rec = Recognize()
        return self.rec.run(data)



#
# should correct the spelling
#
class Computation_SpellCorrect(object):
    def __init__(self):
        return
    
    def name(self):
        return "Computation_SpellCorrect"

    def compute(self, data):
        tb = TextBlob(data)
        rv = "--------------------------\n[Orig:" + data + "]"
               
        corrected = tb.correct()
        rv += "\n[Corr:" + str(corrected) + "]" 
        
        return rv



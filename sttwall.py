import struct
import wallaroo

#import recognize
import sys
sys.argv = ['']
from recog import Recognize



def application_setup(args):
    ab = wallaroo.ApplicationBuilder("Reverse Word")
    ab.new_pipeline("sttw", Decoder())
    ab.to(Reverse)
    ab.to_sink(Encoder())
    return ab.build()


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


class Reverse(object):
    def __init__(self):
        self.rec = None

    def name(self):
        return "reverse"

    def compute(self, data):
        if self.rec == None:
            self.rec = Recognize()
        return self.rec.run(data)


class Encoder(object):
    def encode(self, data):
        # data is a string
        #print "encode", data
        return data + "\n"

import string
import struct
import pickle
from collections import defaultdict

import wallaroo


#import recognize
import sys
sys.argv = ['']
from recog import Recognize



def application_setup(args):
    partition_count = 2
    partition_list = list();
    for x in range(0, partition_count):
        partition_list.append(x)
    
    ab = wallaroo.ApplicationBuilder("STTWallStatefull")
    ab.new_pipeline("STTWallStatefull", Decoder())
    ab.to_state_partition(Computation_STT(), WordCounterBuilder(), "word counter",
                          RoundRobinPartitionFunction(partition_count), partition_list)
    ab.to_sink(Encoder())
    return ab.build()


def serialize(o):
    return pickle.dumps(o)


def deserialize(bs):
    return pickle.loads(bs)


class RoundRobinPartitionFunction(object):
    def __init__(self, partition_count_):
        self.current_count = 0
        self.partition_count = partition_count_

    def partition(self, data):
        self.current_count += 1
        rv = self.current_count % self.partition_count
        print ("RRPartition, count:{}, rv:{}".format(self.current_count, rv))
        return rv




class WordCounterBuilder(object):
    def __init__(self):
        self.word_counter = WordCounter()
        
    def build(self):
        return self.word_counter
        #return WordCounter()


class WordCounter(object):
    def __init__(self):
        self.words = defaultdict()
        self.word = ""
        self.count = 0

    def update(self, data_):
        try:
            self.count = self.words[data_]
        except KeyError:
            self.count = 0
            
        self.count += 1
        self.words[data_] = self.count
        print ("Updated:{}, Count:{}".format(data_, self.count))
        
        
    def get_word(self):
        return Word(self.word, self.count)


class Word(object):
    def __init__(self, word_, count_):
        self.word = word_
        self.count = count_


class Computation_STT(object):
    def __init__(self):
        self.rec = None
        
    def name(self):
        return "add votes"

    def compute(self, data_, state_):
        print ("data:{}".format(data_))
        
        #if self.rec == None:
        #    self.rec = Recognize()
        #the_text = self.rec.run(data_)
        
        the_text = data_
        words = the_text.split()
        for w in words:
            state_.update(w)
            
        return (state_.get_word(), True)




class Decoder(object):
    def header_length(self):
        return 4

    def payload_length(self, bs):
        return struct.unpack(">I", bs)[0]

    def decode(self, bs):
         return bs.decode("utf-8")

class Encoder(object):
    def encode(self, data):
        rv = data.word
        rv += ":" 
        rv += str(data.count)
        return rv + "\n"
    
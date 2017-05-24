import time
import string
import struct
import pickle
from collections import defaultdict
import datetime

import wallaroo



#import recognize
import sys
sys.argv = ['']
from recog import Recognize
rec = Recognize()



print_phrase=False
print_not_valid_words=False

def application_setup(args):
    
    partition_count = 4
    partition_list = list();
    for x in range(0, partition_count):
        partition_list.append(x)
        
    syncpoint_list = list()
    syncpoint_list.append("0")
    
    ab = wallaroo.ApplicationBuilder("STTWallStatefull")
    ab.new_pipeline("STTWallStatefull", Decoder())
    ab.to_state_partition(Computation_STT(), 
                          WordCounterBuilder(), "word counter",
                          RoundRobinPartitionFunction(partition_count), 
                          partition_list)
    #ab.to_state_partition(Computation_SyncPoint(), 
    #                      SyncPointBuilder(), "sync-point",
    #                      SynchornizationPointPartition(), 
    #                      syncpoint_list)
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
        #return self.word_counter
        return WordCounter()


class WordCounter(object):
    def __init__(self):
        self.words = defaultdict()
        self.word = ""
        self.count = 0
        self.valid_words = {}
        
        file = "/home/kgoldstein/dev/eclipse_projects/STTWall/wordlist.txt"
        print ("Valid dictionary words: {}".format(file))
        with open (file, "r") as myfile:
            for line in myfile:
                self.valid_words[line.rstrip()] = True
        
        print ("Number of words loaded:{}".format(len(self.valid_words)))
        

    def update(self, data_):
        try:
            if self.valid_words[data_] != True:
                if ( print_not_valid_words ):
                    print ("Word is not a valid word:{}".format(data_))
                return data_ + ":0"
        except KeyError:
            if ( print_not_valid_words ):
                print ("Not a valid SAT word:{}".format(data_))
            rv = data_ + ":0"
            return  rv# I am not tracking this as an SAT word    
                 
        try:
            self.count = self.words[data_]
        except KeyError:
            self.count = 0
            
        self.count += 1
        self.words[data_] = self.count
        
        
        print ("Updated:{}, Count:{}".format(data_, self.count))
        rv = data_
        rv += ":"
        #rv += str(self.count)
        rv += "1"
        return rv
      

class Word(object):
    def __init__(self, word_, count_):
        self.word = word_
        self.count = count_


class Computation_STT(object):
    def __init__(self):
        self.rec = None
        
    def name(self):
        return "word count"

    def compute(self, data_, state_):
        print ("data:{}".format(data_))
        
        a = datetime.datetime.now()
        the_text = rec.run(data_)
        
        if ( print_phrase ):
            print the_text
            
        words = the_text.split()
        rv = ""
        for w in words:
            rv += state_.update(w.strip())
            rv += ";"
            
        b = datetime.datetime.now()
        c = b - a
        print ("Total time: {} milliseconds".format(int(c.total_seconds() * 1000)))
        return (rv, True)


class Decoder(object):
    def header_length(self):
        return 4

    def payload_length(self, bs):
        return struct.unpack(">I", bs)[0]

    def decode(self, bs):
         return bs.decode("utf-8")

class Encoder(object):
    def encode(self, data_):
        print ("Encode, data: {}".format(data_, type(data_)))
        return data_ + "\n"
 


#
# the sync point stuff
#
class SynchornizationPointPartition(object):
    def __init__(self):
        print "SynchornizationPoint"

    def partition(self, data):
        print ("SynchornizationPoint::partition - returning 'a'")
        return "0"
    
class SyncPointBuilder(object):
    def __init__(self):
        print "SyncPointBuilder"
        #self.sync_point = SyncPoint()
        
    def build(self):
        print "SyncPointBuilder::build - returning SyncPoint()"
        return SyncPoint()

    
class SyncPoint(object):
    def __init__(self):
        print "SyncPoint"
        self.count = 0
    
    def update(self, data_):
        rv = "SyncPoint::update:"
        rv += str(self.count)
        print rv
        self.count+=1
        return rv

class Computation_SyncPoint(object):
    def __init__(self):
        print "Computation_SyncPoint" 
        
    def name(self):
        return "SyncPointComputation"

    def compute(self, data_, state_):
        print ("Computation_SyncPoint::compute:data={}".format(data_))
        a = datetime.datetime.now()
        rv = state_.update(data_)
        b = datetime.datetime.now()
        c = b - a
        print ("Total time: {} milliseconds".format(int(c.total_seconds() * 1000)))
        return (rv, True)
    
    
    

if __name__ == "__main__":
    w = WordCounter();
    workd = "i"
    w.update(workd)
    
    
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0001.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0002.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0003.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0004.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0004.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0005.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0006.flac")
    print rec.run("/home/kgoldstein/Downloads/LibriSpeech/test-clean/1580/141083/1580-141083-0007.flac")
    
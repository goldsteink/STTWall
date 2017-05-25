# -*- coding: utf-8 -*-
import sys
import sugartensor as tf
import numpy as np
import librosa
from model import *
import sttwdata


__author__ = 'namju.kim@kakaobrain.com'


class Recognize:
    def __init__(self):
        # set log level to debug
        tf.sg_verbosity(10)

        # batch size
        self.batch_size = 1

        # vocabulary size
        self.voca_size = sttwdata.voca_size
        
        # mfcc feature of audio
        self.x = tf.placeholder(dtype=tf.sg_floatx, shape=(self.batch_size, None, 20))

        # encode audio feature
        self.logit = get_logit(self.x, voca_size=self.voca_size)
        
        # sequence length except zero-padding
        self.seq_len = tf.not_equal(self.x.sg_sum(axis=2), 0.).sg_int().sg_sum(axis=1)
        
        # run network
        self.session = tf.Session()
        tf.sg_init(self.session)
        self.saver = tf.train.Saver()
        self.saver.restore(self.session, tf.train.latest_checkpoint('asset/train'))



    def run(self,datafile):
        # ctc decoding
        decoded, _ = tf.nn.ctc_beam_search_decoder(self.logit.sg_transpose(perm=[1, 0, 2]), self.seq_len, merge_repeated=False)

        # to dense tensor
        y = tf.sparse_to_dense(decoded[0].indices, decoded[0].dense_shape, decoded[0].values) + 1
     
        # load wave file
        wav, _ = librosa.load(datafile, mono=True, sr=16000)

        # get mfcc feature
        mfcc = np.transpose(np.expand_dims(librosa.feature.mfcc(wav, 16000), axis=0), [0, 2, 1])
        
        # run session
        label = self.session.run(y, feed_dict={self.x: mfcc})
        
        # return string
        return sttwdata.index_as_string(label)
        
        



if __name__ == "__main__":
    d1 = sys.argv[1]
    d2 = sys.argv[2]
    
    r=Recognize()
    print "R1:", r.run(d1)
    print "R2:", r.run(d2)


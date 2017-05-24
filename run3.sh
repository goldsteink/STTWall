#!/bin/bash
export PATH="$PATH:/home/kgoldstein/wallaroo-tutorial/wallaroo/machida/build"
export PYTHONPATH="$PYTHONPATH:/home/kgoldstein/wallaroo-tutorial/wallaroo/machida"
taskset -c 3 \
machida \
--application-module RecognizeInWallaroo \
--in 127.0.0.1:7010 \
--out 127.0.0.1:7002 --metrics 127.0.0.1:5001 --control 127.0.0.1:6000 \
--data 127.0.0.1:6001 --worker-count 4 --name worker-3 --ponythreads=1

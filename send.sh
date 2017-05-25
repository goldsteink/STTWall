#!/bin/bash
/home/ubuntu/wallaroo-tutorial/wallaroo/giles/sender/sender \
--host 127.0.0.1:7010 \
--file files.txt \
--batch-size 1 \
--interval 100_000_000 \
--messages 2000 \
--ponythreads=1 \
--repeat

#--repeat \

#!/bin/bash
export PATH="$PATH:/home/ubuntu/wallaroo-tutorial/wallaroo/machida/build"
export PYTHONPATH="$PYTHONPATH:/home/ubuntu/wallaroo-tutorial/wallaroo/machida"

WORKER_COUT=15
echo "Starting worker: intializer, cpu:$WORKER_COUT"
taskset -c $WORKER_COUT \
machida \
--application-module RecognizeInWallaroo \
--in 127.0.0.1:7010 \
--out 127.0.0.1:7002 --metrics 127.0.0.1:5001 --control 127.0.0.1:6000 \
--data 127.0.0.1:6001 --worker-count $WORKER_COUT --topology-initializer \
--ponythreads=1 > run.log.initializer 2>&1 &

name=""
for i in `seq 0 14`
do
    sleep 2
    name="worker-$i"
    echo "Starting worker: $name, CPU: $i"
    taskset -c $i \
	machida \
	--application-module RecognizeInWallaroo \
	--in 127.0.0.1:7010 \
	--out 127.0.0.1:7002 --metrics 127.0.0.1:5001 --control 127.0.0.1:6000 \
	--data 127.0.0.1:6001 --worker-count $WORKER_COUT --name $name \
	--ponythreads=1 > run.log.$i 2>&1 &
done

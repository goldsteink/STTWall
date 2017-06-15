#!/bin/bash
COLOR=~/.local/scrpt/color.sh
if [ -e $COLOR ] ; then
	source $COLOR
	print=print
else
	print=echo
fi

BIN=~/wallaroo-tutorial/wallaroo/giles/receiver/receiver
if [ ! -e $BIN ] ; then
	$print ERR "Cannot find receiver!"
	$print ERR "Looking for: $BIN"
	exit 1
fi

#pushd ../var
LISTEN_PORT=7002
METRICS=127.0.0.1:5001
$print DBG "Listenign on port: $LISTEN_PORT"
$print DBG "Publishing metrics on:$METRICS"
$BIN --listen 0.0.0.0:$LISTEN_PORT --metrics $METRICS
#popd


#!/bin/bash
COLORS=/home/kgoldstein/.local/scrpt/color.sh
if [ -e $COLORS ] ; then
	source $COLORS
	print=print
else
	print=echo
fi



BIN=~/wallaroo-tutorial/wallaroo/giles/sender/sender
command -v $BIN >/dev/null 2>&1 || { $print ERR "I require $BIN but it's not installed.  Aborting." >&2; exit 1; }

DATAFILE=files.10
MESSAGECNT=`wc -l $DATAFILE | cut -f 1 -d ' '`

if [ ! -e $DATAFILE ] ; then
    $print ERR "Datafile not prsent. Looking for: $DATAFILE"
    exit 1
else
    $print INF "Staring sender, data file: $DATAFILE"
    $print INF "Will send: $MESSAGECNT messages"
fi
$BIN \
--host 127.0.0.1:7010 \
--file $DATAFILE \
--batch-size 1 \
--interval 100_000_000 \
--messages $MESSAGECNT \
--ponythreads=1 
#--repeat \

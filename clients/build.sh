#!/bin/bash

SKETCH=$1

if [ ! -d $SKETCH ]; then
    echo Unknown sketch was specified 
    exit 1
fi

[ -f $SKETCH/secrets.h ] && rm $SKETCH/secrets.h

grep -ve "^\#" *.secret | grep "\S" | cut -d# -f1 | \
    awk '{print "#define " $1 " \"" $2"\""}' > $SKETCH/secrets.h

FQBN=`grep FQBN build_config | awk '{print $2}'`
PORT=`grep PORT build_config | awk '{print $2}'`

echo $FQBN
echo $PORT

arduino-cli compile --fqbn $FQBN $SKETCH
[ $? != "0" ] && exit 1
arduino-cli upload -p $PORT --fqbn $FQBN $SKETCH
#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$(uname)" == 'Linux' ]; then
    COMMAND=aplay
elif [ "$(uname)" == 'Darwin' ]; then
    COMMAND=afplay
fi
time dropdb -h localhost goattower && createdb -h localhost goattower && python ${BASEDIR}/../load.py ${BASEDIR}/../objects/test_location.yaml yaml || python ${BASEDIR}/../load.py ${BASEDIR}/../objects/test_location.yaml yaml && ${COMMAND} ${BASEDIR}/dogbark4.wav

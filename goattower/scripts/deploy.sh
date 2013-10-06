#!/bin/bash
time dropdb -h localhost goattower && createdb -h localhost goattower && python ../load.py ../objects/test_location.yaml yaml || python ../load.py ../objects/test_location.yaml yaml && afplay ./dogbark4.wav

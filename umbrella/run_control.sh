#!/bin/bash

while true;
do
    ./check_frames.sh
    ./restart_error.sh
    ./restart_incomplete.sh
    sleep 1800
done

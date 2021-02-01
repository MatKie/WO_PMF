#!/bin/bash

 
while read line; 
do
    cd ${line}
    qsub ${line}_UMBRELLA.sh
    cd ..
done < frames.raw

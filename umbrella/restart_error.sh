#!/bin/bash

while read line;
do
    cd $line
    qsub ${line}_UMBRELLA.sh
    cd ..
    echo 'Restarted '$line
done < error.txt

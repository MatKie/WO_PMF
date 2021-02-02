#!/bin/bash

while read line;
do
    cp RESTART_PROD.sh ${line}/${line}_CONT.sh
    cd $line
    sed -i s/WINDOW/${line}/g ${line}_CONT.sh
    qsub ${line}_CONT.sh
    cd ..
    echo 'Restarted '$line
done < incomplete.txt

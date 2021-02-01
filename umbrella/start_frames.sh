#!/bin/bash

 
while read line; 
do
    cd ${line}
    rm *.sh.e*
    rm *.sh.o*
    qsub ${line}_UMBRELLA.sh
    cd ..
done < error.txt

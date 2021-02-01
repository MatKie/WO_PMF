#!/bin/bash
touch force-files.dat
touch tpr-files.dat

if [ -f force-files.dat ] ;
then 
    rm force-files.dat
fi 

if [ -f tpr-files.dat ] ;
then 
    rm tpr-files.dat
fi 

while read line; 
do
    echo "${line}/prod/umbrella${line}f.xvg" >> force-files.dat 
    echo "${line}/prod/umbrella${line}.tpr" >> tpr-files.dat 
done < complete.txt


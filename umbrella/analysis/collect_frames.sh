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
    echo "../${line}/prod/umbrella${line}f.xvg" >> force-files.dat 
    echo "../${line}/prod/umbrella${line}.tpr" >> tpr-files.dat 
done < ../complete.txt

if [ -f lhs.txt ];
then
    if [ -f lhs-force-files.dat ] ;
    then 
        rm lhs-force-files.dat
    fi 

    if [ -f lhs-tpr-files.dat ] ;
    then 
        rm lhs-tpr-files.dat
    fi 
    while read line; 
    do
        echo "../${line}/prod/umbrella${line}f.xvg" >> lhs-force-files.dat 
        echo "../${line}/prod/umbrella${line}.tpr" >> lhs-tpr-files.dat 
    done < lhs.txt
fi

if [ -f rhs.txt ];
then
    if [ -f rhs-force-files.dat ] ;
    then 
        rm rhs-force-files.dat
    fi 

    if [ -f rhs-tpr-files.dat ] ;
    then 
        rm rhs-tpr-files.dat
    fi 
    while read line; 
    do
        echo "../${line}/prod/umbrella${line}f.xvg" >> rhs-force-files.dat 
        echo "../${line}/prod/umbrella${line}.tpr" >> rhs-tpr-files.dat 
    done < rhs.txt

fi


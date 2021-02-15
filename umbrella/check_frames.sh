#!/bin/bash

restart_inc=false
nsteps=2000001
n_total=0
n_compl=0
n_incompl=0
n_error=0
if [ -f 'complete.txt' ];
then    
    rm complete.txt incomplete.txt error.txt
fi
touch complete.txt
touch incomplete.txt
touch error.txt

while read line; 
do
    n_total=$((n_total+1))
    file=${line}/prod/umbrella${line}.log
    if [ -f $file ]; 
    then 
        if grep -q 'Statistics over '${nsteps}' steps using' $file
        then 
            n_compl=$((n_compl+1))
            echo $line >> complete.txt
        else
            if qstat | grep -q ${line}'_'
            then
                echo 'Still continuing: '${line}
            else
                n_incompl=$((n_incompl+1))
                echo 'Did not fully complete '${line}' window'
                echo $line >> incomplete.txt
                if $restart_inc;
                then 
                    cp RESTART_PROD.sh ${line}/prod/${line}_CONT.sh
                    cd $line
                    cd prod
                    sed -i s/WINDOW/${line}/g ${line}_CONT.sh
                    qsub ${line}_CONT.sh
                    cd ../..
                    echo 'Restarted '$line
                fi
            fi
        fi
    else
        if qstat | grep -q ${line}'_' 
        then 
            echo 'Still running: '${line}
        else
            echo 'Error in '${line}' window'
            n_error=$((n_error+1))
            echo $line >> error.txt
        fi
    fi 
done < frames_original.raw

echo 'Complete windows  : '$n_compl
echo 'Incomplete windows: '$n_incompl
echo 'Erroreous windows : '$n_error  

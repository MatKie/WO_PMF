#!/bin/bash

#################################################
# get_distances.sh
#
#   Script iteratively calls gmx distance and
#   assembles a series of COM distance values
#   indexed by frame number, for use in
#   preparing umbrella sampling windows.
#
# Written by: Justin A. Lemkul, Ph.D.
#    Contact: jalemkul@vt.edu
#
#################################################

if [ ! -d gro_files ];
then
    mkdir gro_files
fi

echo 0 | gmx trjconv -s ../nvt_pull/topol.tpr -f ../nvt_pull/traj.trr -o gro_files/conf.gro -n index.ndx -sep -pbc whole 

frames=3201

# compute distances
for (( i=0; i<${frames}; i++ ))
do
    gmx distance -s ../nvt_pull/topol.tpr -f gro_files/conf${i}.gro -n index.ndx -select 'com of group SOL plus com of group solute' -oxyz dist${i}.xvg 
done

# compile summary
touch summary_distances.dat
for (( i=0; i<${frames}; i++ ))
do
    d=`tail -n 1 dist${i}.xvg | awk '{print $4}'`
    echo "${i} ${d}" >> summary_distances.dat
    rm dist${i}.xvg
done

exit;

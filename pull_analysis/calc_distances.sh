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

echo 0 | gmx trjconv -s ../npt_pull/topol.tpr -f ../npt_pull/traj.trr -o gro_files/conf.gro -n ../npt_pull/index.ndx -sep -pbc cluster <<EOF
micelle
system
EOF
frames=441
# compute distances
for (( i=0; i<${frames}; i++ ))
do
    gmx distance -s ../npt_pull/topol.tpr -f gro_files/conf${i}.gro -n ../npt_pull/index.ndx -select 'com of group "micelle" plus com of group "monomer"' -oall dist${i}.xvg 
done

# compile summary
touch summary_distances.dat
for (( i=0; i<${frames}; i++ ))
do
    d=`tail -n 1 dist${i}.xvg | awk '{print $2}'`
    echo "${i} ${d}" >> summary_distances.dat
    rm dist${i}.xvg
done

exit;

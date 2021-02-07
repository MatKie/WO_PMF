#!/bin/bash

traj='traj.xtc'
index='index_analysis.ndx'
begin=5000
width=0.005

gmx sasa -f ../$traj -s ../topol.tpr -n ../$index -b $begin -output 'name C1 C2 C3 C4; name SU' <<EOF
group SDS
EOF

gmx gyrate -f ../$traj -s ../topol.tpr -n ../$index -b $begin <<EOF
group SDS
EOF


gmx principal -n ../$index -f ../$traj -s ../topol.tpr -b $begin <<EOF
group SDS
EOF

gmx rdf -bin $width -f ../$traj -s ../topol.tpr -n ../$index -ref 'com of name C1 C2 C3 C4 SU' -b $begin <<EOF
group CM
group CT
group SO4V9
group SOL
group 9
group CM_CT
EOF


gmx rdf -bin $width -f ../$traj -s ../topol.tpr -n ../$index -ref 'com of name C1 C2 C3 C4 SU' -b $begin -norm none -o rdf_no_norm.xvg <<EOF
group CM
group CT
group SO4V9
group SOL
group 9
group CM_CT
EOF

gmx rdf -bin $width -f ../$traj -s ../topol.tpr -b $begin -o rdf_headgroup.xvg -n ../$index <<EOF
group SO4V9
group SOL
group 9
group SO4V9
EOF


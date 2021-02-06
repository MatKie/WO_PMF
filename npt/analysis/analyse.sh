#!/bin/bash

traj='traj.xtc'
index='index_analysis.ndx'
begin=5000
width=0.005

gmx sasa -f ../$traj -s ../topol.tpr -n ../$index -b $begin -output 'name C1 C2 C3 C4; name SU' <<EOF
2
EOF

gmx gyrate -f ../$traj -s ../topol.tpr -n ../$index -b $begin <<EOF
2
EOF


gmx principal -f ../$traj -s ../topol.tpr -b $begin <<EOF
2
EOF

gmx rdf -bin $width -f ../$traj -s ../topol.tpr -n ../$index -ref 'com of name C1 C2 C3 C4 SU' -b $begin <<EOF
11
12
14
4
3
13
EOF


gmx rdf -bin $width -f ../$traj -s ../topol.tpr -n ../$index -ref 'com of name C1 C2 C3 C4 SU' -b $begin -norm none -o rdf_no_norm.xvg <<EOF
11
12
14
4
3
13
EOF

gmx rdf -bin $width -f ../$traj -s ../topol.tpr -b $begin -o rdf_headgroup.xvg -n ../$index <<EOF
14
4
3
14
EOF


#!/bin/bash

gmx energy -f ../ener.edr -b 10000 > energies.out  <<EOF
1
2
3
4
5
6
7
8
9
10
20
24
28
29
EOF

gmx density -f ../traj.trr -s ../topol.tpr -b 10000 -ng 2 -symm yes -o density_mass.xvg <<EOF
2
2
3
EOF

gmx density -f ../traj.trr -s ../topol.tpr -b 10000 -ng 2 -symm yes -dens number -o density_number.xvg <<EOF
2
2
3
EOF

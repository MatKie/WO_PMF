#!/bin/bash

rm energies.out

gmx energy  -f ../ener.edr -b 1000 >> energies.out <<EOF
27
31
35
36
EOF

#27
#31
#35

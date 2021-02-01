#!/bin/bash
cd ../

mkdir ../umbrella/XXX
mkdir ../umbrella/XXX/eq
mkdir ../umbrella/XXX/prod
cp runfiles/frame-XXX_GROMACS_UMBRELLA.sh ../umbrella/XXX/XXX_UMBRELLA.sh
cp topol.top ../umbrella/XXX
cp index.ndx ../umbrella/XXX

cp min_dist_numpy.py ../umbrella/XXX/eq
cp gro_files/confXXX.gro ../umbrella/XXX/eq
cp npt_umbrella.mdp ../umbrella/XXX/eq
cp pull.tpr ../umbrella/XXX/eq


cp min_dist_numpy.py ../umbrella/XXX/prod
cp md_umbrella.mdp ../umbrella/XXX/prod

cd ../umbrella/XXX/eq
gmx pairdist -s pull.tpr -f confXXX.gro -n ../index.ndx -seltype atom -selgrouping none -sel 'group sol'  -ref 'com of group solute'
python min_dist_numpy.py dist.xvg npt_umbrella.mdp 
rm pull.tpr
cd ../../../pull_analysis

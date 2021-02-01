#PBS -lselect=1:ncpus=32:mem=2gb
#PBS -lwalltime=06:00:00

#module load intel-suite 
#module load mpi 
module load gromacs/2019.3
module load anaconda3/personal

FOLDERNAME=$PBS_JOBID
EPHEMERAL_SCRATCH=$EPHEMERAL/Scratch
RUNPATH=$EPHEMERAL_SCRATCH/$FOLDERNAME
GMXLIB=/rds/general/user/mk8118/home/2021/PMF_Water_Oil/CarbonFF/tables


mkdir $RUNPATH
cp -r $PBS_O_WORKDIR/* $RUNPATH/

cd $RUNPATH

cp $GMXLIB/* $RUNPATH/eq
cp $GMXLIB/* $RUNPATH/prod

cd eq

# Short equilibration
gmx grompp -f npt_umbrella.mdp -c confXXX.gro -p ../topol.top -n ../index.ndx -o nptXXX.tpr
gmx mdrun -maxh 2 -ntmpi 32 -c nptXXX.gro -s nptXXX.tpr -o nptXXX.trr -x nptXXX_comp.xtc -cpo nptXXX.cpt -e nptXXX.edr -g nptXXX.log -px nptXXXx.xvg -pf nptXXXf.xvg
rm table*.xvg

gmx pairdist -s nptXXX.tpr -f nptXXX.gro -n ../index.ndx -seltype atom -selgrouping none -sel 'group sol'  -ref 'com of group sol'

cp -r $RUNPATH/eq/* $PBS_O_WORKDIR/eq/

cd ../prod

python min_dist_numpy.py ../eq/dist.xvg md_umbrella.mdp 

# Umbrella run
gmx grompp -f md_umbrella.mdp -c ../eq/nptXXX.gro -t ../eq/nptXXX.cpt -p ../topol.top -n ../index.ndx -o umbrellaXXX.tpr
gmx mdrun -maxh 4 -ntmpi 32 -c umbrellaXXX.gro -s umbrellaXXX.tpr -o umbrellaXXX.trr -x umbrellaXXX_comp.xtc -cpo umbrellaXXX.cpt -e umbrellaXXX.edr -g umbrellaXXX.log -px umbrellaXXXx.xvg -pf umbrellaXXXf.xvg

rm table*.xvg

cp -r $RUNPATH/prod/* $PBS_O_WORKDIR/prod/

cd $PBS_O_WORKDIR

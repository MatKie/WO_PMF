#PBS -lselect=1:ncpus=32:mem=2gb
#PBS -lwalltime=18:00:00

#module load intel-suite 
#module load mpi 
module load gromacs/2019.3
module load anaconda3/personal

FOLDERNAME=$PBS_JOBID
EPHEMERAL_SCRATCH=$EPHEMERAL/Scratch
RUNPATH=$EPHEMERAL_SCRATCH/$FOLDERNAME
GMXLIB=/rds/general/user/mk8118/home/CODE/saftv1.ff/tables


mkdir $RUNPATH
cp -r $PBS_O_WORKDIR/* $RUNPATH/

cd $RUNPATH

cp $GMXLIB/* $RUNPATH/prod

cd eq

cd ../prod


# Umbrella run
gmx mdrun -cpi umbrellaWINDOW.cpt -maxh 18 -ntmpi 32 -c umbrellaWINDOW.gro -s umbrellaWINDOW.tpr -o umbrellaWINDOW.trr -x umbrellaWINDOW_comp.xtc -cpo umbrellaWINDOW.cpt -e umbrellaWINDOW.edr -g umbrellaWINDOW.log -px umbrellaWINDOWx.xvg -pf umbrellaWINDOWf.xvg

rm table*.xvg

cp -r $RUNPATH/prod/* $PBS_O_WORKDIR/prod/

cd $PBS_O_WORKDIR

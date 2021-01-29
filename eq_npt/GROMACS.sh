#PBS -lselect=1:ncpus=32:mem=2gb
#PBS -lwalltime=06:00:00

#module load intel-suite 
#module load mpi 
module load gromacs/2019.3

FOLDERNAME=$PBS_JOBID
EPHEMERAL_SCRATCH=$EPHEMERAL/Scratch
RUNPATH=$EPHEMERAL_SCRATCH/$FOLDERNAME

mkdir $RUNPATH
cp -r $PBS_O_WORKDIR/* $RUNPATH/

cd $RUNPATH

GMXLIB=/rds/general/user/mk8118/home/2021/PMF_Water_Oil/CarbonFF/tables
cp $GMXLIB/* $RUNPATH

#OMP_NUM_THREADS=1
#MPI_NUM_THREADS=32

gmx mdrun -maxh 6 -ntmpi 32 -s topol.tpr   

rm GROMACS.sh.*
rm table*.xvg

cp -r $RUNPATH/* $PBS_O_WORKDIR/
cd $PBS_O_WORKDIR

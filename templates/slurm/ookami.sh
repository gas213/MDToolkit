#!/bin/sh

# From MDToolkit template file: ookami.sh

# REPLACE THE {{FIELDS}}

# Ookami partitions: short (4h), medium (12h), long (2d), extended (14h)

#SBATCH --partition={{short, medium, long, extended}}
#SBATCH --time={{d-hh:mm:ss}}
#SBATCH --nodes={{n}}
#SBATCH --ntasks-per-node=48
#SBATCH --job-name {{name}}
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

module purge
module load slurm
module load lammps/gcc13.2.0/29Sept2024

cd ${SLURM_SUBMIT_DIR}

mpirun -np $SLURM_NTASKS lmp_mpi -in {{file.in}}
 
exit
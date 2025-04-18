#!/bin/sh

# REPLACE THE {{FIELDS}}
# Maximum run time on Ookami short is 4 hours

#SBATCH --partition=short
#SBATCH --time={{d-hh:mm:ss}}
#SBATCH --nodes={{num_nodes}}
#SBATCH --ntasks-per-node=48
#SBATCH --job-name {{job_name}}
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

module purge
module load lammps/gcc12/29Sep2021

cd ${SLURM_SUBMIT_DIR}

mpirun -np $SLURM_NTASKS lmp_mpi -in {{in_file}}
 
exit
#!/bin/sh

# REPLACE THE {{FIELDS}}
# Maximum run time on rapids/hawkcpu is 3 days

#SBATCH --partition={{rapids, hawkcpu}}
#SBATCH --time={{d-hh:mm:ss}}
#SBATCH --nodes={{num_nodes}}
#SBATCH --ntasks-per-node={{64, 50}}
#SBATCH --job-name {{job_name}}
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

module purge
module load gcc/12.4.0
module load openmpi/5.0.5
module load lammps/20240829.1

cd ${SLURM_SUBMIT_DIR}

mpirun -np $SLURM_NTASKS `which lmp` -in {{in_file}}
 
exit

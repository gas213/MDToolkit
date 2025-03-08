#!/bin/sh

# REPLACE THE {{FIELDS}}
# Maximum run time on eng is 3 days

#SBATCH --partition=eng
#SBATCH --time={{d-hh:mm:ss}}
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=22
#SBATCH --job-name {{job_name}}
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

# Specify legacy modules (required after Sol upgrade Jan 2025)
# NOTE: You must run clearLmod command in the terminal before queueing this job
# NOTE: Infiniband no longer works with legacy modules; can only run on one node
source /share/Apps/legacy.sh

module purge
module load intel/2021.3.0
module load mvapich2/2.3.4
module load lammps/20210310

cd ${SLURM_SUBMIT_DIR}

mpirun -np $SLURM_NTASKS `which lmp` -in {{in_file}}
 
exit

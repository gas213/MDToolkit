#!/bin/bash

# NTASKS-PER-NODE MUST BE 1 (otherwise it will run the same installation commands multiple times)

# vvv REPLACE THE {{FIELDS}} vvv

#SBATCH --partition={{partition_name}}
#SBATCH --time=06:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name md_install
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

cd ${SLURM_SUBMIT_DIR}

srun sh spack_md.sh

exit
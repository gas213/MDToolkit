#!/bin/sh

# From MDToolkit template file: sol_new.sh

# REPLACE THE {{FIELDS}}

# Partitions info:
# rapids: max 3 days, 64 CPUs per node
# hawkcpu: max 3 days, 50 CPUs per node
# rapids-express: max 2 hours, 6 CPUs total

#SBATCH --partition={{rapids, hawkcpu, rapids-express}}
#SBATCH --time={{d-hh:mm:ss}}
#SBATCH --nodes={{n}}
#SBATCH --ntasks-per-node={{64, 50, 6}}
#SBATCH --job-name={{name}}
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

module purge
module load gcc/12.4.0
module load openmpi/5.0.5
module load lammps/20240829.1

cd ${SLURM_SUBMIT_DIR}

mpirun -np $SLURM_NTASKS `which lmp` -in {{file.in}}
 
exit

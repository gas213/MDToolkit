#!/bin/bash

# vvv REPLACE THE {{FIELDS}} vvv

#SBATCH --partition=cpu
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name md_install
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

cd ${SLURM_SUBMIT_DIR}

module load CMake GCC Python WebProxy

git clone -c feature.manyFiles=true --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git /scratch/user/$USER/spack
. /scratch/user/$USER/spack/share/spack/setup-env.sh

spack env activate .
spack external find --all
spack concretize --force
spack install

exit
#!/bin/bash

#SBATCH --partition=cpu
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name md_install
#SBATCH --output="job.%j.%N.out"

cd ${SLURM_SUBMIT_DIR}

module purge
module load CMake GCC/15.2.0 Python WebProxy

git clone -c feature.manyFiles=true --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git $PROJECT/spack
. $PROJECT/spack/share/spack/setup-env.sh

spack env activate .
spack compiler find
spack external find --all
spack concretize --force
spack install

exit
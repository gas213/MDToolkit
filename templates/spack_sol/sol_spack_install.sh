#!/bin/bash

#SBATCH --partition=rapids
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name=md_install
#SBATCH --output="job.%j.%N.out"

cd ${SLURM_SUBMIT_DIR}

git clone -c feature.manyFiles=true --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh

spack env activate .
# Sol's curl package was causing build issues
spack external find --all --exclude curl
spack concretize --force
spack install

exit
#!/bin/bash

#SBATCH -A mch260155
#SBATCH --partition=debug
#SBATCH --time=0-01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name=md_install
#SBATCH --output="job.%j.%N.out"

cd ${SLURM_SUBMIT_DIR}

git clone -c feature.manyFiles=true --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git $PROJECT/spack
. $PROJECT/spack/share/spack/setup-env.sh

spack env activate .
spack external find --all
spack concretize --force
spack install

exit
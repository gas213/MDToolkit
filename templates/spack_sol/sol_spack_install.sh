#!/bin/bash

# vvv REPLACE THE {{FIELDS}} vvv

# Partitions info:
# rapids: max 3 days, 64 cores per node
# hawkcpu: max 3 days, 50 cores per node
# rapids-express: max 2 hours, max 6 cores
# hawkcpu-express: max 6 hours, max 6 cores

#SBATCH --partition={{rapids, hawkcpu, rapids-express, hawkcpu-express}}
#SBATCH --time={{d-hh:mm:ss}}
#SBATCH --nodes={{n}}
#SBATCH --ntasks-per-node={{64, 50, 6}}
#SBATCH --job-name=md_install
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

cd ${SLURM_SUBMIT_DIR}

git clone -c feature.manyFiles=true --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git ~/ebw210_093025/shared/spack
. ~/ebw210_093025/shared/spack/share/spack/setup-env.sh

spack env activate .
# Sol's curl package was causing build issues
spack external find --all --exclude curl
spack concretize --force
spack install

exit
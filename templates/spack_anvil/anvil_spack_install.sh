#!/bin/bash

# vvv REPLACE THE {{FIELDS}} vvv

# Partitions info - all nodes have 128 cores
# NOTE: wholenode and wide are node-exclusive (a whole node will be reserved and charged to you even if you request a partial node)
# debug: max 2 hours and 2 nodes per job, max 1 job at a time
# shared (default): max 96 hours and 1 node per job, max 1280 cores queued in total
# wholenode (node-exclusive): max 96 hours and 16 nodes per job, max 64 jobs at a time
# wide (node-exclusive): max 12 hours and 56 nodes per job, max 5 jobs at a time

#SBATCH -A mch250010
#SBATCH --partition=debug
#SBATCH --time=0-02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --job-name=md_install
#SBATCH --output="job.%j.%N.out"
#SBATCH --mail-type=ALL
#SBATCH --mail-user={{email}}

cd ${SLURM_SUBMIT_DIR}

git clone -c feature.manyFiles=true --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git $PROJECT/spack
. $PROJECT/spack/share/spack/setup-env.sh

spack env activate .
spack external find --all
spack concretize --force
spack install

exit
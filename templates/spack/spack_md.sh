#!/bin/bash

git clone --depth=2 https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh

spack env create md spack.yaml
spack env activate md
spack install
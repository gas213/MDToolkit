#!/bin/bash

. spack/share/spack/setup-env.sh

spack env create md spack.yaml
spack env activate md
spack install
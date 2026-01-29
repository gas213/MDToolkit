## Spack MD Environment Setup Instructions

1. Create folder (ex. "md_env") in home space which will contain the spack environment
2. Navigate into md_env and clone the Spack repository: `git clone --depth=2 https://github.com/spack/spack.git`
3. Upload files into md_env:
    - slurm_install_md.sh
    - spack_md.sh
    - spack.yaml
4. Fill out any fields in slurm_install_md.sh and queue it via `sbatch slurm_install_md.sh`
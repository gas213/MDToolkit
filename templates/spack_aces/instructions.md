## Spack MD Environment Setup Instructions

1. Edit $HOME/.bashrc and add the following line to the end: `export SPACK_USER_CACHE_PATH="/scratch/user/$USER/spack/cache"`
2. Open a terminal session (on an ACES login node) and run `. $HOME/.bashrc` to apply the change
3. Create folder (ex. "md_env") in home space which will contain the spack environment view
4. Upload files into md_env:
    - slurm_install_md.sh
    - spack.yaml
5. Fill out any fields in slurm_install_md.sh and queue it via `sbatch slurm_install_md.sh`
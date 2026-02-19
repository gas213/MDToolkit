## Spack MD Environment Setup Instructions

1. Edit ~/.bashrc and add the following line to the end: `export SPACK_USER_CACHE_PATH="/scratch/user/$USER/spack/cache"`
2. Open a terminal session (on an ACES login node) and run `. ~/.bashrc` to apply the change
3. Create folder (ex. "md_env") in home space which will contain the spack environment view
4. Upload files into md_env:
    - aces_spack_install.sh
    - spack.yaml
5. Fill out any fields in aces_spack_install.sh and queue it via `sbatch aces_spack_install.sh`
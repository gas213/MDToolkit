## Spack MD Environment Setup Instructions

1. Create folder (ex. "md_env") in your user folder which will contain the spack environment view
2. Upload files into md_env:
    - slurm_install_md.sh
    - spack.yaml
3. Fill out any fields in slurm_install_md.sh and queue it via `sbatch sol_spack_install.sh`
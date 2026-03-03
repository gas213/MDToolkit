## Spack MD Environment Setup Instructions

1. Create folder (ex. "md_env") in your user folder which will contain the spack environment view
2. Upload files into md_env folder:
    - sol_spack_install.sh
    - spack.yaml
3. Fill out any fields in sol_spack_install.sh and queue it via `sbatch sol_spack_install.sh`
    - By default, spack uses 16 build workers, so request 16 CPUs for at least an hour (maybe a few hours just to be extra safe)
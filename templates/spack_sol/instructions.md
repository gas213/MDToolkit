## Spack MD Environment Setup Instructions

1. Create folder (ex. `md_env`) in your user folder which will contain the spack environment view
2. Upload files into `md_env` folder:
    - `sol_spack_install.sh`
    - `spack.yaml`
3. In a terminal pointed at your `md_env` folder, queue the install job via `sbatch sol_spack_install.sh`
    - By default, spack uses 16 build workers, so request 16 CPUs for an hour
4. Once installation is complete, feel free to delete the `spack_safetodelete` folder located at:
    - `/share/ceph/hawk/ebw210_093025/${USER}/spack_safetodelete`

Note: Sol doesn't have modules for most of LAMMPS' dependencies, so making a module-based packages.yaml is not useful on this machine.
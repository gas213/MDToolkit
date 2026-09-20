## Spack MD Environment Setup Instructions

1. Make sure `$PROJECT` is pointed to the current allocation; verify/add this at the end of your `~/.bashrc` file:
    - `export PROJECT="/path/to/project/folder"`
    - example: `export PROJECT="/scratch/group/p.mch260155.000"`
2. Add this to the end of `~/.bashrc` after the PROJECT line: `export SPACK_USER_CACHE_PATH="$PROJECT/spack/cache"`
3. If you modified `~/.bashrc`, either close any existing terminal sessions or enter this command in them: `. ~/.bashrc`
4. At the top of your home space, create `.spack` folder and upload `packages.yaml` into it
5. Elsewhere in home space, create folder (ex. `md_env`) which will contain the spack environment view
6. Upload files into md_env folder:
    - `aces_spack_install.sh`
    - `spack.yaml`
7. In a terminal pointed at your environment folder, queue the install job via `sbatch aces_spack_install.sh`
    - By default, spack uses 16 build workers, so request 16 CPUs for one hour
8. Once installation is complete, feel free to delete the `spack_safetodelete` folder in scratch space
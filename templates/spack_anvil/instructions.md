## Spack MD Environment Setup Instructions

1. Make sure `$PROJECT` is pointed to the current allocation; verify/add this at the end of your `~/.bashrc` file:
    - `export PROJECT="/path/to/project/folder"`
    - example: `export PROJECT="/anvil/projects/x-mch260155"`
2. Add this to the end of `~/.bashrc` after the PROJECT line: `export SPACK_USER_CACHE_PATH="$PROJECT/spack/cache"`
3. If you modified `~/.bashrc`, either close any existing terminal sessions or enter this command in them: `. ~/.bashrc`
4. Create folder (ex. `md_env`) in your home space which will contain the spack environment view
5. Upload files into `md_env` folder:
    - `anvil_spack_install.sh`
    - `spack.yaml`
6. In a terminal pointed at your `md_env` folder, queue the install job via `sbatch anvil_spack_install.sh`
    - By default, spack uses 16 build workers, so request 16 CPUs for one hour
7. Once installation is complete, feel free to delete the `spack_safetodelete` folder in scratch space
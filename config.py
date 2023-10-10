# These are the required packages for Mac
REQUIRED_PACKAGES = [
    # "curl",
    # "libcurl4",
    "git",
    "vim",
    "gfortran",
    # "libopenblas-dev",
    # "liblapack-dev",
    # "openssh-client",
    # "openssh-server",
    # "openmpi-bin",
    # "libopenmpi-dev",
    "open-mpi",
    "python3",
    # "tcl-dev",
    # "tk-dev",
]
HDF5_URL="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz"
HDF5_SRC_DIR = "hdf5-src"
HDF5_DIR="hdf5"
NETCDF_URL="https://github.com/Unidata/netcdf-c/archive/v4.7.4.tar.gz"
NETCDF_SRC_DIR = "netcdf-src"
NETCDF_DIR="netcdf"
SILO_URL="https://wci.llnl.gov/sites/wci/files/2021-01/silo-4.10.2.tgz"
SILO_SRC_DIR = "silo-src"
SILO_DIR = "silo"
PARFLOW_MPIEXEC_EXTRA_FLAGS =  "--mca mpi_yield_when_idle 1 --oversubscribe --allow-run-as-root"
HYPRE_SRC_DIR="hypre-src"
HYPRE_DIR="/hypre"


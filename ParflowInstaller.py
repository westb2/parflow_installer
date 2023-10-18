import os
import json
import config
from utils import *
from SystemPackageManager import SystemPackageManager
import shutil


class ParflowInstaller:

    def __init__(self):
        self.system_package_manager = SystemPackageManager(config.PACKAGE_MANAGER)
        self.package_locations = {}

    def install_parflow(self, use_local_source_code=False):
        create_directory(config.INSTALLATION_ROOT)
        os.chdir(config.INSTALLATION_ROOT)
        self.set_environment_variables()
        if use_local_source_code:
            self.cmake(parflow_source=config.LOCAL_PARFLOW_SRC)
        else:
            self.download_parflow_source()
            self.cmake(parflow_source=f"{config.INSTALLATION_ROOT}/{config.PARFLOW_SRC_DIR}")
        self.install_pftools()
        self.write_env_file()
        print("INSTALLATION COMPLETE!\n")
        print("Please add the following lines to your bashrc (or other profile) file\n\n")
        print(f'export PATH="{config.INSTALLATION_ROOT}/{config.PARFLOW_INSTALLATION_DIR}/bin:$PATH"\n')
        print(f'export PARFLOW_DIR="{config.INSTALLATION_ROOT}/{config.PARFLOW_INSTALLATION_DIR}"\n\n')
        print("You can also find this information where you installed parflow if you need to find it later")


    def write_env_file(self):
        with open("add_me_to_your_bashrc.txt", "w") as file:
            file.write(f'export PATH="{config.INSTALLATION_ROOT}/{config.PARFLOW_INSTALLATION_DIR}/bin:$PATH"\n')
            file.write(f'export PARFLOW_DIR="{config.INSTALLATION_ROOT}/{config.PARFLOW_INSTALLATION_DIR}"')

    def download_parflow_source(self):
        os.system(f"git clone -b master --single-branch {config.PARFLOW_URL} {config.PARFLOW_SRC_DIR}")
    

    def install_pftools(self):
        run_and_capture_terminal_output(
            f"python3 -m pip install \
            {config.INSTALLATION_ROOT}/{config.PARFLOW_BUILD_DIR}/pftools/python"
        )

    def cmake(self, parflow_source):
        curl_location = shutil.which("curl")
        create_directory(config.PARFLOW_SRC_DIR)
        os.system(
            f"cmake -S {parflow_source}\
            -B {config.INSTALLATION_ROOT}/{config.PARFLOW_BUILD_DIR}\
            -D CMAKE_BUILD_TYPE=Release\
            -D PARFLOW_ENABLE_HDF5=TRUE\
            -D HDF5_ROOT={config.INSTALLATION_ROOT}/{config.HDF5_DIR}\
            -D PARFLOW_ENABLE_HYPRE=TRUE\
            -D HYPRE_ROOT={config.INSTALLATION_ROOT}/{config.HYPRE_DIR}\
            -D PARFLOW_HAVE_CLM=TRUE\
            -D PARFLOW_ENABLE_PYTHON=TRUE\
            -D PARFLOW_ENABLE_TIMING=TRUE\
            -D PARFLOW_ENABLE_PROFILING=TRUE\
            -D PARFLOW_AMPS_LAYER=mpi1\
            -D PARFLOW_AMPS_SEQUENTIAL_IO=TRUE\
            -D CURL_LIBRARY={curl_location}\
            -D CMAKE_BUILD_TYPE=Debug\
            -D PARFLOW_ENABLE_SILO=/Users/ben/parflow_build/silo\
            -D SILO_ROOT={config.INSTALLATION_ROOT}/{config.SILO_DIR}\
            -D PARFLOW_ENABLE_NETCDF=TRUE\
            -D NETCDF_DIR={config.INSTALLATION_ROOT}/{config.NETCDF_DIR} \
            -DCMAKE_POLICY_DEFAULT_CMP0144=NEW \
            && cmake --build {config.INSTALLATION_ROOT}/{config.PARFLOW_BUILD_DIR}\
            && cmake --install {config.INSTALLATION_ROOT}/{config.PARFLOW_BUILD_DIR} --prefix {config.INSTALLATION_ROOT}/{config.PARFLOW_INSTALLATION_DIR}\
            "
        )
        # -D PARFLOW_PYTHON_VIRTUAL_ENV=TRUE\


    def set_environment_variables(self):
        for (name, value) in config.CMAKE_ENVIRONMENT_VARIABLES.items():
            os.environ[name] = value


    def install_requirements(self):
        create_directory(config.INSTALLATION_ROOT)
        os.chdir(config.INSTALLATION_ROOT)
        # first install everything we can via our system package manager
        for package in config.REQUIRED_PACKAGES:
            self.system_package_manager.install_package(package)
            self.package_locations[package] = self.system_package_manager.get_package_location(package)
        # next install the packages we need to build and configure from source.
        # The order of these matters!
        self.install_hdf5()
        self.install_netcdf()
        self.install_silo()
        self.install_hypre()
        os.chdir(config.INSTALLATION_ROOT)
        self.save_package_locations()

    def install_hypre(self):
        os.chdir(config.INSTALLATION_ROOT)
        create_directory(config.HYPRE_SRC_DIR)
        os.chdir(config.HYPRE_SRC_DIR)
        os.system(f"git clone {config.HYPRE_URL} --single-branch")
        os.chdir("hypre/src")
        os.system(f"./configure --prefix={config.INSTALLATION_ROOT}/{config.HYPRE_DIR} CC=mpicc && make && make install")
        self.package_locations["hypre"] = config.INSTALLATION_ROOT + "/" + config.HYPRE_DIR


    def install_hdf5(self):
        os.chdir(config.INSTALLATION_ROOT)
        create_directory(config.HDF5_SRC_DIR)
        os.chdir(config.HDF5_SRC_DIR)
        os.system(f"curl -L {config.HDF5_URL} | tar --strip-components=1 -xzv && \
                    CC=mpicc ./configure \
                    --prefix={config.INSTALLATION_ROOT}/{config.HDF5_DIR} \
                    --enable-parallel && \
                    make && make install"
                  )
        self.package_locations["hdf5"] = config.INSTALLATION_ROOT + config.HDF5_DIR


    def install_netcdf(self):
        os.chdir(config.INSTALLATION_ROOT)
        create_directory(config.NETCDF_SRC_DIR)
        os.chdir(config.NETCDF_SRC_DIR)
        os.system(f"curl -L {config.NETCDF_URL} | tar --strip-components=1 -xzv && \
                    CC=mpicc CPPFLAGS=-I{config.HDF5_DIR}/include LDFLAGS=-L{config.HDF5_DIR}/lib \
                    ./configure --disable-shared --disable-dap --prefix=${config.NETCDF_DIR} && \
                    make && make install"
                  )
        self.package_locations["netcdf"] = config.INSTALLATION_ROOT + config.NETCDF_DIR

    
    def install_silo(self):
        os.chdir(config.INSTALLATION_ROOT)
        create_directory(config.SILO_DIR)
        os.chdir(config.SILO_DIR)
        os.system(f"curl -L {config.SILO_URL} | tar --strip-components=1 -xzv && \
                    ./configure  --prefix={config.SILO_DIR} --disable-silex --disable-hzip --disable-fpzip && \
                    make && make install"
                  )
        self.package_locations["silo"] = config.INSTALLATION_ROOT + config.SILO_DIR


    def save_package_locations(self):
        with open("package_locations.json", "w") as file:
            json.dump(self.package_locations, file)





import os
from config import *
from utils import *


class ParflowInstaller:

    def __init__(self, package_manager, installation_directory):
        self.package_manager = package_manager
        if package_manager == "brew":
            self.package_manager_automatic_yes_string = ""
        self.installation_directory = installation_directory
        self.package_locations = {}

    def install_parflow(self):
        original_directory = os.getcwd()
        create_directory(self.installation_directory)
        os.chdir(self.installation_directory)
        self.install_requirements()
        os.chdir(original_directory)
        self.save_package_locations()

    def install_requirements(self):
        # first install everything we can via our system package manager
        for package in REQUIRED_PACKAGES:
            self.install_package(package)
            self.package_locations[package] = self.get_package_location(package)
        # next install the packages we need to build and configure from source.
        # The order of these matters!
        self.install_hdf5()
        self.install_netcdf()
        self.install_silo()
        self.install_hypre()

    def install_hypre(self):
        os.chdir(self.installation_directory)
        create_directory(HYPRE_SRC_DIR)
        os.chdir(HYPRE_SRC_DIR)
        os.system(f"git clone https://github.com/hypre-space/hypre.git --single-branch")
        os.chdir("hypre/src")
        os.system(f"make && make install && ./configure --prefix={self.installation_directory}/{HYPRE_DIR} CC=mpicc")
        self.package_locations["hypre"] = self.installation_directory + "/" + HYPRE_DIR


    def install_hdf5(self):
        os.chdir(self.installation_directory)
        create_directory(HDF5_SRC_DIR)
        os.chdir(HDF5_SRC_DIR)
        os.system(f"curl -L {HDF5_URL} | tar --strip-components=1 -xzv && \
                    CC=mpicc ./configure \
                    --prefix={self.installation_directory}/{HDF5_DIR} \
                    --enable-parallel && \
                    make && make install"
                  )
        self.package_locations["hdf5"] = self.installation_directory + HDF5_DIR


    def install_netcdf(self):
        os.chdir(self.installation_directory)
        create_directory(NETCDF_SRC_DIR)
        os.chdir(NETCDF_SRC_DIR)
        os.system(f"curl -L {NETCDF_URL} | tar --strip-components=1 -xzv && \
                    CC=mpicc CPPFLAGS=-I{NETCDF_DIR}/include LDFLAGS=-L{NETCDF_DIR}/lib \
                    ./configure --disable-shared --disable-dap --prefix=${NETCDF_DIR} && \
                    make && make install"
                  )
        self.package_locations["netcdf"] = self.installation_directory + NETCDF_DIR

    
    def install_silo(self):
        os.chdir(self.installation_directory)
        create_directory(HDF5_DIR)
        os.chdir(HDF5_DIR)
        os.system(f"curl -L {SILO_URL} | tar --strip-components=1 -xzv && \
                    ./configure  --prefix={SILO_DIR} --disable-silex --disable-hzip --disable-fpzip && \
                    make && make install"
                  )
        self.package_locations["silo"] = self.installation_directory + SILO_DIR


    def get_homebrew_package_location(self, package):
        return self.capture_command_output(f"brew --prefix {package}")


    def get_package_location(self, package, package_manager="homebrew"):
        if package_manager=="homebrew":
   
            return self.get_homebrew_package_location(package)

    def install_package(self, package):
        if self.package_manager == "brew":
            self.brew_install_package(package)


    def brew_install_package(self, package):
        os.system(
            f'''
            {self.package_manager} update && \
            {self.package_manager} install {self.package_manager_automatic_yes_string} \
            {package}
            '''
        )


    def save_package_locations(self):
        with open("package_locations.txt", "w") as file:
            file.write(
                f'''
                NETCDF_FULL_PATH="{self.package_locations["netcdf"]}"\
                HYPRE_FULL_PATH="{self.package_locations["hypre"]}"\
                HDF5_FULL_PATH="{self.package_locations["hdf5"]}"\
                SILO_FULL_PATH="{self.package_locations["silo"]}"\
                '''
                )





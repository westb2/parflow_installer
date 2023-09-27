import os
import subprocess
import shutil

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class ParflowInstaller:

    def __init__(self, package_manager, installation_directory):
        self.package_manager = package_manager
        if package_manager == "brew":
            self.package_manager_automatic_yes_string = ""
        self.installation_directory = installation_directory
        self.package_dirs = {}

    def install(self):
        original_directory = os.getcwd()
        create_directory(self.installation_directory)
        os.chdir(self.installation_directory)
        self.install_requirements()
        os.chdir(original_directory)
        self.generate_addition_to_bashrc()

    def install_requirements(self):
        packages = ["open-mpi", "hypre", "netcdf", "hdf5", "netcdf-cxx"]
        for package in packages:
            self.install_package(package)
            self.package_dirs[package] = self.get_package_location(package)


    def brew_install_packages(self):
        os.system(
            f'''{self.package_manager} update && \
            {self.package_manager} install {self.package_manager_automatic_yes_string} tzdata && \
            dpkg-reconfigure --frontend noninteractive tzdata && \
            {self.package_manager} install {self.package_manager_automatic_yes_string} \
            build-essential \
            curl \
            libcurl4 \
            git \
            vim \
            gfortran \
            libopenblas-dev \
            liblapack-dev \
            openssh-client \
            openssh-server \
            openmpi-bin \
            libopenmpi-dev \
            python3 \
            python3-pip \
            python3-venv \
            tcl-dev \
            tk-dev
            '''
        )

    def capture_command_output(self, command):
        tmp_file_location = "very_temporary_file"
        os.system(f"{command} > {tmp_file_location}")
        output = ""
        with open(tmp_file_location, "r") as file:
            output = file.read()
        os.remove("very_temporary_file")
        return output

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

    def generate_addition_to_bashrc(self):
        with open("add_me_to_your_user_profile.txt", "w") as file:
            file.write(
                f'export HYPRE_DIR="{self.package_dirs["hypre"]}"\
                export NETCDF_DIR="{self.package_dirs["netcdf-cxx"]}"\
                export HDF5_DIR="{self.package_dirs["hdf5"]}"\
                '
                )

    def cmake_options():
        '''
        -D CMAKE_BUILD_TYPE=Release   \
        -D HDF5_ROOT=$HDF5_DIR         \
        -D PARFLOW_ENABLE_HDF5=TRUE     \
        -D HYPRE_ROOT=$HYPRE_DIR         \
        -D PARFLOW_ENABLE_HYPRE=TRUE      \
        -D PARFLOW_HAVE_CLM=TRUE             \
        -D PARFLOW_ENABLE_PYTHON=TRUE         \
        -D PARFLOW_ENABLE_TIMING=TRUE          \
        -D PARFLOW_ENABLE_PROFILING=TRUE          \
        -D PARFLOW_AMPS_LAYER=mpi1              \
        -D PARFLOW_AMPS_SEQUENTIAL_IO=TRUE       \
        -D PARFLOW_ENABLE_NETCDF=TRUE             \
        -D NETCDF_DIR=$NETCDF_DIR                  \
        -D CURL_LIBRARY=/usr/bin/curl
        '''


def main():
    
    PACKAGE_MANAGER = "brew"
    package_manager_automatic_yes_string = ""
    USER_HOME_DIRECTORY = "Users/ben"
    INSTALLATION_DIRECTORY = USER_HOME_DIRECTORY + "/parflow_dependencies"
    parflow_installer = ParflowInstaller(package_manager=PACKAGE_MANAGER, installation_directory=INSTALLATION_DIRECTORY)
    parflow_installer.install()
    # generate_addition_to_bashrc(HYPRE_DIR, NETCDF_DIR, H)
   



if __name__ == "__main__":
    main()
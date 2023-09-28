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
        self.package_locations = {}

    def install_parflow(self):
        original_directory = os.getcwd()
        create_directory(self.installation_directory)
        os.chdir(self.installation_directory)
        self.install_requirements()
        os.chdir(original_directory)
        self.generate_addition_to_bashrc()

    def install_requirements(self):
        packages = ["open-mpi", "netcdf", "hdf5", "netcdf-cxx"]
        for package in packages:
            self.install_package(package)
            self.package_locations[package] = self.get_package_location(package)
        self.install_hypre()

    def install_hypre(self):
        HYPRE_DIR="hypre-src"
        os.chdir(self.installation_directory)
        create_directory(HYPRE_DIR)
        os.chdir(HYPRE_DIR)
        # os.system(f"git clone https://github.com/hypre-space/hypre.git --single-branch")
        os.chdir("hypre/src")
        os.system(f"make && make install && ./configure --prefix={self.installation_directory}/{HYPRE_DIR} CC=mpicc")
        self.package_locations["hypre"] = self.installation_directory + "/" + HYPRE_DIR

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


    def install_hdf5(self):
        HDF5_URL="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz"
        HDF5_DIR="hdf5-src"
        os.chdir(self.installation_directory)
        create_directory(HDF5_DIR)
        os.chdir(HDF5_DIR)
        os.system(f"curl -L {HDF5_URL} | tar --strip-components=1 -xzv && \
                    CC=mpicc ./configure \
                    --prefix={self.installation_directory}/{HDF5_DIR} \
                    --enable-parallel && \
                    make && make install"
                  )
        self.package_locations["hdf5"] = self.installation_directory + "/hdf5"

    def generate_addition_to_bashrc(self):
        with open("add_me_to_your_user_profile.txt", "w") as file:
            file.write(
                f'''
                export NETCDF_DIR="{self.package_locations["netcdf-cxx"]}"\
                export HYPRE_DIR="{self.package_locations["hypre"]}"\
                export HDF5_DIR="{self.package_locations["hdf5"]}"\
                '''
                )

    # def detect_package_manager(self):
    #     package_managers=["brew", "apt-get", "yum"]
    #     for package_manager in package_managers



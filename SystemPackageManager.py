import os
from utils import *


class SystemPackageManager:
    def __init__(self, package_manager):
        if package_manager == "AUTO_CONFIGURED":
            # make this instantiate a HomebrewManager child class
            self.package_manager = "brew"
            self.automatic_yes_flag = ""


    def get_homebrew_package_location(self, package):
        return run_and_capture_terminal_output(f"brew --prefix {package}")


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
            {self.package_manager} install {self.automatic_yes_flag} \
            {package}
            '''
        )
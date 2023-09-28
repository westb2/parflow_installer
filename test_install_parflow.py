from install_parflow import ParflowInstaller

# block one 
PACKAGE_MANAGER = "brew"
package_manager_automatic_yes_string = ""
USER_HOME_DIRECTORY = "Users/ben"
INSTALLATION_DIRECTORY = USER_HOME_DIRECTORY + "/parflow_dependencies"
parflow_installer = ParflowInstaller(package_manager=PACKAGE_MANAGER, installation_directory=INSTALLATION_DIRECTORY)
parflow_installer.install_parflow()

#block 2
print("HI\n")

#block 3
print("bye\n")
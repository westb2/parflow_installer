from ParflowInstaller import ParflowInstaller

# block one. Reminder to show go to definition, find references
PACKAGE_MANAGER = "brew"
USER_HOME_DIRECTORY = "Users/ben"
INSTALLATION_DIRECTORY = USER_HOME_DIRECTORY + "/parflow_dependencies"
parflow_installer = ParflowInstaller(package_manager=PACKAGE_MANAGER, installation_directory=INSTALLATION_DIRECTORY)
parflow_installer.install_parflow()

#block 2
print("HI\n")

#block 3
print("bye\n")
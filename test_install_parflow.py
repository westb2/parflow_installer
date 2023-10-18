from ParflowInstaller import ParflowInstaller

# block one. Reminder to show go to definition, find references
PACKAGE_MANAGER = "brew"
USER_HOME_DIRECTORY = "/Users/ben"
INSTALLATION_DIRECTORY = USER_HOME_DIRECTORY + "/parflow_build"

parflow_installer = ParflowInstaller()

# parflow_installer.install_requirements()
parflow_installer.install_parflow(use_local_source_code=True)

#block 3
print("bye\n")
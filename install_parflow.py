from ParflowInstaller import ParflowInstaller

# block one. Reminder to show go to definition, find references
parflow_installer = ParflowInstaller()

# parflow_installer.install_requirements()
parflow_installer.install_parflow(use_local_source_code=True, install_pftools=False)

import os

def run_and_capture_terminal_output(command):
    tmp_file_location = "very_temporary_file"
    os.system(f"{command} > {tmp_file_location}")
    output = ""
    with open(tmp_file_location, "r") as file:
        output = file.read()
    os.remove("very_temporary_file")
    return output


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

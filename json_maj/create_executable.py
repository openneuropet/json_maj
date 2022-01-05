#! /usr/bin/env python3
import pathlib
import subprocess
import os
import platform
import toml
import shutil


# collect the path to this script
this_scripts_path = pathlib.Path(__file__)

# the build path for any executable created via pyinstaller should be in ../build/
build_folder = os.path.join(this_scripts_path.parent.parent, 'build')
project_folder = this_scripts_path.parent.parent

# check if pyinstaller is installed
check_for_pyinstaller = subprocess.run("pyinstaller --help", shell=True, stdout=subprocess.DEVNULL)

# get architecture and platform
platform_and_arch = platform.platform()

# collect version of software
project_toml = toml.load(f"{this_scripts_path.parent.parent}/pyproject.toml")
version = project_toml['tool']['poetry']['version']
executable_name = f"jsonmaj-{version}_{platform_and_arch}"

if check_for_pyinstaller.returncode == 0:
    command = f"pyinstaller cli.py -F -n {executable_name} --specpath {build_folder}"
    create_executable = subprocess.run(command, shell=True)
else:
    raise Exception("Pyinstaller is not installed.")

print("done")

if create_executable.returncode == 0:
    for folder in ['build', 'dist']:
        shutil.copytree(folder, build_folder, symlinks=False, ignore=None, ignore_dangling_symlinks=False,
                        dirs_exist_ok=True)

        # remove files b/c why not
        shutil.rmtree(folder)

    # lastly place the binary in the binary folder
    try:
        # shutil is garbage
        shutil.move(os.path.join(build_folder, executable_name, executable_name), os.path.join(project_folder, 'executable'))
    except shutil.Error:
        os.remove(os.path.join(project_folder, 'executable', executable_name))
        shutil.move(os.path.join(build_folder, executable_name, executable_name),
                    os.path.join(project_folder, 'executable'))
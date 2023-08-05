import os
import sys

from setuptools import find_packages, setup

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + "/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="titan-iris",
    version="0.1",
    install_requires=install_requires,
    entry_points={"console_scripts": ["iris = iris.main:main"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
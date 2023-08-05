import os
from distutils.command.install import install

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = ""


class custom_install(install):
    def run(self):
        install.run(self)


cur_directory_path = os.path.abspath(os.path.dirname(__file__))

setup(
    name="grebble-rpa",
    version="0.0.1",
    packages=find_packages(exclude=("tests", "executor")),
    description="Grebble rpa desktop",
    long_description=README,
    author="Grebble",
    author_email="info@grebble.io",
    url="https://github.com/Grebble-team/rpa",
    install_requires=[
        "grebble-flow==0.0.3.50",
        "rpaframework",
        "robotframework-browser",
        "rpaframework-dialogs",
        "rpaframework-windows",
    ],
    include_package_data=True,
    cmdclass={"install": custom_install},
)

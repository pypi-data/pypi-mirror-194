"""Set up ECHO library"""

from setuptools import setup, find_packages
from setuptools.command.install import install as DistutilsInstall
from os import system

with open("ECHO/README.org", "r") as ldf:
    long_description = ldf.read()

class EFP_Install(DistutilsInstall):
    def run(self):
        system('cd ECHO/engines/mae_epddl_planning/sofai/Planners/EFP; make; cd -')
        DistutilsInstall.run(self)

setup(
    name='echosys',
    version='0.2.0',
    description='A python library for modeling and solving epistemic multi agents planning problems',
    #long_description = long_description,
    #long_description_content_type = '',
    url='https://github.com/DavideSolda/echosys',
    author='Davide Solda\'',
    author_email='davide.solda@tuwien.ac.at',
    license='GNU General Public License v3.0',
    packages=find_packages(),
    install_requires=['clingo'],
    classifiers=[],
    cmdclass={'install': EFP_Install},
    #include_package_data = True,
    data_files=[('../../ECHO/engines/mae_epddl_planning/sofai/Planners/EFP/bin',
                 ['ECHO/engines/mae_epddl_planning/sofai/Planners/EFP/bin/efp.out'])]
    )

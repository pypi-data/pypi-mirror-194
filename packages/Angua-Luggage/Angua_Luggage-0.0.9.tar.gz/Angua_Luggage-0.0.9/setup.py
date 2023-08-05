# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:19:59 2023

@author: mwodring
"""

from setuptools import setup, find_packages

VERSION = '0.0.9' 
DESCRIPTION = 'Additional commands for Angua and other Bioinformatic tools.'
LONG_DESCRIPTION = 'Additional commands for Angua and other Bioinformatic tools.'

# Setting up
setup(
        package_data={'data': ['/data/*']},
	#scripts = ["bin/rma", "bin/fetchSRA", "bin/getORFs", "bin/ICTVEntrez", "bin/TextSearch"],
        include_package_data=True,
        name="Angua_Luggage", 
        version=VERSION,
        author="Morgan Wodring",
        author_email="morgan.wodring@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["Bio", "rpy2", "pyyaml"],
        #Note: Make a requirements file for the Angua env after all is said and done.
        keywords=['bioinformatics', 'angua'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
        ]
)
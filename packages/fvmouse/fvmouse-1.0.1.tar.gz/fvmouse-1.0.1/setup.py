#################################################################################
# Copyright (C) 2023
# Juan Carlos Perez Castellanos <cuyopc@gmail.com>
# Maria Frine de la Rosa Gutierrez <frinedlr@gmail.com>
#
# This file is part of fvmouse.
#
# fvmouse can not be copied and/or distributed without the express
# permission of Juan Carlos Perez Castellanos or Maria Frine de la Rosa Gutierrez
##################################################################################

# !/usr/bin/env python3
from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
# Build the production package
prod_pkgs = find_packages(exclude=["venv", "virtualenv"])

setup(
    name='fvmouse',
    version='1.0.1',
    description='Face and voice recognition system to control the cursor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=prod_pkgs,
    data_files=[('detection/data',
                 ['detection/data/shape_predictor_68_face_landmarks.dat',
                  'detection/data/optimized_model.eim'])],
    license='Proprietary',
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': ['fvmouse=detection.full_detection:main']
    }
)

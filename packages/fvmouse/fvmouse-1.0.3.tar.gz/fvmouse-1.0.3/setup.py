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
    version='1.0.3',
    description='Face and voice recognition system to control the cursor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=prod_pkgs,
    data_files=[('detection/data',
                 ['detection/data/shape_predictor_68_face_landmarks.dat',
                  'detection/data/optimized_model.eim'])],
    install_requires=[
        'dlib~=19.24.0',
        'edge_impulse_linux~=1.0.7',
        'numpy~=1.23.2',
        'opencv_python~=4.5.5.64',
        'PyAutoGUI~=0.9.53',
        'pynput~=1.7.6',
        'PySimpleGUI~=4.60.4',
        'pyaudio~=0.2.13'
    ],
    license='Proprietary',
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': ['fvmouse=detection.full_detection:main']
    }
)

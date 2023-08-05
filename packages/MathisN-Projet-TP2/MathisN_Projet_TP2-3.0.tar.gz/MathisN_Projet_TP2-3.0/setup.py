# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:54:43 2023

@author: mathi
"""

from setuptools import setup

setup(
    name='MathisN_Projet_TP2',
    version='3.0',
    packages=["Package_Robot"],
    install_requires=[
        
    ],
    include_package_data=True,
    author='Mathis',
    author_email='mathis.nenach@cpe.fr',
    description='Crée une grille où pourra se deplacer un robot',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
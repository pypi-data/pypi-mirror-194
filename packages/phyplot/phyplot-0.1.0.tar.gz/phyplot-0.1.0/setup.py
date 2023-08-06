'''
Phyplot is a python plotting package for use with the Sci-Phy package(statistical analysis and modelling of 
evolved data using evolutionary trees).
'''

from setuptools import setup, find_packages

setup(
    name='phyplot',
    version='0.1.0',
    author='Chris Organ & Andrew Meade',
    url='https://github.com/ChrisOrgan/phyplot',
    license='GNU General Public License v3.0',
    description='PhyloGrpah is a python package for plotting evolutionary trees and data.',
    keywords = ['plotting', 'graphs', 'evolution', 'phylogenetics', 'phylodynamics', 'comparative methods'],
    long_description=open('README.md').read(),
    install_requires=[
        'pandas>=1.2.3',
        'scipy>=1.6.3',
        'numpy>=1.20.3',
        'ply>=3.11'
        ],
    python_requires='>=3.7',
    packages=find_packages(),
    package_data={'': ['LICENSE', 'README.md', 'setup.py']},
    include_package_data=True
    )
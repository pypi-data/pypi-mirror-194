from setuptools import setup, find_packages
import sys

setup(
    name='stoichiometric_balancer',
    version='1.0.2',
    description='Python package for balancing and visualising reactions',
    url='https://github.com/EVBiotechBV/simple_chemtools/tree/master',
    author='Sivasudhan Rathnachalam',
    author_email='s.rathnachalam@evbio.tech',
    license='BSD 2-clause',
    packages=find_packages(include=['stoi_balancer', 'examples.ipynb', 'test.py','README.md']),
    install_requires=['chempy >= 0.7.6',
                      'equilibrator-api >=0.4.7',
                      'rdkit >=2022.09.4',
                      'pubchempy>=1.0.4',
                      'jupyterlab'
    ],


    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
       'Programming Language :: Python :: 3.6',
       'Programming Language :: Python :: 3.7',
       'Programming Language :: Python :: 3.8',
       'Programming Language :: Python :: 3.9',
    ],
)


from setuptools import find_packages, setup






setup(
    name='geodesicDome',
    packages=find_packages(include=['geodesicDome']),
    version='0.6.0',
    long_description="""
    Module geodesic_dome
====================

About
-------
The purpose of this library is to assist in storing the vertices in a geodesic dome,
and contain methods to allow neighbourhood searches and tessellation of the vertices
to be performed efficiently.

The library provides:
* Tessellation for a geodesic dome surface
* Provide index based storage and neighbouring search algorithm
* Provide functionality for uneven surface tessellation

Installation
-------
To install our library run this command in your terminal:
pip install geodesicDome
    """,
    long_description_content_type="text/markdown",
    install_requires=["numpy", "numba"],
    description='Geodesic Dome',
    author='Sam, Lewis, James, Kevin, Jacob, Manan',
    license='MIT',
    
   
)
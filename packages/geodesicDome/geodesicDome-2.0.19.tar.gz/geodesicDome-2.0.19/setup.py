from setuptools import find_packages, setup
import os

f = open("../docs/geodesic_dome.md", "r")
long_descr = f.read()

setup(
    name='geodesicDome',
    packages=find_packages(include=['geodesicDome']),
    version='2.0.19',
    long_description=long_descr,
    long_description_content_type="text/markdown",
    install_requires=["numpy", "numba"],
    description='Geodesic Dome',
    author='Sam, Lewis, James, Kevin, Jacob, Manan',
    license='MIT',
    
   
)
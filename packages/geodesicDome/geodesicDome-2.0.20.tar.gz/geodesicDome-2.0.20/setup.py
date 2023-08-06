from setuptools import find_packages, setup
import os


with open("../docs/geodesic_dome.md") as f:
    long_description = f.read()

setup(
    name='geodesicDome',
    packages=find_packages(include=['geodesicDome']),
    version='2.0.20',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["numpy", "numba"],
    description='Geodesic Dome',
    author='Sam, Lewis, James, Kevin, Jacob, Manan',
    license='MIT',
    
   
)
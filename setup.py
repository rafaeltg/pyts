from setuptools import setup, find_packages
import pyts

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pyts',
    version=pyts.__version__,
    description='Time Series functions',
    author='Rafael Gonzalez',
    author_email='rthomazigonzalez@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=required
)

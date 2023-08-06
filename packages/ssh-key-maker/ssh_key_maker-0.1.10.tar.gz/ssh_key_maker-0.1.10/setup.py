# __Author__ = "Pranav Chandran"
# __Date__ = 28-02-2023
# __Time__ = 13:23
# __FileName__ = setup.py
from setuptools import setup, find_packages

setup(
    name='ssh_key_maker',
    version='0.1.10', #updated version
    author='Pranav Chandran',
    author_email='pranav.chandran@gmail.com',
    description='A package to generate ssh keys',
    long_description=open('README.md').read(),
    packages=find_packages(),
    url='',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

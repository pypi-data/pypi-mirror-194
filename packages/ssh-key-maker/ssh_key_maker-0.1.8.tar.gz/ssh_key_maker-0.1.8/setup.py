# __Author__ = "Pranav Chandran"
# __Date__ = 28-02-2023
# __Time__ = 13:23
# __FileName__ = setup.py
from setuptools import setup

setup(
    name='ssh_key_maker',
    version='0.1.8', #updated version
    author='Pranav Chandran',
    author_email='pranav.chandran@gmail.com',
    description='Package to generate SSH keys for windows users.',
    packages=['ssh_key_maker'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

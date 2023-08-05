from setuptools import setup

setup(
    name='diskloaf',
    version='0.2.0',
    description='A tool for creating a large file (a loaf) in order to wipe a hard disk '
                'written by someone who knows nothing about security',
    author='Andrew Blomenberg',
    author_email='andrewBlomen@gmail.com',
    url='https://github.com/Yook74/diskloaf',

    install_requires=['progressbar2'],
    entry_points={
        'console_scripts': ['diskloaf = loaf:main'],
    }
)
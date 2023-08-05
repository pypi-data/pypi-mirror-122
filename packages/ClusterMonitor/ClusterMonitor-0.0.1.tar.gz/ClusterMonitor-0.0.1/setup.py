from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Simple script which can be used to monitor and log CPU and RAM usage of submitted cluster jobs'

# Setting up
setup(
    name="ClusterMonitor",
    version=VERSION,
    author="nickhir",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['matplotlib'],
    keywords=['python', 'cluster', 'monitor', 'CPU', 'RAM', 'usage', 'SLURM'],
    classifiers=[
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

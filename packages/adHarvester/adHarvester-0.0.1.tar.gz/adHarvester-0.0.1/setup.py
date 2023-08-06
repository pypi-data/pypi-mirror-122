from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="adHarvester",
    version='0.0.1',
    author="Suren ABrahamyan",
    author_email="suren.abrahamyan89@gmail.com",
    description='Harvester for any type of online shops and advertisements',
    long_description='Harvester for any type of online shops and advertisements',
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
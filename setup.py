from setuptools import setup, find_packages

setup(
    name="StateSpaceGrid",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "networkx",
        "numpy",
        "pandas",
        "pytest",
    ],
)

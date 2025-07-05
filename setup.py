from setuptools import setup, find_packages

setup(
    name="StateSpaceGridLib",
    version="0.0.1",
    packages=find_packages(),
    description="2D state space grid diagrams and measures for dynamic systems",
    install_requires=[
        "matplotlib"
    ],
)
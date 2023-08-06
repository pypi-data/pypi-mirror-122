import pathlib
from setuptools import setup, find_packages
# The directory containing this file
HERE = pathlib.Path('D:\School\Fall 2021\Econ\VWAP_code\setup.py').parent
# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
    name="VWAP",
    version="1.0.3",
    description="Buy and Sell signals using VWAP-based trading algorithm",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourgithubname/yourpackagename",
    author="Saad Lahrichi",
    author_email="sl636@duke.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    # dependencies for installing the package
    install_requires=["numpy", "pandas", "matplotlib", "alpha_vantage"]
)

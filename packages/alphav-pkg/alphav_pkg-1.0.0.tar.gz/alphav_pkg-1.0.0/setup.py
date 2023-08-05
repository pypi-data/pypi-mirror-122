import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="alphav_pkg",
    version="1.0.0",
    description="Client for consuming Alpha Vantage API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathan-mothe/alphav_client",
    author="Jonathan Mothé",
    author_email="jonathan.mothe@gmail.com",
    packages=["stock_time_series", "core"],
    install_requires=["requests", "python-decouple"],
)

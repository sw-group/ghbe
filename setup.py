# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="Mining GitHub",
    author_email="sw.project.mining@gmail.com",
    url="",
    keywords=["Swagger", "Mining GitHub"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    This Swagger API provides endpoints for retrieving detailed information about issues, workflows, and repository metadata. It allows users to access various aspects of a repository&#x27;s management, including issue tracking, workflow management, and general repository information.   Some useful links: - [The GitHub project repository](https://github.com/sw-group/ghbe) - [The source API definition](*Mettere url openAPI)
    """
)

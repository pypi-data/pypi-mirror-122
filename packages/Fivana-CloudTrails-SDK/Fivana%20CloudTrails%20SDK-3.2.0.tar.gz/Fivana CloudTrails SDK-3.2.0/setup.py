import os

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


VERSION = os.environ.get("TAG_VERSION")
VERSION = VERSION[1:] if VERSION else "3.2.0"
#VERSION = "3.0.0"

print(VERSION)

setuptools.setup(
    name="Fivana CloudTrails SDK",
    version=VERSION,
    author="Reynier Lester Claro Escalona, Ernesto Herrera",
    author_email="rclaro@fivana.com, eherrera@fivana.com",
    description="SDK for CloudTrails DevOps management FIVANA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/factorclick/fc-cloudtrails-sdk-py",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)

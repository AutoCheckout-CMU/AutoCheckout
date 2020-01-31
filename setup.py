from setuptools import find_packages, setup

setup(
    name="cpsdriver",
    version="1.0.0",
    license="AiFi (C) All rights reserved",
    long_description=__doc__,
    packages=find_packages(".", exclude=["test", "test.*"]),
    install_requires=["pymongo", "requests", "numpy"],
)

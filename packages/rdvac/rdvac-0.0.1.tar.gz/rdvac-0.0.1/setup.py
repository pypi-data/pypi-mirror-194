from setuptools import setup
from distutils.core import setup
setup(
    name="rdvac",
    version="0.0.1",
    description="An Uber Rides Clustering",
    author="Lagisetty Ravikiran",
    author_email="kiranlravi8@gmail.com",
    py_modules=["rdvac"],
    package_dir={"":"src"},
    include_package_data=True,
    )

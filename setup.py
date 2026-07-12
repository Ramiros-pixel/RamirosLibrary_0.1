from setuptools import setup, find_packages

setup(
    name="ramiros_vision",
    version="0.1",
    packages=find_packages(),
    include_package_data= True,
    package_data= {'ramiros_vision': ['*.dll', '*.so']},
)
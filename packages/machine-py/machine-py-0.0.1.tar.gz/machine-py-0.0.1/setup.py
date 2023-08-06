# python setup.py sdist bdist_wheel

from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
	long_description = fh.read()

setup(
	name="machine-py",
	version="0.0.1",

	author="Prashant Lawhatre & Pranay Lawhatre",
	author_email="prashantlawhatre@gmail.com",
	
	description="A package for machine learning",
	long_description=long_description,
	long_description_content_type="text/markdown",

	package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
	install_requires=['numpy', 'sympy', 'matplotlib']
	)

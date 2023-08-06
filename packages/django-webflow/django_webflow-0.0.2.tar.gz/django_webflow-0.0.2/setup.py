from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django_webflow',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    long_description=long_description,
)

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='pyjowi',
    version='0.1.0',
    description='A Python SDK for the Jowi API',
    author='Mumtoz Valijonov',
    author_email='mumtoz.valijonov@gmail.com',
    packages=find_packages(),
    install_requires=required,
)

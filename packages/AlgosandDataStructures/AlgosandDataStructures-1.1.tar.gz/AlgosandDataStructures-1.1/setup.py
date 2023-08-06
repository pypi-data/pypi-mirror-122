from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='AlgosandDataStructures',
    version='1.1',
    url='https://github.com/joaogabrielferr/AlgosandDataStructures',
    license='MIT License',
    author='Joao Gabriel Ferreira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='joaogabrielferr@gmail.com',
    keywords='Competitive programming',
    description=u'Package with implementation of some useful algorithms and data structures commonly used in competitive programming',
    packages=['AlgosandDataStructures'],
    install_requires=[''],)
import os
from setuptools import setup, find_packages


def get_version():
    project_dir = os.path.abspath(os.path.dirname(__file__))
    version_filename = os.path.join(project_dir, 'artefacts', 'VERSION')
    version = open(version_filename).read().strip()
    return version


setup(
    name='artefacts',
    version=get_version(),
    description='Extensible linter for dbt projects.',  
    author='Tom Waterman',
    author_email='tjwaterman99@gmail.com',
    url='https://github.com/tjwaterman99/miro-dbt-linter', 
    packages=find_packages(),
    install_requires=[
        'pydantic==1.8.2',
    ]
)
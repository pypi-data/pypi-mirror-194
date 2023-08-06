"""Gituptools setup file."""
import os
import setuptools

IID = os.getenv('CI_PIPELINE_IID')

with open('README.md') as f:
    long_description = f.read()

if __name__ == '__main__':
    setuptools.setup(
        name='gituptools',
        version=f'0.{IID}',
        author='Sol Courtney',
        author_email='sol.courtney@gmail.com',
        description='Python setuptools helper for Gitlab pipelines.',
        long_description=long_description,
        packages=setuptools.find_packages(),
        license='GPL'
        )

"""Gituptools setup file."""
import os
import setuptools

MAJOR = 0
MINOR = os.getenv('CI_PIPELINE_IID')

with open('README.md') as f:
    long_description = f.read()

if __name__ == '__main__':
    setuptools.setup(
        name='gituptools',
        version=f'{MAJOR!s}.{MINOR!s}',
        author='Sol Courtney',
        author_email='sol.courtney@gmail.com',
        description='Python setuptools helper for Gitlab pipelines.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='GPL',
        include_package_data=True,
        packages=['gituptools', 'gituptools.static'],
        package_dir={'gituptools': 'gituptools'},
        package_data={
            'gituptools': ['static/*']
            }
        )

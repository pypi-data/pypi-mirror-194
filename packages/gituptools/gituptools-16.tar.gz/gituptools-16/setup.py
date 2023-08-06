'''Gituptools setup file.'''
import os
import setuptools

# --------------------------------------------------------------------------- #

version = os.getenv('CI_PIPELINE_IID')
status = '4 - Beta'

with open('README.md') as f:
    long_description = f.read()

# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    setuptools.setup(
        name='gituptools',
        version=version,
        author='Sol Courtney',
        author_email='sol.courtney@gmail.com',
        description='Python setuptools helper for Gitlab pipelines.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='GNU General Public License v3 (GPLv3)',
        include_package_data=True,
        packages=['gituptools', 'gituptools.static'],
        package_dir={'gituptools': 'gituptools'},
        package_data={'gituptools': ['static/*']},
        keywords=['Gitlab', 'DevOps', 'CICD', 'Packaging'],
        python_requires='>=3.6',
        classifiers=[
            'Development Status :: %s' % status,
            'Topic :: Utilities',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            ]
        )

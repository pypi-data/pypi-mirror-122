# from distutils.core import setup
from setuptools import setup

setup(
    name='dbtjumpstart',
    packages=['dbtjumpstart'],
    version='0.1.3',
    license='MIT',
    description='A package to jumpstart a dbt project',
    author='Hari Prasad SA',
    author_email='sahariprasad@outlook.com',
    url='https://github.com/sahariprasad/dbt-jumpstart',
    download_url='https://github.com/sahariprasad/dbt-jumpstart/archive/refs/tags/v0.1.tar.gz',
    keywords=['dbt', 'jumpstart'],
    install_requires=[
        'pandas',
        'openpyxl',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

from setuptools import setup, find_packages

# Package metadata
NAME = 'pysparkify'
VERSION = '0.22'
DESCRIPTION = 'Spark based ETL'
URL = 'https://github.com/raohammad/pysparkify'
AUTHOR = 'Hammad Aslam KHAN'
AUTHOR_EMAIL = 'raohammad@gmail.com'
LICENSE = 'MIT'
KEYWORDS = ['python', 'pysparkify', 'etl', 'bigdata']

# Read the long description from the README file
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

# Define project dependencies
INSTALL_REQUIRES = [
    'pyyaml==6.0.1', 'pyspark==3.5.0'
]

# Classifiers for your package
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

# Define the setup configuration
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
)

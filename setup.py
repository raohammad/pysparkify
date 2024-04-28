# Setup script for the Pysparkify package
from setuptools import setup, find_packages

# Classifiers for your package
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

# Read the long description from the README file
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='pysparkify',
    version='0.26.2',
    description='Spark based ETL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hammad Aslam KHAN',
    author_email='raohammad@gmail.com',
    license='MIT',
    keywords=['python', 'pysparkify', 'etl', 'bigdata'],
    url='https://github.com/raohammad/pysparkify',
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.0.0',
        'pyyaml>=5.3'
    ],
    entry_points={
        'console_scripts': [
            'pysparkify=lib.app:main'
        ]
    },
    classifiers=CLASSIFIERS,
)

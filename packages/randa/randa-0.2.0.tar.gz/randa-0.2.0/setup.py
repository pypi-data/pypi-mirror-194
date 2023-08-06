from setuptools import setup, find_packages

setup(
    name='randa',
    version='0.2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'randa=randa.cli:main',
        ],
    },
)
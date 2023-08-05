from setuptools import setup

setup(
    name='sort_example',
    version='0.1.0',    
    description='A example Python package with sort methods',
    author='Artyom Kolosov',
    packages=['sort_example'],
    install_requires=[
                      'numpy>=1.20',                     
                      ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
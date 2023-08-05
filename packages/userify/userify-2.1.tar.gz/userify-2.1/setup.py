from setuptools import setup

setup(
    name="userify",
    version='2.1',
    description='A Python package for user-centric tasks',
    author='Akshat Sabharwal',
    author_email='akshatsabharwal35@gmail.com',
    packages=['userify'],
    install_requires=[
        'mysql.connector',
        'maskpass',
        'random2',
        'numpy',
    ],
)
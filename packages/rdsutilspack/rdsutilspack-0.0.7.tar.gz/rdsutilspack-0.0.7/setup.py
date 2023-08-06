from setuptools import setup

setup(
    name='rdsutilspack',
    version='0.0.7',
    description='My first Python package',
    author='johnson',
    author_email='johnssimon007@email.com',
    packages=['rdsutilspack'],
    install_requires=[
        'requests',
    ],
    entry_points={
    'console_scripts': [
        'rdsutilspack=rdsutilspack.__main__:main',
    ],
},
)

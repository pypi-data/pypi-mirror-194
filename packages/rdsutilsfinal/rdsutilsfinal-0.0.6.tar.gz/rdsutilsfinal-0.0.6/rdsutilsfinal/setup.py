from setuptools import setup

setup(
    name='rdsutilsfinal',
    version='0.0.6',
    description='My first Python package',
    author='johnson',
    author_email='johnssimon007@email.com',
    packages=['rdsutilsfinal'],
    install_requires=[
        'requests',
    ],
    entry_points={
    'console_scripts': [
        'rdsutilsfinal=rdsutilsfinal.__main__:main',
    ],
},
)

# -*- encoding: cp949 -*-

from setuptools import setup

with open('requirements.txt') as f:
	requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
    name='hdstreetview',
    version='0.1',
    description='Get pictures and timelines of panoramas from Naver Map.',
    long_description=long_description,
    url='https://github.com/arawatki97/hdstreetview',
    author='Hyundo_Kang',
    author_email='arawatki97@gmail.com',
    license='Hyundo_Kang',
    packages=['hdstreetview'],
    zip_safe=False,
    install_requires=requirements,
    test_suite='nose.collector',
    tests_require=['nose'],
)
	

from setuptools import setup

def readme():
    with open('readme.md') as f:
        return f.read()

setup(
    name='hdstreetview',
    version='0.1',
    description='Get pictures and timelines of panoramas from Naver Map.',
    long_description="hi",
    url='https://github.com/arawatki97/hdstreetview',
    author='Hyundo_Kang',
    author_email='arawatki97@gmail.com',
    license='MIT',
    packages=['hdstreetview'],
    zip_safe=False,
    install_requires=[
	    'requests',
	    'PIL',
	    'shutil',
	    'pandas',
	    'itertools',
	    'nose'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
	
